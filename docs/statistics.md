# Statistical procedures

`bootstrap_mean_ci(values, confidence=.95, n_boot=2000, groups=None, random_state=42)` returns a percentile bootstrap interval. Without groups, individual observations are resampled. With groups, group means are resampled with equal weight per group, changing the estimand to the average of group means.

`permutation_pvalue(observed, null_statistics, alternative="two-sided", center=0)` computes the add-one empirical probability: `(extreme+1)/(n_null+1)`. The null distribution is only valid when its permutation design matches the scientific hypothesis and dependence structure.

Neither function automatically corrects multiple testing, supports causal conclusions, or guarantees valid inference for complex hierarchical neuroscience data.
