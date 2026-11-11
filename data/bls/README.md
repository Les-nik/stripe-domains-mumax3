# BLS data

All frequencies in GHz, wavenumbers in rad/µm. In BLS, the Stokes peak comes from waves with
wavevector -k and the anti-Stokes peak from +k, so `f_stokes` at k is the frequency at -k.

| File | Content |
| --- | --- |
| `saturated_4kOe.csv` | saturated state at +4 kOe and -4 kOe, modes P1 and P2 |
| `stripe_phase_k_perp.csv` | stripe phase, k perpendicular to the stripes, bands 1-3 |
| `stripe_phase_k_parallel.csv` | stripe phase, k parallel to the stripes, bands 1-5 (`angle_deg` is the incidence angle) |

Empty cells are peaks that could not be resolved. `raw/` holds the tables as received
(tab separated, Stokes frequencies with a minus sign); `raw/saturated_5kOe.txt` has three mode
frequencies at 5 kOe.
