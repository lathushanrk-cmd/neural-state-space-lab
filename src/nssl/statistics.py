"""Cluster-aware bootstrap and empirical null probabilities."""
import numpy as np

def bootstrap_mean_ci(values, *, confidence=0.95, n_boot=2000, random_state=42, groups=None):
    x = np.asarray(values, float)
    if x.ndim != 1 or not np.isfinite(x).all() or len(x) < 2 or not 0 < confidence < 1 or n_boot < 100:
        raise ValueError("need finite 1D values, >=2, and >=100 bootstrap replicates")
    rng = np.random.default_rng(random_state)
    if groups is None:
        estimates = np.mean(x[rng.integers(len(x), size=(n_boot, len(x)))], axis=1)
    else:
        g = np.asarray(groups)
        if g.shape != x.shape:
            raise ValueError("groups must match values")
        ids = np.unique(g)
        if len(ids) < 2:
            raise ValueError("need >=2 independent groups")
        subject_means = np.array([x[g == key].mean() for key in ids])
        estimates = np.mean(subject_means[rng.integers(len(ids), size=(n_boot, len(ids)))], axis=1)
        x = subject_means
    alpha = (1 - confidence) / 2
    return {"estimate": float(x.mean()), "lower": float(np.quantile(estimates, alpha)),
            "upper": float(np.quantile(estimates, 1 - alpha)), "confidence": confidence,
            "n_boot": n_boot, "sampling_unit": "groups" if groups is not None else "observations"}

def permutation_pvalue(observed, null_statistics, *, alternative="two-sided", center=0.0):
    null = np.asarray(null_statistics, float)
    if null.ndim != 1 or not len(null) or not np.isfinite(null).all() or not np.isfinite(observed):
        raise ValueError("invalid observed statistic or null distribution")
    if alternative == "greater":
        count = np.count_nonzero(null >= observed)
    elif alternative == "less":
        count = np.count_nonzero(null <= observed)
    elif alternative == "two-sided":
        count = np.count_nonzero(abs(null - center) >= abs(observed - center))
    else:
        raise ValueError("unknown alternative")
    return (count + 1) / (len(null) + 1)
