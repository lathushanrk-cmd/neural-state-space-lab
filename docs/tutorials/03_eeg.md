# Optional PhysioNet EEGBCI example

This uses public PhysioNet EEG Motor Movement/Imagery data, subject 1, runs 6, 10 and 14. It is **observational**. The script was successfully executed on public recordings on a GitHub runner; see the [verified data report](physionet_observational_result.md) and [figure](../../results/eegbci_subject1/eeg_observational.png).

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

The script explicitly maps `T1` to hands (2) and `T2` to feet (3), excluding `T0` rest annotations. Synthetic MNE unit tests verify the mapping logic, and a separate hosted execution verified the download and generation of descriptive output from public recordings.

It filters EEG 7–30 Hz, epochs 0.5–3.0 s after cues, splits trials within condition, learns scaling and PCA from training trials only, and measures test-trial distances from training-condition references. Outputs go to `outputs/eegbci/`.

This is not cross-subject or cross-run validation. It neither performs physical stimulation nor demonstrates causal restoration.
