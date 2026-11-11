"""Equilibrium stripe period from an energy scan.

``simulations/energy_minimum_vs_field.mx3`` relaxes one stripe period of
``nx`` cells for a range of periods and fields and records the total energy
density. For a fixed field, the period with the lowest energy density is the
equilibrium one. A minimum at the first or last period of the scan only says
that the true minimum lies outside the scanned range, so those points are
flagged.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class PeriodScan:
    field_mT: np.ndarray      # (n_fields,)
    period_nm: np.ndarray     # (n_periods,)
    energy: np.ndarray        # (n_fields, n_periods), J/m^3

    def equilibrium(self):
        """Period of minimum energy for each field, and a flag for minima at the scan edge."""
        idx = np.argmin(self.energy, axis=1)
        at_edge = (idx == 0) | (idx == self.period_nm.size - 1)
        return self.period_nm[idx], at_edge


def period_scan(table: dict, cell_nm: float = 2.0, field_key: str = "B0",
                nx_key: str = "nx", energy_key: str = "Edens_total") -> PeriodScan:
    """Arrange the rows of a MuMax3 table (one row per field and period) on a grid."""
    nx = table[nx_key]
    # Zero-field scans have no field column.
    B = table[field_key] if field_key in table else np.zeros_like(nx)
    E = table[energy_key]
    fields = np.unique(B)
    nxs = np.unique(nx)
    grid = np.full((fields.size, nxs.size), np.nan)
    for b, n, e in zip(B, nx, E):
        grid[np.searchsorted(fields, b), np.searchsorted(nxs, n)] = e
    return PeriodScan(field_mT=fields, period_nm=nxs * cell_nm, energy=grid)
