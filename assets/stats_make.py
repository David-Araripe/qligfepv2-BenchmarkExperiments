import numpy as np
import scipy.stats
import sklearn.metrics
from joblib import Parallel, delayed


def result_to_latex(res, latexify_each=False):
    """Round output to two decimal places and return a LaTeX string."""
    mle = round(res["mle"], 2)
    low = round(res["low"], 2)
    high = round(res["high"], 2)

    if latexify_each:
        return f"{mle:.2f}_{{{low:.2f}}}^{{{high:.2f}}}"
    else:
        return f"{mle:.2f} ({low:.2f}, {high:.2f})"


# compute_statistic and bootstrap_statistic are adapted from
# https://github.com/OpenFreeEnergy/cinnabar/blob/main/cinnabar/stats.py
def compute_statistic(y_true, y_pred, statistic):
    """Compute requested statistic.

    Args:
        y_true: True values
        y_pred: Predicted values
        statistic: Statistic, one of ['RMSE', 'MUE', 'R2', 'rho','KTAU','RAE']
    """
    if statistic == "RMSE":
        return np.sqrt(sklearn.metrics.mean_squared_error(y_true, y_pred))
    elif statistic == "MUE":
        return sklearn.metrics.mean_absolute_error(y_true, y_pred)
    elif statistic == "R2":
        return scipy.stats.linregress(y_true, y_pred).rvalue ** 2
    elif statistic == "rho":
        return scipy.stats.pearsonr(y_true, y_pred)[0]
    elif statistic == "KTAU":
        return scipy.stats.kendalltau(y_true, y_pred)[0]
    elif statistic == "RAE":
        mae = sklearn.metrics.mean_absolute_error(y_true, y_pred)
        mad = np.mean(np.abs(np.mean(y_true) - y_true))
        return mae / mad
    raise ValueError(f"unknown statistic '{statistic}'")


def bootstrap_statistic(
    y_true,
    y_pred,
    dy_true=None,
    dy_pred=None,
    ci=0.95,
    statistic="RMSE",
    nbootstrap=1000,
    include_true_uncertainty=False,
    include_pred_uncertainty=False,
    return_verbose=False,
    seed=None,
):
    """Compute mean and confidence intervals of specified statistic.

    Args:
        y_true: True values
        y_pred: Predicted values
        dy_true: Errors of true values. If None, the values are assumed to have no errors
        dy_pred: Errors of predicted values. If None, the values are assumed to have no errors
        ci: Interval for confidence interval (CI)
        statistic: Statistic, one of ['RMSE', 'MUE', 'R2', 'rho','KTAU','RAE']
        nbootstrap: Number of bootstrap samples
        include_true_uncertainty: whether to account for the uncertainty in y_true when bootstrapping
        include_pred_uncertainty: whether to account for the uncertainty in y_pred when bootstrapping
        return_verbose: whether to return the all the metrics calculated with the bootstrap samples
        seed: A seed for the random number generator to ensure reproducibility.

    Returns:
        rmse_stats : dict of float
        'mle' : point estimate
        'mean' : mean RMSE
        'stderr' : standard error
        'low' : low end of CI
        'high' : high end of CI
    """
    # asarray also drops any pandas index, so the sampling below is positional
    # whether the caller passes arrays or Series.
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    dy_true = np.zeros_like(y_true) if dy_true is None else np.asarray(dy_true, dtype=np.float64)
    dy_pred = np.zeros_like(y_pred) if dy_pred is None else np.asarray(dy_pred, dtype=np.float64)

    if not (len(y_true) == len(y_pred) == len(dy_true) == len(dy_pred)):
        raise ValueError("y_true, y_pred and their errors must be the same length")

    sample_size = len(y_true)
    rng = np.random.default_rng(seed)
    s_n = np.zeros(nbootstrap, np.float64)
    for replicate in range(nbootstrap):
        # draw the whole replicate at once rather than element by element
        idx = rng.choice(np.arange(sample_size), size=sample_size, replace=True)
        y_true_sample = y_true[idx]
        y_pred_sample = y_pred[idx]
        if include_true_uncertainty:
            y_true_sample = rng.normal(loc=y_true_sample, scale=np.fabs(dy_true[idx]))
        if include_pred_uncertainty:
            y_pred_sample = rng.normal(loc=y_pred_sample, scale=np.fabs(dy_pred[idx]))
        s_n[replicate] = compute_statistic(y_true_sample, y_pred_sample, statistic)

    low_percentile = (1.0 - ci) / 2.0 * 100
    high_percentile = (1.0 + ci) / 2.0 * 100
    low, high = np.percentile(s_n, [low_percentile, high_percentile])

    result = {
        "mle": compute_statistic(y_true, y_pred, statistic),
        "stderr": np.std(s_n),
        "mean": np.mean(s_n),
        "low": low,
        "high": high,
    }
    if return_verbose:
        result["all"] = s_n
    return result


def cinnabar_stats(avg_values, exp_values):
    """Compute the statistics using Cinnabar."""
    statistics = ["RMSE", "MUE", "KTAU"]

    def calculate_statistic(stat):
        stat_result = bootstrap_statistic(avg_values, exp_values, statistic=stat)
        return stat, result_to_latex(stat_result, latexify_each=False)

    results = Parallel(n_jobs=len(statistics))(delayed(calculate_statistic)(stat) for stat in statistics)
    return dict(results)
