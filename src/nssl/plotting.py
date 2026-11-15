"""Neon-accented dark scientific figures; never edit measured values in graphics."""
from contextlib import contextmanager
import matplotlib.pyplot as plt

BG = "#070d20"
FG = "#e8f3ff"
GRID = "#263353"
CYAN = "#43e7fb"
PINK = "#ff5ecf"
LIME = "#a1ffbd"

@contextmanager
def neon_style():
    with plt.rc_context({"figure.facecolor": BG, "axes.facecolor": BG,
                         "savefig.facecolor": BG, "text.color": FG,
                         "axes.labelcolor": FG, "axes.edgecolor": GRID,
                         "xtick.color": "#adc3dd", "ytick.color": "#adc3dd",
                         "grid.color": GRID, "font.family": "DejaVu Sans"}):
        yield

def finish_axis(ax, title, xlabel=None, ylabel=None):
    ax.set_title(title, loc="left", fontweight="bold", pad=12, color=FG)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.grid(alpha=.35)
    ax.spines[["top", "right"]].set_visible(False)
    return ax
