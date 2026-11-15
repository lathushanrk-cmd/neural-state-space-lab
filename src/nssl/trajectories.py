"""Low-dimensional population trajectory utilities."""
import numpy as np

def velocity(Z, times):
    z = np.asarray(Z, dtype=float)
    t = np.asarray(times, dtype=float)
    if z.ndim < 2 or z.shape[-1] != len(t) or len(t) < 2 or not np.all(np.diff(t) > 0):
        raise ValueError("Z time dimension and strictly increasing times required")
    return np.gradient(z, t, axis=-1, edge_order=2 if len(t) >= 3 else 1)

def trajectory_centroid(Z):
    z = np.asarray(Z, dtype=float)
    if z.ndim != 3 or not np.isfinite(z).all():
        raise ValueError("expected finite trials × components × time")
    return np.mean(z, axis=0)
