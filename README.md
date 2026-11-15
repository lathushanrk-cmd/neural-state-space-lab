# Neural State Space Lab

**An Open-Source Perturbation and Recovery Toolkit for Neural Population Dynamics**

Neural State Space Lab (NSSL) is a Python research software prototype exploring how trajectories of neural population activity respond to **computational perturbations** under explicitly defined dynamical models.

A neural state space represents activity from many recording channels as a point moving through a mathematical space. NSSL aims to help researchers build trajectories, impose controlled in-silico changes, and measure how simulated trajectories approach or separate from references.

## Scientific workflow

Neural recordings or simulated signals → preprocessing → dimensionality reduction → trajectories → controlled in-silico perturbations → model propagation → recovery and divergence metrics → statistical checks → figures.

## Current repository status

**The complete project has not yet been published in this GitHub repository.** The source release is prepared separately as version **0.9.0**, but uploading its files is still pending. This repository README is an introductory placeholder, **not an installable software release**. No tests or GitHub Actions have run on this repository yet.

The prepared local archive includes Python source, tests, documentation, simulated figures, and examples. Its local validation work reported **39 passing tests**, successful packaging, and synthetic figure generation. Native Windows installation, the online EEGBCI demonstration, remote CI runs and independent biological validation are **unverified**.

## Interpretation and limitations

- A computational perturbation does **not** physically stimulate the brain.
- Model recovery does **not** independently establish biological attractor dynamics.
- Synthetic figures are simulations, not empirical neuroscience findings.
- This project is not a diagnostic tool or clinically validated medical device.

## Author

**Lathushan RK**  
Department of Life Sciences, NSBM Green University, Sri Lanka.

Biomedical Science undergraduate interested in computational neuroscience, neural dynamics, brain-state representation, and neurophysiology.

## License and citation

License and complete citation metadata will accompany the full source-code publication. Do not infer a software release or DOI from this introductory README.
