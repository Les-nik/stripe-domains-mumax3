import numpy as np

from stripe_domains.data import DATA, load_bls, load_mumax_table
from stripe_domains.energy import period_scan


def test_energy_scan_grid():
    scan = period_scan(load_mumax_table(DATA / "energy" / "energy_vs_period_and_field.txt"))
    assert scan.energy.shape == (77, 31)
    assert not np.isnan(scan.energy).any()
    assert scan.period_nm[0] == 100 and scan.period_nm[-1] == 160


def test_period_shrinks_with_field():
    scan = period_scan(load_mumax_table(DATA / "energy" / "energy_vs_period_and_field.txt"))
    period, at_edge = scan.equilibrium()
    inner = period[~at_edge]
    assert np.all(np.diff(inner) <= 0)  # an in-plane field shortens the stripes
    assert at_edge[0]  # at zero field the minimum lies beyond the scanned 160 nm


def test_zero_field_scan_has_no_field_column():
    scan = period_scan(load_mumax_table(DATA / "energy" / "energy_vs_period_B0_d40.txt"))
    assert scan.energy.shape[0] == 1


def test_bls_tables():
    perp = load_bls("stripe_phase_k_perp")
    assert set(perp["band"]) == {1.0, 2.0, 3.0}
    assert np.isnan(perp["f_antistokes_GHz"]).sum() == 1  # one peak not resolved
    sat = load_bls("saturated_4kOe")
    m = (sat["field_kOe"] == 4) & (sat["mode"] == "P1")
    df = sat["f_antistokes_GHz"][m] - sat["f_stokes_GHz"][m]
    assert np.all(df < 0)  # non-reciprocal, sign set by the field direction
