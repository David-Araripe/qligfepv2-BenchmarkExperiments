from cinnabar import stats as cstats
from joblib import Parallel, delayed


def result_to_latex(res, latexify_each=False):
    """Round output to two decimal places and return a LaTeX string."""
    mle = round(res["mle"], 2)
    low = round(res["low"], 2)
    high = round(res["high"], 2)

    if latexify_each:
        return f"{mle:.2f}_{{{low:.2f}}}^{{{high:.2f}}}"
    else:
        return rf"{mle:.2f} <sub>({{{low:.2f}}}, {{{high:.2f}}})<\sub>"


def cinnabar_stats(avg_values, exp_values):
    """Compute the statistics using Cinnabar."""
    statistics = ["RMSE", "MUE", "KTAU"]

    def calculate_statistic(stat):
        cinnabar_stat = cstats.bootstrap_statistic(avg_values, exp_values, statistic=stat)
        return stat, result_to_latex(cinnabar_stat, latexify_each=False)

    results = Parallel(n_jobs=len(statistics))(delayed(calculate_statistic)(stat) for stat in statistics)
    return dict(results)
