"""Train-once, transform-many latent representations."""
import numpy as np
from sklearn.decomposition import PCA, FactorAnalysis

def _array(X):
    x = np.asarray(X.data if hasattr(X, "metadata") else X, dtype=float)
    if x.ndim != 3 or not np.isfinite(x).all():
        raise ValueError("expected finite (trials, features, times) array")
    return x

class _Embedding:
    estimator = None
    def __init__(self, n_components=3, random_state=42):
        self.n_components = n_components
        self.random_state = random_state
        self.model = None
        self.n_features_ = None

    def fit(self, X):
        x = _array(X)
        if not isinstance(self.n_components, int) or not 1 <= self.n_components <= min(x.shape[1], x.shape[0] * x.shape[2]):
            raise ValueError("n_components exceeds available dimensions/samples")
        self.model = self.estimator(n_components=self.n_components, random_state=self.random_state)
        self.model.fit(x.transpose(0, 2, 1).reshape(-1, x.shape[1]))
        self.n_features_ = x.shape[1]
        return self

    def transform(self, X):
        if self.model is None:
            raise RuntimeError("fit on training data first")
        x = _array(X)
        if x.shape[1] != self.n_features_:
            raise ValueError("feature dimension mismatch")
        return self.model.transform(x.transpose(0, 2, 1).reshape(-1, x.shape[1])).reshape(x.shape[0], x.shape[2], self.n_components).transpose(0, 2, 1)

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        if self.model is None:
            raise RuntimeError("fit first")
        z = _array(Z)
        if z.shape[1] != self.n_components:
            raise ValueError("latent feature dimension mismatch")
        zt = z.transpose(0, 2, 1).reshape(-1, z.shape[1])
        if isinstance(self.model, FactorAnalysis):
            xt = zt @ self.model.components_ + self.model.mean_
        else:
            xt = self.model.inverse_transform(zt)
        return xt.reshape(z.shape[0], z.shape[2], -1).transpose(0, 2, 1)

class PCAEmbedding(_Embedding):
    estimator = PCA
    @property
    def explained_variance_ratio_(self):
        if self.model is None:
            raise RuntimeError("fit first")
        return self.model.explained_variance_ratio_

class FactorAnalysisEmbedding(_Embedding):
    estimator = FactorAnalysis
