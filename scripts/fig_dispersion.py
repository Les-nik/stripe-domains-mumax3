"""Simulated dispersions with the BLS points on top.

Needs the reduced simulation files in data/simulations (see scripts/reduce_run.py):
stripes_k_perp.npz, stripes_k_parallel.npz, saturated.npz. Panels whose file is
missing are left empty.

    python scripts/fig_dispersion.py
"""

from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from stripe_domains.data import DATA, load_bls

ROOT = Path(__file__).resolve().parents[1]
PANELS = [
    ("saturated", "saturated, 500 mT", None),
    ("stripes_k_perp", r"stripes, $k \perp$ stripes", "stripe_phase_k_perp"),
    ("stripes_k_parallel", r"stripes, $k \parallel$ stripes", "stripe_phase_k_parallel"),
]


def main():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, (name, title, bls) in zip(axes, PANELS):
        path = DATA / "simulations" / f"{name}.npz"
        ax.set_title(title, fontsize=9)
        ax.set_xlabel(r"$k$ (rad/$\mu$m)")
        if not path.exists():
            ax.text(0.5, 0.5, f"missing {path.name}\n(scripts/reduce_run.py)", ha="center",
                    va="center", transform=ax.transAxes, fontsize=8)
            continue
        d = np.load(path)
        amp = d["amplitude"]
        ax.pcolormesh(d["k"] * 1e-6, d["f"] * 1e-9, amp, shading="nearest", cmap="YlOrBr",
                      norm=mcolors.LogNorm(amp.max() * 1e-3, amp.max()), rasterized=True)
        if bls:
            b = load_bls(bls)
            ax.plot(b["k_rad_per_um"], b["f_antistokes_GHz"], "o", ms=3, mfc="none", mec="k")
            ax.plot(-b["k_rad_per_um"], b["f_stokes_GHz"], "o", ms=3, mfc="none", mec="k")
        ax.set_xlim(-30, 30)
    axes[0].set_ylabel("frequency (GHz)")
    fig.tight_layout()
    out = ROOT / "figures" / "dispersions.png"
    fig.savefig(out, dpi=200)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
