# Controlled representational perturbations

Perturbing $z(t_0)$ gives a new initial state $\tilde z(t_0)$, but **not a future trajectory**.

- **Isotropic:** random hypersphere direction normalized to a specified Euclidean magnitude.
- **Axis:** normalized selected axis or user-supplied direction.
- **Empirical residual:** sample centered training residual and scale it; magnitude is a multiplier, not a fixed final norm.
- **State swap:** use caller-selected donor trial indices, with subject/condition matching justified by the researcher.

`PerturbationResult` includes original and changed states, delta, sample time/index and descriptive metadata. Use an explicit dynamics backend for any modeled future behavior. None of these operations stimulates a biological brain.
