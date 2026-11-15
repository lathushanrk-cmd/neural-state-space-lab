# Null models and validity

| Function | Question | Caution |
|---|---|---|
| `permute_trial_labels` | Is there a condition–label association? | Respect independent exchangeability blocks |
| `shift_reference` | Does time alignment matter? | Circular shifts can violate event structure |
| `random_times` | Is chosen timing special? | Match margins and selection criteria |
| `phase_randomized_surrogate` | Is an effect explainable by stationary spectra? | Shared phases preserve cross spectra, not event-locking |
| `permute_reference_trials` | Are matched trial references informative? | Restrict to valid groups |

AR(1) regression-to-the-mean simulations show apparent recovery after extreme selections without any neuronal restoration mechanism. Valid null p-values depend on sampling unit, autocorrelation and preregistered hypothesis.
