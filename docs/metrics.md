# Metrics and interpretation

For trial trajectory $z_i(t)$ and reference $\mu_c(t)$, define $D_i(t)=\lVert z_i(t)-\mu_c(t)\rVert_2$.

1. **Distance:** Euclidean reference distance in consistent latent units.
2. **Recovery fraction:** $(D(t_0)-D(t_0+\Delta))/(D(t_0)+\epsilon)$. A positive fraction only indicates a decrease over that horizon.
3. **Time-to-recovery:** first post-initial threshold crossing, optionally requiring consecutive samples. `NaN` means no observed crossing (censored).
4. **Divergence integral:** trapezoidal integral of distance over time.
5. **Directional restoration:** cosine between trajectory velocity and the direction toward reference; undefined for zero norms.
6. **Local separation:** Euclidean separation between matched perturbed and baseline trajectories.

A descriptive metric alone does not demonstrate a biological attractor or causal response.
