# Reproducibility

## Synthetic demo

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python reproduce/figure_1.py
nssl-demo --output outputs/synthetic
```

Figures are generated from mathematically defined systems and seeded synthetic processes (seed 42). The scripts `figure_1.py` and `figure_2.py` call the same generating function. Keep generated figures and numerical metadata together.

## Benchmarks

`python reproduce/benchmark.py` records local hardware- and environment-dependent measurements; Python `tracemalloc` does not capture all native memory allocations.

## Optional public EEG demo

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

This external-data demonstration has not been independently verified on downloaded participant recordings. Keep package versions, data provenance, seed, channel units, and train/test splits. Do not commit raw participant files.
