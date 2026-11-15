# Scientific, statistical, software and privacy limitations

- In-silico perturbation is **not** biological stimulation.
- EEG/MEG sensors record spatially mixed activity, not necessarily localized populations.
- PCA/FA depend on preprocessing, scaling, model choices and input sampling.
- Euclidean distances between independently fitted latent spaces require alignment.
- Distance reductions may result from selection bias, regression to the mean, reference drift and measurement noise.
- Fitted-model rollouts are hypothetical and can accumulate long-horizon prediction errors.
- Missing time-to-recovery crossings are censored, not zero.
- Phase surrogates assume approximate stationarity and can violate event-locked structure.
- Trial permutations and bootstraps must respect participant/session dependence.
- The optional EEG example is single-participant observational analysis, not a perturbation experiment.
- No software component diagnoses disease, consciousness, or safety risk.
- Local tests do not independently validate Windows execution, remote CI, external EEG processing or biology.
