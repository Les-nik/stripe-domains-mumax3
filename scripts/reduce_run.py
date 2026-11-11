"""Turn a MuMax3 output folder (several GB) into a small .npz for this repository.

Run it where the simulation output is:

    pip install git+https://github.com/Les-nik/spin-wave-dispersion
    python scripts/reduce_run.py path/to/stripes_k_perp.out stripes_k_perp

It reads every snapshot (one component, averaged over the periodic direction),
computes the dispersion with ``swdispersion`` and keeps only the part that
the figures show. The result goes to ``data/simulations/<name>.npz``:

    f, k, amplitude   dispersion, cropped to f < fmax and |k| < kmax
    m_static          (3, nz, nx) static magnetization from m_stab.ovf, if present
    dx, dz            cell sizes
"""

import argparse
from pathlib import Path

import numpy as np
from swdispersion import compute_dispersion, load_series, read_ovf

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run", type=Path)
    p.add_argument("name")
    p.add_argument("--component", default="z")
    p.add_argument("--along", default="x", choices="xy",
                   help="direction of k: x (stripes_k_perp, saturated) or y (stripes_k_parallel)")
    p.add_argument("--fmax", type=float, default=30.0, help="GHz")
    p.add_argument("--kmax", type=float, default=60.0, help="rad/um")
    args = p.parse_args()

    if args.along == "x":
        series = load_series(args.run, component=args.component, average_y=True)
        data, dk_cell = series.data, series.dx                    # (t, z, x)
    else:
        # k along y: average over x instead, keep (t, z, y).
        series = load_series(args.run, component=args.component, average_y=False)
        data, dk_cell = series.data.mean(axis=3), series.dy       # (t, z, y)
    print(f"{len(series.t)} snapshots, dt = {series.dt:.3e} s, data {data.shape}")

    disp = compute_dispersion(data, series.dt, dk_cell)
    fm = disp.f <= args.fmax * 1e9
    km = np.abs(disp.k) <= args.kmax * 1e6
    out = dict(f=disp.f[fm], k=disp.k[km], amplitude=disp.amplitude[np.ix_(fm, km)].astype(np.float32),
               dx=series.dx, dy=series.dy, dz=series.dz, along=args.along, component=args.component)

    stab = args.run / "m_stab.ovf"
    if stab.exists():
        m, _ = read_ovf(stab)                                     # (z, y, x, 3)
        out["m_static"] = np.moveaxis(m.mean(axis=1), -1, 0).astype(np.float32)

    target = ROOT / "data" / "simulations" / f"{args.name}.npz"
    target.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(target, **out)
    print(f"saved {target} ({target.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
