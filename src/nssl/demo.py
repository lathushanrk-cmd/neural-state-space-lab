"""Reproducible figures from actual known-answer mathematical simulations.
Every graphic clearly states SYNTHETIC; this is NOT an empirical neural result.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from .dynamics import LinearContinuousDynamics
from .simulation import system_matrix, simulate_two_conditions, regression_to_mean_trap
from .statistics import bootstrap_mean_ci
from .plotting import neon_style, finish_axis, BG, FG, GRID, CYAN, PINK, LIME
from .validation import validate_known_systems

def _save(fig, output, stem):
    fig.savefig(output / (stem + ".png"), dpi=175, bbox_inches="tight", facecolor=BG)
    fig.savefig(output / (stem + ".svg"), bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return [output / (stem + ".png"), output / (stem + ".svg")]

def generate(output):
    path = Path(output)
    path.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0, 5, 201)
    rng = np.random.default_rng(42)
    recordings = np.stack([np.sin(2*np.pi*(1+i/8)*t + .5*i) * np.exp(-t*.16) +
                           .17*rng.normal(size=len(t)) for i in range(16)])
    x0, d = np.array([[1., .45]]), np.array([[.6, -.25]])
    roll_stable = LinearContinuousDynamics(system_matrix("stable")).compare(x0, x0+d, t)
    roll_unstable = LinearContinuousDynamics(system_matrix("unstable")).compare(x0, x0+d, t)
    sep_stable = np.linalg.norm(roll_stable.perturbed - roll_stable.baseline, axis=1)[0]
    sep_unstable = np.linalg.norm(roll_unstable.perturbed - roll_unstable.baseline, axis=1)[0]
    files = []
    with neon_style():
        fig = plt.figure(figsize=(15.6, 5.2), layout="constrained")
        fig.suptitle("NEURAL STATE SPACE LAB   /   CONTROLLED PERTURBATION ENGINE", fontsize=20, weight="bold", color=FG)
        gs = fig.add_gridspec(1, 3, wspace=.28)
        a = fig.add_subplot(gs[0, 0]); b = fig.add_subplot(gs[0, 1]); c = fig.add_subplot(gs[0, 2])
        a.imshow(recordings, aspect="auto", origin="lower", extent=[0,5,0,16], cmap="cool", interpolation="none")
        finish_axis(a, "01  /  Population signals", "Time (a.u.)", "Simulated channels")
        base, per = roll_stable.baseline[0], roll_stable.perturbed[0]
        b.plot(base[0], base[1], color=CYAN, lw=2, label="Unperturbed")
        b.plot(per[0], per[1], color=PINK, lw=2, label="Perturbed")
        b.scatter([base[0,0], per[0,0]], [base[1,0], per[1,0]], c=[CYAN,PINK], s=38, zorder=3)
        b.annotate("δ", (per[0,0], per[1,0]), color=FG, xytext=(5,5), textcoords="offset points")
        finish_axis(b, "02  /  Known-system state space", "Dimension 1", "Dimension 2")
        b.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG, fontsize=8)
        c.plot(t, sep_stable, color=CYAN, label="Stable ODE", lw=2)
        c.plot(t, sep_unstable, color=PINK, label="Unstable ODE", lw=2)
        c.set_yscale("log")
        finish_axis(c, "03  /  Trajectory separation", "Time (a.u.)", "Euclidean distance (log)")
        c.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG, fontsize=8)
        fig.text(.5, -.03, "SYNTHETIC EXAMPLE  •  exact linear ODE propagation  •  no empirical neural claims", ha="center", color="#a8bdd5", fontsize=10)
        files += _save(fig, path, "hero_simulation")

        fig, ax = plt.subplots(figsize=(10, 5.1), layout="constrained")
        two = simulate_two_conditions(random_state=42)
        for j, color in enumerate((CYAN,PINK)):
            distances = np.linalg.norm(two["data"][j], axis=1)
            mean = distances.mean(axis=0)
            se = distances.std(axis=0, ddof=1) / np.sqrt(len(distances))
            ax.plot(two["times"], mean, lw=2.3, color=color, label=f'{two["condition_names"][j]} (true rate {two["rates"][j]:.1f})')
            ax.fill_between(two["times"], mean-se, mean+se, color=color, alpha=.16)
        finish_axis(ax, "Recovery behavior in two simulated stable systems", "Time (a.u.)", "Distance to equilibrium")
        ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG)
        ax.text(.01, -.20, "SYNTHETIC DATA  •  shaded bands = SEM across simulated trials", transform=ax.transAxes, color="#a8bdd5")
        files += _save(fig, path, "two_condition_simulation")

        trap = regression_to_mean_trap(random_state=42)
        fig, ax = plt.subplots(figsize=(10,5), layout="constrained")
        selected = trap["series"][trap["selected"]]
        idx = trap["index"]
        centers = np.mean(np.abs(selected[:, idx-5:idx+12]), axis=0)
        ax.plot(np.arange(-5,12), centers, lw=2.7, color=PINK, marker="o", ms=3)
        ax.axvline(0, color=LIME, ls="--", alpha=.8, label="Selected unusually large deviation")
        finish_axis(ax, "Regression-to-the-mean trap / stationary AR(1)", "Sample relative to selection", "Mean absolute deviation")
        ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG)
        ax.text(.01, -.20, "SYNTHETIC STOCHASTIC SERIES  •  apparent recovery is NOT evidence of a biological attractor", transform=ax.transAxes, color="#a8bdd5")
        files += _save(fig, path, "regression_to_mean_trap")

        fig, ax = plt.subplots(figsize=(10,5), layout="constrained")
        for kind, color in (("stable",CYAN),("unstable",PINK),("oscillatory",LIME)):
            model = LinearContinuousDynamics(system_matrix(kind))
            xx = model.rollout(np.array([[1., 0.]]), t)[0]
            ax.plot(xx[0], xx[1], color=color, lw=2, label=kind.capitalize())
            ax.scatter(xx[0,0], xx[1,0], c=color, s=32, marker="o")
        finish_axis(ax, "Ground-truth state-space trajectories", "Dimension 1", "Dimension 2")
        ax.legend(facecolor=BG, edgecolor=GRID, labelcolor=FG)
        ax.text(.01, -.19, "SYNTHETIC EXAMPLE  •  analytically specified ODE systems", transform=ax.transAxes, color="#a8bdd5")
        files += _save(fig, path, "phase_portraits")

    result = {"source": "exact known-system ODE and seeded synthetic processes", "seed": 42,
              "known_system_checks": validate_known_systems(),
              "stable_initial_separation": float(sep_stable[0]),
              "stable_final_separation": float(sep_stable[-1]),
              "unstable_initial_separation": float(sep_unstable[0]),
              "unstable_final_separation": float(sep_unstable[-1]),
              "regression_to_mean_selected_trials": int(trap["selected"].sum()),
              "regression_to_mean_average_naive_fraction": trap["mean_apparent_recovery"],
              "interpretation": "numerical demonstration only; no biological result"}
    result_path = path / "simulation_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return files + [result_path]
