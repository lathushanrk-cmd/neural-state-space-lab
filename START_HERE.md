# START HERE — Neural State Space Lab

## What this project is

Neural State Space Lab is a computational neuroscience research prototype. It builds state-space trajectories and examines controlled **in-silico** perturbations under explicit mathematical models. All included figures are based on seeded synthetic data, not recordings of a stimulated brain.

## Installation (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
nssl-demo --output outputs/synthetic
```

## macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
nssl-demo --output outputs/synthetic
```

Browse `assets/` for simulated trajectories and regression-to-the-mean plots, and `docs/` for scientific concepts and limitations.

Optional public EEGBCI observational example (not yet independently verified on downloaded data):

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

No private participant data or unverified empirical results are bundled.
