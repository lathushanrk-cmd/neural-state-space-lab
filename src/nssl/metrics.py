"""Descriptive metrics. Positive recovery fraction does NOT establish an attractor."""
import numpy as np

def reference_distance(Z, reference):
    z, ref = np.asarray(Z, float), np.asarray(reference, float)
    if z.shape != ref.shape or z.ndim not in (2, 3) or not np.isfinite(z).all() or not np.isfinite(ref).all():
        raise ValueError("matching finite components × time or trials × components × time needed")
    return np.linalg.norm(z - ref, axis=-2)

def recovery_fraction(distances, *, initial_index=0, horizon_index=-1, epsilon=1e-12):
    d = np.asarray(distances, dtype=float)
    if d.ndim not in (1, 2) or not np.isfinite(d).all() or (d < 0).any() or epsilon <= 0:
        raise ValueError("distances must be finite and nonnegative")
    start, end = d[..., initial_index], d[..., horizon_index]
    return (start - end) / (start + epsilon)

def time_to_recovery(distances, times, threshold, *, initial_index=0, require_consecutive=1):
    """First threshold crossing at/after initial_index; NaN if never crosses."""
    d, t = np.asarray(distances, float), np.asarray(times, float)
    if d.ndim not in (1, 2) or d.shape[-1] != len(t) or not np.isfinite(d).all() or (d < 0).any() or len(t) < 2 or not np.all(np.diff(t) > 0) or threshold < 0 or not np.isfinite(threshold) or require_consecutive < 1:
        raise ValueError("invalid distances, times or threshold")
    arr = d[None, :] if d.ndim == 1 else d
    output = np.full(len(arr), np.nan)
    for i, row in enumerate(arr):
        for j in range(initial_index, len(t) - require_consecutive + 1):
            if np.all(row[j:j + require_consecutive] <= threshold):
                output[i] = t[j] - t[initial_index]
                break
    return output[0] if d.ndim == 1 else output

def divergence_integral(distances, times):
    d, t = np.asarray(distances, float), np.asarray(times, float)
    if d.ndim not in (1, 2) or d.shape[-1] != len(t) or not np.isfinite(d).all() or (d < 0).any() or not np.all(np.diff(t) > 0):
        raise ValueError("invalid distance series/times")
    return np.trapezoid(d, t, axis=-1) if hasattr(np, "trapezoid") else np.trapz(d, t, axis=-1)

def directional_restoration(Z, reference, times, *, epsilon=1e-12):
    """Cosine(velocity, reference minus state). Undefined zero norms -> NaN."""
    from .trajectories import velocity
    z, ref = np.asarray(Z, float), np.asarray(reference, float)
    if z.shape != ref.shape or z.ndim not in (2, 3):
        raise ValueError("matching trajectories required")
    v, direction = velocity(z, times), ref - z
    dot = np.sum(v * direction, axis=-2)
    norm = np.linalg.norm(v, axis=-2) * np.linalg.norm(direction, axis=-2)
    return np.divide(dot, norm, out=np.full_like(dot, np.nan), where=norm > epsilon)

def local_trajectory_separation(perturbed, baseline):
    return reference_distance(perturbed, baseline)
