"""Condition- and split-specific reference trajectories."""
import numpy as np
import pandas as pd

class ConditionReference:
    """Fit condition mean trajectories from training trials ONLY."""
    def __init__(self):
        self.references_ = None
        self.shape_ = None

    def fit(self, Z, conditions):
        z = np.asarray(Z, dtype=float)
        c = np.asarray(conditions)
        if z.ndim != 3 or c.ndim != 1 or len(c) != len(z) or not np.isfinite(z).all() or pd.isna(c).any():
            raise ValueError("Z and conditions must match and be valid")
        self.references_ = {key: z[c == key].mean(axis=0) for key in np.unique(c)}
        self.shape_ = z.shape[1:]
        return self

    def transform(self, conditions):
        if self.references_ is None:
            raise RuntimeError("fit on training trials first")
        try:
            return np.stack([self.references_[key] for key in conditions])
        except KeyError as exc:
            raise ValueError(f"unseen condition {exc}") from exc

def leave_one_out_reference(Z, conditions):
    """Within-condition leave-one-out average; >=2 trials per condition."""
    z = np.asarray(Z, dtype=float)
    c = np.asarray(conditions)
    if z.ndim != 3 or len(c) != len(z) or not np.isfinite(z).all():
        raise ValueError("invalid trials or conditions")
    out = np.empty_like(z)
    for key in np.unique(c):
        mask = c == key
        n = int(mask.sum())
        if n < 2:
            raise ValueError("leave-one-out requires two or more trials per condition")
        out[mask] = (z[mask].sum(axis=0)[None, :, :] - z[mask]) / (n - 1)
    return out
