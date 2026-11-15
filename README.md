# Neural State Space Lab

**Research software for studying perturbation and recovery in low-dimensional neural state spaces**

[![Tests](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/workflows/tests.yml)
[![Documentation](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/workflows/docs.yml/badge.svg)](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions/workflows/docs.yml)
[MIT license](LICENSE) · Python 3.10+ · Version 0.9.0

![A synthetic population-signal example, two trajectories in a known linear system, and their separation over time](assets/hero_simulation.png)

*Figure: simulated signals and trajectories propagated using a specified linear dynamical system. No experimental neural data are shown.*

## Overview

Recordings from many neural channels can be treated as a sequence of population states. After dimensionality reduction, each state becomes a point in a smaller coordinate space, and the points across time form a trajectory.

Neural State Space Lab (NSSL) provides tools to examine how these trajectories relate to reference trajectories and how a **computationally displaced state** evolves under an explicitly chosen model. The aim is to make the assumptions behind perturbation-and-recovery analyses inspectable and reproducible.

There are three distinct uses:

- **Observed trajectories:** describe distance and movement in recorded or simulated data.
- **Known-system simulations:** perturb an initial state in a defined dynamical system and calculate its future trajectory.
- **Fitted-model forecasts:** estimate a linear transition model from training data and examine hypothetical future trajectories, with predictive error assessed on held-out observations.

A change to latent coordinates is not physical brain stimulation. Model-predicted recovery is not evidence, by itself, that the brain has an attractor.

## Methods implemented

| Component | Implementation |
| --- | --- |
| Data handling | Trial × feature × time arrays, metadata checks, optional MNE Epochs adapter |
| Preprocessing | Channel standardization fitted on training recordings |
| Embedding | PCA and Factor Analysis |
| References | Condition-specific means and leave-one-out reference trajectories |
| State changes | Random fixed-norm, directional, empirical-residual and trial-state-swap displacements |
| Dynamics | Exact linear continuous-time propagation and ridge-fitted discrete transitions |
| Descriptive measures | Reference distance, recovery fraction, recovery threshold time, separation and divergence |
| Controls | Label permutations, time shifts, phase-randomized surrogates and a regression-to-the-mean demonstration |
| Uncertainty | Bootstrap mean intervals and permutation probabilities |

The mathematical assumptions, units and statistical restrictions are described in [the documentation](docs/index.md).

## Install and run

Clone this repository, open a terminal in its root folder, then install the package.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
nssl-demo --output outputs/synthetic
```

For Windows PowerShell, a Python 3.11 virtual environment can be created with:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

The demonstration writes figures and numerical results to `outputs/synthetic/`. It uses seeded synthetic inputs and does not download participant recordings.

### Minimal example: perturb a known stable system

```python
import numpy as np
from nssl.dynamics import LinearContinuousDynamics
from nssl.simulation import system_matrix
from nssl.metrics import local_trajectory_separation

times = np.linspace(0, 5, 201)
initial = np.array([[1.0, 0.5]])
displaced = initial + np.array([[0.4, 0.0]])

model = LinearContinuousDynamics(system_matrix("stable"))
result = model.compare(initial, displaced, times)
separation = local_trajectory_separation(result.perturbed, result.baseline)

print("Initial distance:", separation[0, 0])
print("Final distance:", separation[0, -1])
```

For this specified stable system, the two calculated trajectories approach one another. This example checks the behaviour of the numerical model, not a person's neural response.

## Two useful controls

**Stable and unstable dynamics.** The [phase portrait](assets/phase_portraits.png) shows trajectories in stable, unstable and damped oscillatory linear systems. The underlying matrices are specified in [`simulation.py`](src/nssl/simulation.py); the example provides a known mathematical answer against which to check the implementation.

**Selection effects.** The [regression-to-the-mean example](assets/regression_to_mean_trap.png) starts with stationary simulated noise. Selecting unusually large deviations creates an apparent subsequent decrease. This matters because a reduction in distance is not sufficient to infer active restoration.

The figures are recreated by running:

```bash
python reproduce/figure_1.py
python reproduce/figure_2.py
```

## Working with neural recordings

The core package accepts appropriately structured feature arrays. An optional [EEGBCI example](reproduce/eegbci_demo.py) illustrates an observational workflow using public PhysioNet EEG Motor Movement/Imagery recordings, with training-only transformations and explicit cue mapping.

```bash
python -m pip install -e ".[eeg]"
python reproduce/eegbci_demo.py
```

The EEG example has now been **executed on downloaded public recordings** for PhysioNet subject 1 (runs 6, 10 and 14): 30 training and 15 held-out trials. View the [actual observational figure](results/eegbci_subject1/eeg_observational.png), [output metadata](results/eegbci_subject1/eeg_observational_metadata.json) and [reproduction report](docs/physionet_observational_result.md). This is a single-participant descriptive analysis, not a perturbation experiment, statistical group finding or evidence of cross-participant generalization.

## Testing and scientific scope

The codebase includes unit tests of numerical behaviour, data validation, error handling, and synthetic event mapping. The [GitHub Actions workflows](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions) run tests across supported Python versions and operating systems, check documentation and linting, and verify synthetic figure generation. Check the workflow history for the result on a particular commit.

The [validation report](VALIDATION_REPORT.md) records the local checks and their scope. Software checks support reproducibility of the implementation; they do not validate the biological interpretation of a fitted dynamical model.

In particular, latent coordinates depend on preprocessing, recovery estimates can be affected by reference choice and selection bias, and null tests must respect the dependence structure of the experiment. See [limitations](docs/limitations.md), [dynamics](docs/dynamics.md) and [experimental design](docs/experimental_design.md).

For an explanation of the implementation decisions, see [implementation notes](docs/implementation_notes.md). A short [demonstration walkthrough](docs/walkthrough.md) shows how to reproduce and discuss the synthetic analyses.

## Repository contents

- [`src/nssl/`](src/nssl/) — Python implementation
- [`tests/`](tests/) — known-answer and boundary-condition tests
- [`examples/`](examples/) — notebooks
- [`reproduce/`](reproduce/) — figure generation, benchmark and optional EEG example
- [`docs/`](docs/) — concepts, methods, statistics and tutorials
- [`assets/`](assets/) — generated synthetic figures and numerical record

## Author and license

**Lathushan RK** — Independent researcher  
Research interests: computational neuroscience, neural dynamics, brain-state representation and neurophysiology.

The code is distributed under the [MIT License](LICENSE). For citation details see [`CITATION.cff`](CITATION.cff); for proposed changes see [`CONTRIBUTING.md`](CONTRIBUTING.md). Version 0.9.0 is a research-software pre-release, not an independently biologically validated tool.
