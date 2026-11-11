"""Loaders for the files in ``data/``."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1] / "data"


def load_bls(name: str) -> dict[str, np.ndarray]:
    """One of the CSV files in data/bls as a dict of columns (empty cells become NaN)."""
    with open(DATA / "bls" / f"{name}.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for key in rows[0]:
        values = [r[key] for r in rows]
        try:
            out[key] = np.array([float(v) if v != "" else np.nan for v in values])
        except ValueError:
            out[key] = np.array(values)
    return out


def load_mumax_table(path: str | Path) -> dict[str, np.ndarray]:
    """A MuMax3 table.txt as {column name: values}. Units are dropped from the names."""
    path = Path(path)
    with open(path) as f:
        header = f.readline().lstrip("#").strip().split("\t")
    names = [h.split("(")[0].strip() for h in header]
    values = np.loadtxt(path, comments="#", ndmin=2)
    return {n: values[:, i] for i, n in enumerate(names)}
