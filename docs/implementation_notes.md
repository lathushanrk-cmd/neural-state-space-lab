# Implementation notes and scientific decisions

These notes describe design choices visible in the current implementation. They are not a diary of development, and they do not establish who wrote individual lines of code.

## Why trajectories?

A recording with many channels can be represented as a sequence of feature vectors. PCA or Factor Analysis can reduce that representation to a smaller set of coordinates that can be plotted and compared across time. These coordinates are **statistical representations**, not identified neuronal populations.

## Why distinguish observation from perturbation?

The `metrics` and `references` modules describe distances in supplied trajectories. The `perturb` module changes a numerical state, but that change alone does not determine future activity. The `dynamics` module therefore makes the propagation rule explicit, either as a specified continuous-time linear system or as a model estimated from data.

A synthetic stable system is a controlled numerical example. A fitted transition model produces a forecast whose validity is restricted by training data, prediction horizon, and held-out predictive error. Neither is physical stimulation.

## Why a training/reference split?

Scaling, embedding, and condition-reference construction may learn properties of the dataset. Using information from held-out trials can make performance appear better than it is. The example therefore constructs fitted transformations and references on training data and evaluates held-out trials separately.

This does not remove participant/session dependence. The EEG example is a within-participant descriptive illustration, not evidence of transfer to unseen subjects.

## Why include a regression-to-the-mean control?

Selecting a state because it is unusually far from a reference changes the expected value of later observations, even for some systems without active restoration. The example compares an apparent reduction in distance with this statistical alternative. A fall in distance alone does not justify calling a system a biological attractor.

## Important constraints

- Distances depend on scaling and coordinate choice.
- PCA or Factor Analysis may change with the sample and preprocessing choices.
- Fitted dynamics extrapolate; forecasts are not observations.
- The reference trajectory and observation window affect recovery metrics.
- Permutation and bootstrap validity depends on how recordings were sampled.
- The optional PhysioNet script has not been verified on downloaded recordings in this release.

## Evidence and reproduction

- [Source implementation](../src/nssl/) and [tests](../tests/) are the primary record of what the package does.
- [Reproducibility instructions](reproducibility.md) explain how to run the examples.
- [Validation record](../VALIDATION_REPORT.md) separates local/hosted checks from unverified biological work.
- [GitHub Actions](https://github.com/lathushanrk-cmd/neural-state-space-lab/actions) documents actual automated runs.

These decisions may be challenged or revised as the toolkit is tested on real recordings.
