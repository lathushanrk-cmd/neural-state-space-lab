"""Validated trial × feature × time representation and optional MNE interface."""
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class NeuralTrajectoryDataset:
    data: np.ndarray
    times: np.ndarray
    metadata: pd.DataFrame
    units: str = "arbitrary"

    def __post_init__(self):
        x = np.asarray(self.data, dtype=float)
        times = np.asarray(self.times, dtype=float)
        meta = pd.DataFrame(self.metadata).reset_index(drop=True).copy()
        if x.ndim != 3 or min(x.shape) < 1:
            raise ValueError("data must have nonempty shape (trials, features, times)")
        if times.ndim != 1 or len(times) != x.shape[2] or not np.isfinite(times).all():
            raise ValueError("times must be finite and match time dimension")
        if len(times) < 2 or not np.all(np.diff(times) > 0):
            raise ValueError("times must contain at least two strictly increasing samples")
        if not np.isfinite(x).all():
            raise ValueError("data must be finite; handle NaN/inf before construction")
        if len(meta) != x.shape[0]:
            raise ValueError("metadata must have exactly one row per trial")
        for name in ("trial_id", "condition", "subject"):
            if name not in meta.columns or meta[name].isna().any():
                raise ValueError(f"metadata must have nonmissing {name}")
        if not meta.trial_id.is_unique:
            raise ValueError("trial_id must be unique")
        if not isinstance(self.units, str) or not self.units:
            raise ValueError("units must be a nonempty string")
        object.__setattr__(self, "data", x.copy())
        object.__setattr__(self, "times", times.copy())
        object.__setattr__(self, "metadata", meta)

    def subset(self, indices):
        indices = np.arange(len(self.data))[indices] if isinstance(indices, slice) else np.asarray(indices)
        return NeuralTrajectoryDataset(self.data[indices], self.times, self.metadata.iloc[indices], self.units)

    @classmethod
    def from_mne(cls, epochs, *, picks="data", units=None):
        """MNE Epochs input; default SI units. No implicit filter/baseline/repair."""
        try:
            x = epochs.get_data(picks=picks, units=units, copy=True)
        except TypeError:
            x = epochs.get_data(picks=picks, units=units)
        metadata = epochs.metadata.copy() if epochs.metadata is not None else pd.DataFrame(index=range(len(x)))
        if "trial_id" not in metadata:
            metadata["trial_id"] = [f"trial_{i}" for i in range(len(x))]
        if "condition" not in metadata:
            raise ValueError("MNE epochs.metadata needs a 'condition' column")
        if "subject" not in metadata:
            raise ValueError("MNE epochs.metadata needs a 'subject' column")
        return cls(x, np.asarray(epochs.times), metadata, units=units or "MNE channel SI")


def chronological_index(times, time, *, tolerance=None):
    """Locate the nearest existing sample, rejecting out-of-range times."""
    t = np.asarray(times, dtype=float)
    if not np.isfinite(time) or time < t[0] or time > t[-1]:
        raise ValueError("requested time lies outside recorded interval")
    i = int(np.argmin(np.abs(t - time)))
    if tolerance is not None and abs(t[i] - time) > tolerance:
        raise ValueError("no sample within requested tolerance")
    return i
