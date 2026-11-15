"""Training-only preprocessing to avoid leakage."""
import numpy as np
from sklearn.preprocessing import StandardScaler

class ChannelStandardizer:
    """Learn one mean/std per channel using training trials and times only."""
    def __init__(self):
        self.scaler = StandardScaler()
        self.n_features_ = None

    def fit(self, X):
        x = np.asarray(X, dtype=float)
        if x.ndim != 3 or not np.isfinite(x).all():
            raise ValueError("expected finite (trials, features, times)")
        self.n_features_ = x.shape[1]
        self.scaler.fit(x.transpose(0, 2, 1).reshape(-1, x.shape[1]))
        return self

    def transform(self, X):
        if self.n_features_ is None:
            raise RuntimeError("fit on training recordings before transform")
        x = np.asarray(X, dtype=float)
        if x.ndim != 3 or x.shape[1] != self.n_features_ or not np.isfinite(x).all():
            raise ValueError("shape or finite-value error")
        flattened = x.transpose(0, 2, 1).reshape(-1, x.shape[1])
        return self.scaler.transform(flattened).reshape(x.shape[0], x.shape[2], -1).transpose(0, 2, 1)

    def fit_transform(self, X):
        return self.fit(X).transform(X)
