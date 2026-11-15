# Tutorial 2 — Regression to the mean

```python
from nssl.simulation import regression_to_mean_trap
trial = regression_to_mean_trap(random_state=42)
print(trial["mean_apparent_recovery"])
```

These are stationary synthetic AR(1) sequences. Selecting unusually large absolute values at a chosen instant produces an apparent reduction later. A positive naive recovery fraction is not sufficient evidence of a biological attractor.

For a figure run `python reproduce/figure_2.py` and examine `assets/regression_to_mean_trap.png`.
