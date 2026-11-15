# Neural State Space Lab — validation record

**Package version:** 0.9.0 (research pre-release candidate). These are software-engineering and mathematical synthetic checks, **not biological validation**.

## Previously executed locally on the supplied archive

| Check | Recorded result | Scope |
|---|---|---|
| Unit tests | 39 passed | Including 2 offline synthetic MNE event-mapping tests |
| Compilation | Passed | Source, reproduction scripts and tests |
| Synthetic demonstration | Four PNG, four SVG and JSON produced | Seeded simulations and exact model propagation |
| Synthetic notebooks | Both ran | No external EEG download |
| Wheel | Built and imported | Existing Linux scientific Python environment |
| Internal Markdown links | Checked | Relative targets in local archive |
| EEG event codes | Explicit `T1 → hands=2`, `T2 → feet=3` tested | Artificial MNE RawArray annotations only |

**Remote repository results may differ until GitHub Actions complete.** Never report a workflow as passing merely because its YAML file exists.

## Key scientific correction

The EEG script extracts hand/foot annotations with `mne.events_from_annotations(..., event_id={"hands":2,"feet":3})` and passes the returned event table to `mne.Epochs`, rather than relying on implicit annotation numbering. It also checks for missing cue types and excludes rest events. Real PhysioNet run execution remains unverified.

## Unverified

- Native Windows installation and execution on an independently configured machine.
- Real PhysioNet EEGBCI download and participant-level results.
- Remote CI until results appear in the repository Actions tab.
- Independent cross-subject, biological and clinical validation.
- Package publication on PyPI, registered DOI and external peer review.

## Repeat core checks

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m compileall -q src reproduce tests
nssl-demo --output outputs/synthetic
python reproduce/figure_1.py
python reproduce/figure_2.py
```

Optional separately network-dependent run:

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

A synthetic rollout validates its mathematical implementation, not its use as a description of living brain dynamics. Declining reference distance alone is insufficient evidence for a biological attractor.
