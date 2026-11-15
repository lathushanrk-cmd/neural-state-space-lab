# Neural State Space Lab

NSSL is an open-source Python research-software toolkit for simulated and observational neural population state spaces. Start at [the README](../README.md), [concepts](concepts.md), [dynamics](dynamics.md), and [limitations](limitations.md).

## Three experimental modes

1. **Observational:** compute time-dependent trajectory measures from recorded states and held-out references.
2. **Known-system:** propagate controlled displacements in a specified mathematical dynamical system.
3. **Model-dependent:** fit a transition model on training trials and roll forward hypothetical displaced states after held-out checks.

Neither observation nor computational perturbation establishes in-vivo causality.
