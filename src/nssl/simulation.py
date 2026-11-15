"""Synthetic known-answer systems: outputs are SIMULATED, not neural findings."""
import numpy as np
from .dynamics import LinearContinuousDynamics

def system_matrix(kind="stable", rate=0.8, frequency=3.0):
    if not np.isfinite(rate) or rate <= 0 or not np.isfinite(frequency):
        raise ValueError("rate must be positive and parameters finite")
    if kind == "stable":
        return np.diag([-rate, -rate * 1.5])
    if kind == "unstable":
        return np.diag([rate, -rate])
    if kind == "oscillatory":
        return np.array([[-rate, -frequency], [frequency, -rate]], float)
    raise ValueError("unknown simulation system")

def simulate_linear(kind="stable", *, times=None, n_trials=24, random_state=42, noise=0.0):
    if n_trials < 2 or noise < 0 or not np.isfinite(noise):
        raise ValueError("invalid simulation parameters")
    t = np.linspace(0, 5, 201) if times is None else np.asarray(times, float)
    rng = np.random.default_rng(random_state)
    x0 = rng.normal(size=(n_trials, 2))
    base = LinearContinuousDynamics(system_matrix(kind)).rollout(x0, t)
    observed = base + rng.normal(0, noise, size=base.shape)
    return {"data": observed, "truth": base, "times": t, "A": system_matrix(kind), "initial": x0, "kind": kind}

def simulate_two_conditions(*, rates=(1.2, 0.3), n_trials=30, times=None, random_state=42, noise=0.03):
    if len(rates) != 2 or min(rates) <= 0:
        raise ValueError("two positive recovery rates required")
    t = np.linspace(0, 5, 201) if times is None else np.asarray(times, float)
    rng = np.random.default_rng(random_state)
    initial = rng.normal(loc=1.0, scale=0.1, size=(2, n_trials, 2))
    series = np.stack([LinearContinuousDynamics(np.diag([-rate, -rate])).rollout(initial[j], t)
                       for j, rate in enumerate(rates)])
    return {"data": series + rng.normal(0, noise, size=series.shape), "truth": series,
            "times": t, "rates": rates, "condition_names": ["fast", "slow"]}

def regression_to_mean_trap(*, n_trials=300, n_times=90, rho=0.75, random_state=42):
    """Stationary AR(1) WITHOUT a restorative neural potential."""
    if n_trials < 10 or n_times < 5 or not -1 < rho < 1:
        raise ValueError("invalid AR(1) parameters")
    rng = np.random.default_rng(random_state)
    x = np.zeros((n_trials, n_times))
    x[:, 0] = rng.normal(size=n_trials)
    for j in range(1, n_times):
        x[:, j] = rho * x[:, j-1] + np.sqrt(1 - rho**2) * rng.normal(size=n_trials)
    middle = n_times // 2
    selected = np.abs(x[:, middle]) >= np.quantile(np.abs(x[:, middle]), .8)
    dist_initial = np.abs(x[selected, middle])
    dist_later = np.abs(x[selected, middle + 3])
    apparent = (dist_initial - dist_later) / (dist_initial + 1e-12)
    return {"series": x, "selected": selected, "index": middle, "apparent_recovery": apparent,
            "mean_apparent_recovery": float(apparent.mean()), "description": "stationary AR(1) conditional selection artifact"}
