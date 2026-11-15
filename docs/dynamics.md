# Dynamics and trajectory propagation

## Known-system exact linear dynamics

For $\dot z(t)=Az(t)$, NSSL calculates $z(t)=\exp(A(t-t_0))z(t_0)$. `LinearContinuousDynamics(A)` requires finite square A. `compare(original, displaced, times)` propagates both from a shared origin. Negative real eigenvalue parts imply asymptotic stability; positive-real-part modes may cause growth when excited.

Three 2D canonical systems are included: stable diagonal, unstable diagonal, damped rotation. They are mathematical simulations, not individualized neural biophysics.

## Fitted linear transition

`RegularizedLinearDynamics(alpha)` fits $z_{t+1}=Wz_t+b$ using ridge regression on training trials. Sampling intervals must be uniform. `evaluate_one_step(Z_holdout)` compares predictive error against persistence on held-out trials. Good one-step predictions do not guarantee reliable long-horizon forecasts or causal interpretation.

An edited state alone does not determine a future path: the propagation model must be explicit. A predicted trajectory is not an actual participant's response to brain stimulation.
