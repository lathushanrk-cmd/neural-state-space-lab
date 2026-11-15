"""Null transformations; validity and exchangeability remain experiment-dependent."""
import numpy as np

def permute_trial_labels(labels, random_state=42, *, groups=None):
    c = np.asarray(labels).copy()
    rng = np.random.default_rng(random_state)
    if c.ndim != 1:
        raise ValueError("labels must be one dimensional")
    if groups is None:
        return rng.permutation(c)
    g = np.asarray(groups)
    if g.shape != c.shape:
        raise ValueError("groups must match labels")
    for key in np.unique(g):
        mask = g == key
        c[mask] = rng.permutation(c[mask])
    return c

def shift_reference(reference, random_state=42, *, min_shift=1):
    r = np.asarray(reference, float)
    if r.ndim not in (2, 3) or not np.isfinite(r).all() or min_shift < 1 or 2 * min_shift > r.shape[-1]:
        raise ValueError("cannot shift reference at required distance")
    rng = np.random.default_rng(random_state)
    shift = int(rng.integers(min_shift, r.shape[-1] - min_shift + 1))
    return np.roll(r, shift, axis=-1)

def random_times(n_times, n_draws, random_state=42, *, margins=1):
    if n_times <= 2 * margins or n_draws < 1 or margins < 0:
        raise ValueError("invalid time window")
    return np.random.default_rng(random_state).integers(margins, n_times - margins, size=n_draws)

def phase_randomized_surrogate(series, random_state=42):
    """Shared random phase per frequency across channels, preserving auto/cross spectra."""
    x = np.asarray(series, float)
    if x.ndim != 2 or x.shape[-1] < 4 or not np.isfinite(x).all():
        raise ValueError("finite 2D data with at least four samples required")
    rng = np.random.default_rng(random_state)
    spectrum = np.fft.rfft(x, axis=-1)
    phases = rng.uniform(0, 2 * np.pi, size=spectrum.shape[-1])
    phases[0] = 0.0
    if x.shape[-1] % 2 == 0:
        phases[-1] = 0.0
    return np.fft.irfft(spectrum * np.exp(1j * phases)[None, :], n=x.shape[-1], axis=-1)

def permute_reference_trials(reference, random_state=42, *, groups=None):
    r = np.asarray(reference, float)
    if r.ndim != 3:
        raise ValueError("trial-wise reference array required")
    rng = np.random.default_rng(random_state)
    if groups is None:
        return r[rng.permutation(len(r))]
    g = np.asarray(groups)
    if g.shape != (len(r),):
        raise ValueError("groups shape mismatch")
    out = r.copy()
    for key in np.unique(g):
        mask = np.flatnonzero(g == key)
        out[mask] = r[rng.permutation(mask)]
    return out
