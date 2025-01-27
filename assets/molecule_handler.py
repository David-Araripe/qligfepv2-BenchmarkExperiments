from functools import partial
import pandas as pd
import json
from pathlib import Path
from chemFilters.img_render import MolPlotter
from joblib import Parallel, delayed
from multiprocessing import Pool
from loguru import logger
from tqdm import tqdm


def data_from_lomap_json(
    json_path: str,
    exp_ddG: str = "ddG",
    calc_ddG_avg: str = "Q_ddG_avg",
    calc_ddG_err: str = "Q_ddG_sem",
):
    with Path(json_path).open("r") as f:
        mapping_data = json.load(f)

    perturbation = []
    vals_exp = []
    vals_calc = []
    vals_calc_err = []

    for edge in mapping_data["edges"]:
        perturbation.append((edge["from"], edge["to"]))
        vals_exp.append(edge[exp_ddG])
        vals_calc.append(edge[calc_ddG_avg])
        vals_calc_err.append(edge[calc_ddG_err])

    return perturbation, vals_exp, vals_calc, vals_calc_err


def lomap_json_to_dataframe(lomap_json: dict, molplotter: MolPlotter):
    return pd.DataFrame.from_dict(lomap_json["edges"]).assign(
        from_smiles=lambda x: x["from"].apply(lambda y: lomap_json["nodes"][y]["smiles"]),
        to_smiles=lambda x: x["to"].apply(lambda y: lomap_json["nodes"][y]["smiles"]),
    )


def add_images_to_df(df, molplotter: MolPlotter, n_jobs=4):
    from MolClusterkit.mcs import MCSClustering
    mcs_handler = MCSClustering([], timeout=20, atomCompare="CompareAnyHeavyAtom", bondCompare="CompareAny")
    partial_func = partial(molplotter.render_mol, return_svg=True)
    # find the matching pose
    pairs = list(zip(df["from_smiles"].tolist(), df["to_smiles"].tolist()))
    pairs = tqdm(pairs, total=len(pairs))
    logger.info("Calculating MCS similarity")
    results = Parallel(n_jobs=n_jobs)(
        delayed(mcs_handler.pairwise_mcs_similarity)(p) for p in pairs
    )
    smarts_strings, _ = zip(*results)
    from_variables = list(zip(df["from_smiles"].tolist(), df["from"].tolist(), smarts_strings))
    to_variables = list(zip(df["to_smiles"].tolist(), df["to"].tolist(), smarts_strings))
    to_svgs = []
    with Pool(4) as p:
        from_svgs = p.starmap(partial_func, from_variables)
        to_svgs = p.starmap(partial_func, to_variables)
    # for _from, _to in zip(from_variables, to_variables):
    #     to_svgs.append(molplotter.render_mol(*_to, match_pose=_from[0], return_svg=True))
    df = df.assign(from_svg=from_svgs, to_svg=to_svgs)
    return df

