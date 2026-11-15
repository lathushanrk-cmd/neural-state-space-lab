# Optional PhysioNet EEGBCI example

This uses public PhysioNet EEG Motor Movement/Imagery data, subject 1, runs 6, 10 and 14. It is **observational**, with actual download and processing still unverified.

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

The script explicitly maps `T1` to hands (2) and `T2` to feet (3), excluding `T0` rest annotations. Synthetic MNE unit tests verify the mapping logic, not the external recordings.

It filters EEG 7–30 Hz, epochs 0.5–3.0 s after cues, splits trials within condition, learns scaling and PCA from training trials only, and measures test-trial distances from training-condition references. Outputs go to `outputs/eegbci/`.

This is not cross-subject or cross-run validation. It neither performs physical stimulation nor demonstrates causal restoration.
