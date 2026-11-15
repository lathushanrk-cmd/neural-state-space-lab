# Validation record — Neural State Space Lab 0.9.0

This report distinguishes tests of the software from evidence about real neural systems.

## Checks of the packaged implementation

The original local release checks reported:

| Check | Recorded outcome |
| --- | --- |
| Python unit tests | 39 passed |
| Source compilation | Passed |
| Synthetic figure generation | Four PNG figures, four SVG figures and numerical metadata generated |
| Synthetic notebook examples | Executed |
| Python wheel build and import | Passed in an existing Linux Python environment |
| MNE annotation mapping | Tested using artificial MNE recordings, not downloaded participant EEG |

## Hosted checks

The GitHub repository has subsequently run automated tests successfully on Ubuntu and Windows runners, as well as lint, a strict documentation build and a reproducible synthetic-figure verification job.

The [Actions history](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions) is the authoritative record for each commit. The workflow generates verification figures from source into a separate output directory; it does not silently alter scientific values. Passing hosted Windows checks is not equivalent to a separate installation test on a researcher's own laptop.

## What the checks do and do not establish

- Known-system simulations test numerical behaviour under explicitly defined mathematical dynamics.
- Regression-to-the-mean controls illustrate how conditional selection can produce misleading apparent recovery.
- Training-only fitting and split-aware reference construction reduce common forms of data leakage.
- An in-silico state displacement is not an observed response to physical neural stimulation.
- A decreasing reference distance does not establish a biological attractor or restorative mechanism.

## Executed public EEG example

On 15 November 2026, the optional PhysioNet EEGBCI script ran successfully on GitHub Actions using actual downloaded recordings for subject 1, runs 6, 10 and 14. The output reported **30 training trials** and **15 held-out trials** and generated a descriptive figure of distance to training-condition reference trajectories. Both image and metadata were verified and archived in the repository.

See [public EEG demonstration](docs/physionet_observational_result.md), [recorded figure](results/eegbci_subject1/eeg_observational.png) and [successful workflow](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/runs/43742073456).

This is **single-participant observational analysis**, not an intervention, proof of biological restoration, between-condition inferential finding or cross-participant replication.

## Not independently verified

- Cross-participant generalization on experimental neuroscience datasets.
- Independent biological or clinical validation.
- Distribution on PyPI, a registered DOI or peer-reviewed scientific publication.
- Installation on an independently configured Windows research laptop.

## Commands for reproduction

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m compileall -q src reproduce tests
nssl-demo --output outputs/synthetic
python reproduce/figure_1.py
python reproduce/figure_2.py
```

The optional external-data script is `reproduce/eegbci_demo.py` (requires `.[eeg]`). Results have been executed and checked for the specific subject and runs described above; additional datasets require separate verification.
