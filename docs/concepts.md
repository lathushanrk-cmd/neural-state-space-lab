# Neural state-space concepts

For a multichannel trial, the population state is $x(t) \in \mathbb{R}^{p}$, where $p$ is the count of sensors/neurons/parcels/features. A dimensionality-reduction mapping $f$ transforms it to $z(t) = f(x(t)) \in \mathbb{R}^{k}$, normally with $k < p$. The sequence $z(t)$ is a latent trajectory. The axes are model-defined coordinates, not necessarily anatomical brain coordinates.

NSSL data arrays have shape `(n_trials, n_features, n_times)`; `times` must be strictly increasing and metadata must contain `trial_id`, `condition`, `subject`. EEG/MEG sensor units must be documented. Heterogeneous units may require modality-specific preprocessing before Euclidean distances.

A **reference trajectory** $\mu_c(t)$ denotes a condition-specific trajectory estimated only from training trials, or by explicit leave-one-out estimation. Recovery toward $\mu_c$ is descriptive unless a separate dynamical mechanism has been verified.

Low-dimensional Euclidean metrics depend on scaling, whitening and embedding choices; check robustness to preprocessing.
