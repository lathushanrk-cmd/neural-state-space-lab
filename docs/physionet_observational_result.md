# Public EEG demonstration: PhysioNet EEGBCI

The optional EEG example was executed successfully on a GitHub-hosted Ubuntu runner using downloaded public recordings on 15 November 2026. This is an **observational demonstration** and should not be described as a physical perturbation or neural recovery experiment.

## Recording and preprocessing

- Source: [PhysioNet EEG Motor Movement/Imagery](https://physionet.org/content/eegmmidb/)
- Participant: subject 1
- Motor imagery runs: 6, 10 and 14
- Events: `T1` = both hands (`hands: 2`) and `T2` = both feet (`feet: 3`), with rest events excluded
- EEG filter: 7–30 Hz
- Epoch window: 0.5–3.0 s after cue
- Training/test selection: seeded 70/30 stratified split within condition
- Usable epochs: 45 total; 30 training and 15 held out

The script fits channel standardization and a three-component PCA representation on the training trials only. It constructs training-condition average trajectories and computes each held-out trial's distance to its associated reference trajectory. It plots the mean within-condition distance over time.

## Reproducible evidence

- [Successful hosted workflow run](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/runs/43742073456)
- [Run artifact containing actual figure and metadata](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/runs/43742073456/artifacts/14173215481) (GitHub artifact retention is time-limited)
- Script: [`reproduce/eegbci_demo.py`](https://github.com/lathushanrk-cmd/neural-state-space-lab/blob/main/reproduce/eegbci_demo.py)
- Command: `python -m pip install -e ".[eeg]"`, then `python reproduce/eegbci_demo.py`

The workflow verifies that the figure exists, and that metadata report nonempty training and test sets. The output does not contain inferential p-values or claims of between-condition significance.

## Interpretation

These curves describe how held-out EEG trajectories relate to references learned from other trials of the **same participant**. Their magnitude depends on sensor filtering, feature scaling, the PCA projection, condition averaging and the selected time window. A difference between these curves, if present, would not by itself establish a biological restoring mechanism.

Important limitations remain: trials share a participant and potentially recording-run dependencies; the split is not cross-run or cross-participant; no independent replication or clinical interpretation is established. The example does not estimate causality or apply a perturbation.

The other figures in the repository's main `assets/` folder remain **synthetic** and should not be presented as participant recordings.
