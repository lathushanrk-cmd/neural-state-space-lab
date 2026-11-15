# PhysioNet EEGBCI: subject 1, motor imagery

This figure is derived from **actual public EEG recordings**, not the synthetic simulation used elsewhere in the repository.

Run `python reproduce/eegbci_demo.py` to reproduce the analysis. It downloads PhysioNet EEG Motor Movement/Imagery EDF files for subject 1, runs 6, 10 and 14, filters EEG at 7–30 Hz, selects hand/foot imagery events, and measures held-out trial distances to training-condition reference trajectories in PCA space.

The metadata records the event mapping and train/test trial counts. No permutation p-value, recovery claim, causal perturbation or across-subject finding is reported. The split is within participant and can have run/session dependence. The displayed distances are descriptive and preprocessing-dependent.

Source: https://physionet.org/content/eegmmidb/

Reproduction workflow: [optional real EEGBCI reproduction](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/workflows/real-eeg-validation.yml).
