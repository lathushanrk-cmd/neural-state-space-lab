# Neural State Space Lab — Original Master Guide (archival roadmap)

> **Historical planning document, edited for clarity.** This is a preserved overview of the project requirements in the uploaded archive, not the authoritative current API documentation. Some original illustrative APIs and release milestones were aspirational rather than implemented. For functioning commands use the [README](https://github.com/lathushanrk-cmd/neural-state-space-lab#readme), [API index](api/index.md), [validation record](https://github.com/lathushanrk-cmd/neural-state-space-lab/blob/main/VALIDATION_REPORT.md), and actual Python source and tests.

## 1. Identity

**Neural State Space Lab** — An Open-Source Perturbation and Recovery Toolkit for Neural Population Dynamics.

Scientific identity: a Python toolkit for embedding neural population recordings into low-dimensional state spaces, applying controlled in-silico perturbations and quantifying recovery, divergence and dynamical stability under explicit statistical and mathematical assumptions.

It is **not** a generic PCA viewer, clinical classifier, real-time diagnosis system, conference-paper repository or a claim that simulated state changes are physical neural stimulation.

## 2. Why it exists

Multi-channel neural recordings may be described as time-dependent trajectories. A reproducible research tool should do more than display PCA: it should enable controlled representational changes, explicit propagation, recovery measurements, known-answer tests and suitable controls.

**Workflow:** Signals → preprocessing → embedding → trajectories → computational perturbation → defined propagation model → descriptive metrics → null/statistical checks → figures.

## 3. Minimum scope

Synthetic and generic array input, optional MNE EEG interface, PCA and Factor Analysis, reference trajectories, four perturbation operators, recovery and divergence metrics, null models, bootstrap intervals, reproducible figures, notebooks, tests, an installable package and CI workflows. Avoid adding many embedding algorithms before basic correctness.

## 4. Mathematical states

Let the observed population state be $x(t)\in\mathbb R^p$ and its low-dimensional projection $z(t)=f(x(t))\in\mathbb R^k$. Across trial times, $z_i(t)$ traces a trajectory.

A one-time perturbation changes the initial state $\tilde z_i(t_0)=P(z_i(t_0);\theta)$. **It does not specify the subsequent future.** Future states require an explicit model, such as a known linear ODE or a data-fitted transition model that has been evaluated on held-out data.

## 5. Perturbations

- **Isotropic displacement:** random direction normalized to fixed latent Euclidean magnitude.
- **Axis-specific displacement:** user-defined axis or direction.
- **Empirical residual:** training-data residual sample, scaled by a multiplier.
- **State swap:** donor state selected from another trial, with matching and exchangeability justified.

These are in-silico representational changes, never physical brain interventions.

## 6. Metrics

Reference distance, recovery fraction, time-to-threshold, divergence integral, directional restoration and local trajectory separation. All parameters must specify time windows, reference construction, coordinate scale and failure cases. Positive recovery is descriptive, not proof of an attractor.

## 7. Mathematical validation systems

- Stable linear system: small perturbations decay.
- Unstable system: perturbations exciting unstable modes grow.
- Oscillatory stable system: damped oscillations.
- Two-condition simulation: distinguish known recovery-rate ordering.
- Regression-to-the-mean trap: show misleading apparent recovery after selecting extreme fluctuations.

Use known-answer tests before interpreting participant recordings.

## 8. Null controls

Label permutations, reference time shifts, matched alternative perturbation times, stationary phase-preserving surrogates and reference-trial permutations. Respect conditions, subjects, sampling blocks, autocorrelation and exchangeability. The package cannot select a universally valid null for every study.

## 9. Input and provenance

Canonical array shape: `n_trials × n_features × n_times`; metadata contains `trial_id`, `condition`, `subject`. Preserve sensor units, preprocessing, dataset version, event definitions, sample frequency, channel descriptions, data licensing and participant-level splits. Never commit restricted or identifiable data.

## 10. Project architecture

A modern installable Python package uses `pyproject.toml`, `src/nssl/`, `tests/`, `docs/`, `examples/`, `reproduce/`, generated `assets/`, GitHub workflows, open-source license, citation metadata, changelog, contribution guidelines and a user-facing README.

## 11. Public APIs

See [the implemented API index](api/index.md). Any example in the *original planning document* was conceptual; an experimental propagation and recovery analysis must use the actual interface as implemented and tested. Do not assume an `apply()` operation by itself returns a full future trajectory.

## 12. Software quality gates

Installation, deterministic seeds, mathematical known-answer tests, malformed-input checks, suitable null models, comprehensible beginner documentation, CI, reproducible figures and a credible release process. Test coverage should reflect meaningful scientific failure modes, not vanity metrics.

## 13. Unit testing

For core numerical functions prefer normal-case, shape/type, known-answer and invalid-input tests. Tests should detect errors, rather than assert only that one unvalidated computation agrees with itself.

## 14. GitHub basics

Git manages history and GitHub hosts repositories and automated workflows. Good commits describe actual changes: `Add PCA embedding`, `Fix time-index validation` or `Document EEG event mapping`. Use branches and pull requests for substantial changes. Avoid fictitious activity or meaningless commits.

## 15. Feature branch workflow

Keep main stable, create a short branch for a feature, add tests and documentation, then review the pull request. A clean, justified commit history is more valuable than unnecessary branches.

## 16. Continuous integration

GitHub Actions should test installation, Python compatibility, cross-platform behavior, linting, documentation and deterministic figures. A workflow YAML file alone does not establish that a remote run succeeded; verify real outcomes in the Actions interface.

## 17. Repository README

Explain scientific purpose and audience, core features, diagram, figure, installation, runnable first experiment, interpretation, reproducibility, limitations, author, contributions, license and citation. Avoid large personal biographies or unsupported status badges.

## 18. Hero figure

Include simulated multichannel activity, an illustrative state-space trajectory with mathematical displacement, and stable-versus-unstable model separation. Labels must clearly identify synthetic data and exact model assumptions.

## 19. Documentation

Provide neural state-space concepts, perturbation definitions, reference construction, metrics, statistical controls, experimental design, limitations and tutorials. Define notation and distinguish model forecasts from observed neural responses.

## 20. Reproducibility

Record software versions, random seeds, data provenance, simulation settings, sample units and independent split boundaries. Scripts in `reproduce/` should generate figures from code rather than manual edits to numerical values.

## 21. Benchmarking

Measure fit time, perturbation time and memory across input sizes. Report actual hardware/environment metadata; do not advertise real-time performance without evidence.

## 22. Scientific limitations

Embedding choices, sensor mixing, linearity, representational rather than physical perturbation, selection effects, regression-to-the-mean, reference choice, temporal dependence and model extrapolation all constrain interpretation.

## 23. Security and data

Never commit credentials, API keys, private participant records or restricted datasets. Revoke and rotate exposed secrets rather than only deleting their visible lines.

## 24. Release strategy

Use semantic versions and honest release criteria. A pre-release candidate such as **0.9.0** must not be described as stable 1.0.0 while external EEG, native Windows and independent biological checks remain unfinished.

## 25. Package publication

Publishing to PyPI is optional. Confirm package name availability and build/install behavior before release; a repository's code being public does not mean it has been published on PyPI.

## 26. Development phases

Begin with Git and packaging, then simulation, embedding, perturbations, metrics, null controls, optional public dataset demonstration, documentation and verified release.

## 27. Project strength

A reviewer should be able to understand the research idea, install the package, execute a minimal example, reproduce figures, inspect assumptions and known-answer tests, evaluate limitations and apply the toolkit to compatible arrays. Stars and promotional claims are not scientific-quality measures.

## 28. Acceptance checks

Public repository, README, license, citation, package metadata, source, tests, CI, deterministic known-answer systems, selection-bias controls, real-data tutorial, reproducible figures, docs, changelog, validated installation and accurate limits. A DOI or PyPI release is optional and must never be invented.

## 29. Locked scientific identity

Neural State Space Lab explores recovery and divergence of latent neural-population trajectories using controlled **computational** state changes and explicit evolution models. Separate synthetic simulation from observational analysis and causal interventions.

## 30. Authoritative references

Consult official Python Packaging, GitHub, pytest, MNE-Python and Zenodo documentation for current setup and publication requirements.

---

**Record status:** This file is an edited archival design guide derived from the original project plan. It is *not* intended as evidence that every historical aspiration has been independently validated.
