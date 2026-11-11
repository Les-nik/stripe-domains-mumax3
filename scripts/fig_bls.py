"""Brillouin light scattering data (measured by the experimental co-authors).

(a) Saturated state at +4 kOe and -4 kOe: frequencies of the two modes P1, P2.
    Stokes peaks correspond to waves with -k, anti-Stokes peaks to +k.
(b) Frequency difference f(+k) - f(-k) of P1: the non-reciprocity flips sign
    with the field direction.
(c) Stripe phase, k perpendicular to the stripes: three bands.
(d) Stripe phase, k parallel to the stripes: five bands, almost reciprocal.

    python scripts/fig_bls.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from stripe_domains.data import load_bls

ROOT = Path(__file__).resolve().parents[1]


def plus_minus(ax, d, band_key, band, color, label=None):
    m = d[band_key] == band
    k = d["k_rad_per_um"][m]
    ax.errorbar(k, d["f_antistokes_GHz"][m], d["err_antistokes_GHz"][m], fmt="o", ms=3, color=color, label=label)
    ax.errorbar(-k, d["f_stokes_GHz"][m], d["err_stokes_GHz"][m], fmt="o", ms=3, color=color, mfc="none")


def main():
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.4))

    sat = load_bls("saturated_4kOe")
    for field, ls in [(4, "-"), (-4, "--")]:
        for mode, color in [("P1", "tab:blue"), ("P2", "tab:red")]:
            m = (sat["field_kOe"] == field) & (sat["mode"] == mode)
            k = sat["k_rad_per_um"][m]
            f = np.concatenate([sat["f_stokes_GHz"][m][::-1], sat["f_antistokes_GHz"][m]])
            ax[0].plot(np.concatenate([-k[::-1], k]), f, "o", ls=ls, ms=3, color=color,
                       mfc="none" if field < 0 else color, label=f"{mode}, {field:+d} kOe")
            if mode == "P1":
                df = sat["f_antistokes_GHz"][m] - sat["f_stokes_GHz"][m]
                err = np.hypot(sat["err_antistokes_GHz"][m], sat["err_stokes_GHz"][m])
                ax[1].errorbar(k, df, err, fmt="o", ls=ls, ms=3, color=color,
                               mfc="none" if field < 0 else color, label=f"{field:+d} kOe")
    ax[0].set_title("saturated state", fontsize=9)
    ax[0].set_ylabel("frequency (GHz)")
    ax[0].legend(frameon=False, fontsize=7)
    ax[1].axhline(0, color="k", lw=0.5)
    ax[1].set_title(r"P1: $f(+k) - f(-k)$", fontsize=9)
    ax[1].set_ylabel(r"$\Delta f$ (GHz)")
    ax[1].legend(frameon=False, fontsize=8)

    perp = load_bls("stripe_phase_k_perp")
    for b, c in zip([1, 2, 3], ["tab:blue", "tab:orange", "tab:green"]):
        plus_minus(ax[2], perp, "band", b, c, label=f"band {b}")
    ax[2].set_title(r"stripes, $k \perp$ stripes", fontsize=9)
    ax[2].legend(frameon=False, fontsize=8)

    par = load_bls("stripe_phase_k_parallel")
    for b, c in zip(range(1, 6), plt.cm.tab10(np.arange(5))):
        plus_minus(ax[3], par, "band", b, c, label=f"band {b}")
    ax[3].set_title(r"stripes, $k \parallel$ stripes", fontsize=9)
    ax[3].legend(frameon=False, fontsize=7, ncol=2)

    for a, label in zip(ax, "abcd"):
        a.set_xlabel(r"$k$ (rad/$\mu$m)")
        a.text(0.02, 0.95, f"({label})", transform=a.transAxes, va="top")
    fig.text(0.5, 0.005, "(a) filled: +4 kOe, open: -4 kOe.   (c, d) filled: anti-Stokes (+k), open: Stokes (-k)", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    out = ROOT / "figures" / "bls_data.png"
    fig.savefig(out, dpi=200)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
