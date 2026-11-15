"""One-time representational displacements; NOT physical brain interventions."""
from dataclasses import dataclass
import numpy as np
from .io import chronological_index

@dataclass(frozen=True)
class PerturbationResult:
    initial: np.ndarray
    displaced: np.ndarray
    delta: np.ndarray
    index: int
    time: float
    kind: str
    description: str

def _prepare(Z, times, time):
    z = np.asarray(Z, dtype=float)
    if z.ndim != 3 or not np.isfinite(z).all():
        raise ValueError("expected finite trials × components × times")
    t = np.asarray(times, dtype=float)
    if t.ndim != 1 or len(t) != z.shape[-1] or not np.all(np.diff(t) > 0):
        raise ValueError("invalid time array")
    idx = chronological_index(t, time)
    return z, idx, float(t[idx])

class IsotropicPerturbation:
    def __init__(self, magnitude=1.0, random_state=42):
        if not np.isfinite(magnitude) or magnitude < 0:
            raise ValueError("magnitude must be finite and nonnegative")
        self.magnitude, self.random_state = float(magnitude), random_state

    def apply(self, Z, *, times, time):
        z, idx, actual = _prepare(Z, times, time)
        rng = np.random.default_rng(self.random_state)
        d = rng.normal(size=z[:, :, idx].shape)
        d /= np.linalg.norm(d, axis=1, keepdims=True)
        d *= self.magnitude
        return PerturbationResult(z[:, :, idx].copy(), z[:, :, idx] + d, d, idx, actual, "isotropic", "fixed Euclidean norm in latent coordinates")

class AxisPerturbation:
    def __init__(self, magnitude=1.0, axis=0, direction=None):
        self.magnitude, self.axis, self.direction = magnitude, axis, direction

    def apply(self, Z, *, times, time):
        z, idx, actual = _prepare(Z, times, time)
        if not np.isfinite(self.magnitude) or self.magnitude < 0:
            raise ValueError("invalid magnitude")
        direction = np.zeros(z.shape[1]) if self.direction is None else np.asarray(self.direction, dtype=float)
        if self.direction is None:
            if not 0 <= self.axis < z.shape[1]:
                raise ValueError("invalid axis")
            direction[self.axis] = 1
        if direction.shape != (z.shape[1],) or not np.isfinite(direction).all() or np.linalg.norm(direction) == 0:
            raise ValueError("direction must be nonzero finite latent vector")
        d = np.broadcast_to(self.magnitude * direction / np.linalg.norm(direction), (len(z), z.shape[1])).copy()
        return PerturbationResult(z[:, :, idx].copy(), z[:, :, idx] + d, d, idx, actual, "axis", "unit-direction fixed-norm displacement")

class EmpiricalNoisePerturbation:
    """Draw empirical training residual vectors."""
    def __init__(self, residuals, magnitude=1.0, random_state=42):
        arr = np.asarray(residuals, dtype=float)
        if arr.ndim != 2 or not np.isfinite(arr).all() or len(arr) < 2:
            raise ValueError("residuals must be finite (observations, components), n>=2")
        if not np.isfinite(magnitude) or magnitude < 0:
            raise ValueError("invalid magnitude")
        self.residuals = arr - arr.mean(axis=0)
        self.magnitude, self.random_state = float(magnitude), random_state

    def apply(self, Z, *, times, time):
        z, idx, actual = _prepare(Z, times, time)
        if self.residuals.shape[1] != z.shape[1]:
            raise ValueError("residual feature mismatch")
        rng = np.random.default_rng(self.random_state)
        d = self.residuals[rng.integers(len(self.residuals), size=len(z))] * self.magnitude
        return PerturbationResult(z[:, :, idx].copy(), z[:, :, idx] + d, d, idx, actual, "empirical", "sampled centered training residuals")

class StateSwapPerturbation:
    def __init__(self, donor_indices):
        self.donor_indices = np.asarray(donor_indices)

    def apply(self, Z, *, times, time):
        z, idx, actual = _prepare(Z, times, time)
        indices = self.donor_indices
        if indices.ndim != 1 or len(indices) != len(z) or not np.issubdtype(indices.dtype, np.integer) or (indices < 0).any() or (indices >= len(z)).any():
            raise ValueError("donor_indices needs one valid trial index per trial")
        displaced = z[indices, :, idx].copy()
        initial = z[:, :, idx].copy()
        return PerturbationResult(initial, displaced, displaced - initial, idx, actual, "swap", "caller-selected donor trials; matching must be justified")
