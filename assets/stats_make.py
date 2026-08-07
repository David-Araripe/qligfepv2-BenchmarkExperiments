import numpy as np
from joblib import Parallel, delayed
from scipy.stats import kendalltau


def result_to_latex(res, latexify_each=False):
    """Round output to two decimal places and return a LaTeX string."""
    mle = round(res["mle"], 2)
    low = round(res["low"], 2)
    high = round(res["high"], 2)

    if latexify_each:
        return f"{mle:.2f}_{{{low:.2f}}}^{{{high:.2f}}}"
    else:
        return f"{mle:.2f} ({low:.2f}, {high:.2f})"


def bootstrap_statistic(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    statistic: str,
    ci: float = 0.95,
    nbootstrap: int = 1000,
    rng=None,
    return_verbose: bool = False,
    seed: int | None = None,
) -> dict:
    """Point estimate and bootstrap confidence interval for a comparison statistic.

    Resamples the paired ``(y_true, y_pred)`` values with replacement ``nbootstrap``
    times and reports the statistic computed on the full data (``mle``) together with
    the ``ci`` confidence-interval bounds (``low``/``high``). Supported statistics are
    "RMSE", "MUE" and "KTAU".

    This implementation mirrors QligFEP's analysis helper. ``return_verbose`` and
    ``seed`` are retained for compatibility with this repository's analysis notebook.
    """
    if rng is not None and seed is not None:
        raise ValueError("Pass either rng or seed, not both")
    if rng is None:
        rng = np.random.default_rng(12345 if seed is None else seed)

    # Drop pandas indexes so bootstrap indices are always positional.
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be the same length")

    try:
        compute = {
            "RMSE": lambda a, b: float(np.sqrt(np.mean((a - b) ** 2))),
            "MUE": lambda a, b: float(np.mean(np.abs(a - b))),
            "KTAU": lambda a, b: float(kendalltau(a, b)[0]),
        }[statistic]
    except KeyError as error:
        raise ValueError(f"Unknown statistic: {statistic}") from error

    n = len(y_true)
    s_n = np.empty(nbootstrap)
    for replicate in range(nbootstrap):
        idx = rng.choice(n, size=n, replace=True)
        s_n[replicate] = compute(y_true[idx], y_pred[idx])
    s_n.sort()

    low_frac = (1.0 - ci) / 2.0
    low_idx = int(np.floor(nbootstrap * low_frac))
    high_idx = min(int(np.ceil(nbootstrap * (1.0 - low_frac))), nbootstrap - 1)
    result = {
        "mle": compute(y_true, y_pred),
        "low": float(s_n[low_idx]),
        "high": float(s_n[high_idx]),
    }
    if return_verbose:
        result["all"] = s_n
    return result


def cinnabar_stats(avg_values, exp_values):
    """Compute bootstrapped RMSE, MUE, and Kendall's tau statistics."""
    statistics = ["RMSE", "MUE", "KTAU"]

    def calculate_statistic(stat):
        stat_result = bootstrap_statistic(avg_values, exp_values, statistic=stat)
        return stat, result_to_latex(stat_result, latexify_each=False)

    results = Parallel(n_jobs=len(statistics))(delayed(calculate_statistic)(stat) for stat in statistics)
    return dict(results)
