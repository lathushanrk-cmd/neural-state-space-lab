"""Simple known-answer numerical assertions for simulation backends."""
import numpy as np
from .simulation import system_matrix
from .dynamics import LinearContinuousDynamics

def validate_known_systems():
    t = np.linspace(0, 6, 121)
    x0 = np.array([[1., 0.]])
    displacement = np.array([[0.4, 0.]])
    out = {}
    for kind in ("stable", "unstable", "oscillatory"):
        roll = LinearContinuousDynamics(system_matrix(kind)).compare(x0, x0 + displacement, t)
        sep = np.linalg.norm(roll.perturbed - roll.baseline, axis=1)[0]
        out[kind] = {"initial_separation": float(sep[0]), "final_separation": float(sep[-1]),
                     "expected": "decay" if kind != "unstable" else "growth"}
        if kind == "unstable" and not sep[-1] > sep[0]:
            raise AssertionError("unstable system did not grow")
        if kind != "unstable" and not sep[-1] < sep[0]:
            raise AssertionError("stable system did not decay")
    return out
