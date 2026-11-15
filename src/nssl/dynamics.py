"""Explicit propagation: ground-truth ODE or trained linear transition model."""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import expm
from sklearn.linear_model import Ridge

@dataclass(frozen=True)
class Rollout:
    baseline: np.ndarray
    perturbed: np.ndarray
    times: np.ndarray
    description: str

def _states(initial):
    x = np.asarray(initial, dtype=float)
    if x.ndim != 2 or not np.isfinite(x).all():
        raise ValueError("initial states must be finite (trials, components)")
    return x

class LinearContinuousDynamics:
    """Known linear ODE dz/dt = A z; exact matrix exponential stepping."""
    def __init__(self, A):
        a = np.asarray(A, dtype=float)
        if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.isfinite(a).all():
            raise ValueError("A must be a finite square matrix")
        self.A = a.copy()

    def rollout(self, initial, times):
        x = _states(initial)
        t = np.asarray(times, dtype=float)
        if x.shape[1] != len(self.A) or t.ndim != 1 or len(t) < 2 or not np.isfinite(t).all() or not np.all(np.diff(t) > 0):
            raise ValueError("incompatible states or times")
        return np.stack([x @ expm(self.A * (ti - t[0])).T for ti in t], axis=-1)

    def compare(self, initial, displaced, times):
        return Rollout(self.rollout(initial, times), self.rollout(displaced, times), np.asarray(times), "exact known-system linear ODE evolution")

class RegularizedLinearDynamics:
    """Data-fitted one-step map z[t+1]=W z[t]+b; no causal interpretation.
    Fit on training trials only and evaluate held-out recordings.
    Assumes uniform time steps.
    """
    def __init__(self, alpha=1.0):
        if not np.isfinite(alpha) or alpha <= 0:
            raise ValueError("positive ridge alpha required")
        self.alpha = alpha
        self.model = None
        self.dt_ = None
        self.components_ = None

    def fit(self, Z, times):
        z = np.asarray(Z, dtype=float)
        t = np.asarray(times, dtype=float)
        if z.ndim != 3 or len(t) != z.shape[-1] or len(t) < 3 or not np.isfinite(z).all() or not np.isfinite(t).all():
            raise ValueError("finite trials × components × times and valid times required")
        d = np.diff(t)
        if not (d > 0).all() or not np.allclose(d, d[0], rtol=1e-5, atol=1e-10):
            raise ValueError("trained transition model requires uniform sampling")
        self.dt_ = float(d[0])
        self.components_ = z.shape[1]
        x = z[:, :, :-1].transpose(0, 2, 1).reshape(-1, z.shape[1])
        y = z[:, :, 1:].transpose(0, 2, 1).reshape(-1, z.shape[1])
        self.model = Ridge(alpha=self.alpha).fit(x, y)
        return self

    def rollout(self, initial, steps):
        if self.model is None:
            raise RuntimeError("fit on training data first")
        x = _states(initial)
        if x.shape[1] != self.components_ or not isinstance(steps, int) or steps < 1:
            raise ValueError("invalid initial states or steps")
        out = [x.copy()]
        for _ in range(steps):
            x = self.model.predict(x)
            out.append(x.copy())
        return np.stack(out, axis=-1)

    def compare(self, initial, displaced, steps):
        t = np.arange(steps + 1) * self.dt_
        return Rollout(self.rollout(initial, steps), self.rollout(displaced, steps), t, "model-dependent ridge transition forecast; not an observed response")

    def evaluate_one_step(self, Z):
        """Held-out MSE and persistence baseline MSE; lower is better."""
        if self.model is None:
            raise RuntimeError("fit first")
        z = np.asarray(Z, dtype=float)
        if z.ndim != 3 or z.shape[1] != self.components_ or z.shape[2] < 2:
            raise ValueError("incompatible held-out array")
        x = z[:, :, :-1].transpose(0, 2, 1).reshape(-1, z.shape[1])
        y = z[:, :, 1:].transpose(0, 2, 1).reshape(-1, z.shape[1])
        return {"model_mse": float(np.mean((self.model.predict(x) - y) ** 2)),
                "persistence_mse": float(np.mean((x - y) ** 2))}
