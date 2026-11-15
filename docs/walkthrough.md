# Explain and demonstrate Neural State Space Lab

This walkthrough provides a reproducible demonstration and discussion questions. It is a preparation aid, **not evidence that an interview or live presentation has already occurred**.

## Before starting

Clone the repository, create an environment and run:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
nssl-demo --output outputs/synthetic
```

Open the generated files in `outputs/synthetic/`, or inspect the versioned figures in `assets/`.

## Two-minute explanation

**Question:** What problem does this address?

Multi-channel neural measurements are difficult to interpret directly because activity changes across features and time. A state-space representation summarizes those changes as trajectories. This toolkit asks how trajectories differ and what a **mathematical model** predicts after a controlled numerical change to a state.

**Question:** What is the input?

Either simulated trajectories or validated arrays of trials, features and time samples. MNE Epochs are accepted through an optional adapter.

**Question:** What happens to the input?

Fitted scaling and PCA/Factor Analysis produce low-dimensional coordinates. The software constructs reference trajectories, displaces a model state, runs a specified or fitted transition model and measures separation.

**Question:** What does a recovered trajectory mean?

Only that the chosen model predicted a reduction in the chosen distance over the chosen window. In a known stable system it is an expected mathematical result. It is not direct evidence of a person's neural recovery.

## Demonstration sequence

1. Show `assets/phase_portraits.png`. Explain the difference between a model that moves toward equilibrium and a model that moves away.
2. Open `src/nssl/simulation.py` and identify the system matrices.
3. Open `src/nssl/dynamics.py` and point to the propagation logic.
4. Show `assets/regression_to_mean_trap.png`. Explain why selecting an extreme value can create an apparent subsequent decrease.
5. Open `tests/` and demonstrate that expected numerical behaviour and invalid inputs are checked.
6. Explain that the public EEG example is not yet an independently reproduced empirical result.

## Likely questions

**Why not interpret your model as a biological mechanism?**  
Because dynamics inferred from reduced features are not uniquely identified neuronal mechanisms; additional experimental and independent-data evidence is needed.

**Why does your package have two kinds of dynamics?**  
A specified model tests numerical behaviour against a known system. A fitted model can summarize predictive structure in data, but has additional model-fit and generalization uncertainty.

**How can recovery be misleading?**  
Reference drift, scaling, selection of extreme states, measurement noise and regression to the mean can all change distances without an active restorative mechanism.

**What was actually verified?**  
Tests, synthetic figures, code quality and the outcomes shown in the GitHub Actions history. The external PhysioNet study remains a proposed reproducible example until its download and output have been checked.

**What would improve the project next?**  
Run the EEG example, check the events and trial splits against the actual recording, report observational outputs and negative controls, and assess generalization on independent sessions or subjects.
