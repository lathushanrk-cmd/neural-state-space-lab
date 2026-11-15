# Input, units and metadata

`NeuralTrajectoryDataset(X, times, metadata, units=...)` validates finite arrays of shape `(trial, feature, time)` and strictly increasing times. Metadata requires nonmissing `trial_id`, `condition`, `subject`; trial IDs must be unique. Missing sensor values are rejected rather than interpolated silently.

For MNE `Epochs`, call `NeuralTrajectoryDataset.from_mne(epochs)` and supply metadata containing subject and condition. This adapter does not automatically filter, repair bad channels, re-reference sensors, or resolve spatial mixing.

To prevent leakage use `ChannelStandardizer().fit(X_training).transform(X_test)`, never fitting on the test set.

Record dataset URL/version, preprocessing, event mapping, participants, sampling rate, channel types and license. Do not commit private or restricted participant recordings.
