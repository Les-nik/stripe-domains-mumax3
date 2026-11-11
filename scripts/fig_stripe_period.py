"""Equilibrium stripe period from the MuMax3 energy scans.

(a) Energy density versus period for a few fields (shifted so each curve's
    minimum is at zero).
(b) Equilibrium period versus in-plane field. Open symbols: the minimum is at
    the edge of the scanned range (100-160 nm), so the true period lies outside it.
(c) Zero-field scans for thinner films (review).

    python scripts/fig_stripe_period.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from stripe_domains.data import DATA, load_mumax_table
from stripe_domains.energy import period_scan

ROOT = Path(__file__).resolve().parents[1]


def main():
    scan = period_scan(load_mumax_table(DATA / "energy" / "energy_vs_period_and_field.txt"))
    period, at_edge = scan.equilibrium()

    fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
    for B, color in zip([0, 100, 200, 300, 380], plt.cm.viridis(np.linspace(0, 0.9, 5))):
        i = np.searchsorted(scan.field_mT, B)
        e = scan.energy[i] - np.nanmin(scan.energy[i])
        ax[0].plot(scan.period_nm, e * 1e-3, color=color, label=f"{B:.0f} mT")
        ax[0].plot(period[i], 0, "o", color=color, ms=4)
    ax[0].set_xlabel("stripe period (nm)")
    ax[0].set_ylabel(r"$\varepsilon - \varepsilon_\mathrm{min}$ (kJ/m$^3$)")
    ax[0].set_ylim(-0.2, 8)
    ax[0].legend(frameon=False, fontsize=8)

    inner = ~at_edge
    ax[1].plot(scan.field_mT[inner], period[inner], "o", color="tab:blue", ms=4, label="minimum inside scan")
    ax[1].plot(scan.field_mT[at_edge], period[at_edge], "o", mfc="none", color="tab:blue", ms=4,
               label="minimum at scan edge")
    ax[1].axhline(138, color="grey", ls="--", lw=0.8)
    ax[1].text(5, 139, "138 nm (dynamic simulations)", fontsize=8, color="grey", va="bottom")
    ax[1].set_xlabel(r"$\mu_0 H$ (mT)")
    ax[1].set_ylabel("equilibrium period (nm)")
    ax[1].legend(frameon=False, fontsize=8)

    for d in (40, 60, 70):
        s = period_scan(load_mumax_table(DATA / "energy" / f"energy_vs_period_B0_d{d}.txt"))
        e = s.energy[0]
        ax[2].plot(s.period_nm, (e - np.nanmin(e)) * 1e-3, "o-", ms=3, label=f"d = {d} nm")
    ax[2].set_xlabel("stripe period (nm)")
    ax[2].set_ylabel(r"$\varepsilon - \varepsilon_\mathrm{min}$ (kJ/m$^3$)")
    ax[2].set_title("zero field, thinner films", fontsize=9)
    ax[2].legend(frameon=False, fontsize=8)

    for a, label in zip(ax, "abc"):
        a.text(0.02, 0.95, f"({label})", transform=a.transAxes, va="top")
    fig.tight_layout()
    out = ROOT / "figures" / "stripe_period.png"
    fig.savefig(out, dpi=200)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
