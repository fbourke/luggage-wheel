# luggage-wheel

Replacement dual-wheel spinner carriage for Rimowa-style luggage: CNC
aluminium body swivelling on the case's Ø10 shaft (needle thrust bearing +
Oilite bushing) and a through-axle carrying two wheels. The original wheels
ran on plain plastic bores and wore out.

Two wheel variants share the body (`WHEEL_SOURCE` env var, default `ots`):
**`ots`** uses bought Ø50 × 12 PU luggage wheels on a Ø6 axle (see
[`docs/wheel_sourcing.md`](docs/wheel_sourcing.md)); **`machined`** is our
turned Al hub on 688 bearings with printed TPU tires, kept as a fallback.

![carriage](docs/carriage_views.png)

- [`docs/design.md`](docs/design.md) — envelope, swivel, axle, machinist tolerances, print settings, open questions
- [`docs/wheel_sourcing.md`](docs/wheel_sourcing.md) — off-the-shelf wheel research (Floyd, generic 50×12, Rimowa OEM…)
- [`bom.md`](bom.md) — parts, quantities, sources
- [`cad/params.py`](cad/params.py) — every dimension, single source of truth
- [`cad/wheel.py`](cad/wheel.py), [`cad/carriage.py`](cad/carriage.py) — build123d models
- [`cad/generate.py`](cad/generate.py) — exports + clearance report
- [`cad/preview.py`](cad/preview.py), [`cad/views.py`](cad/views.py) — PNG renders

## Regenerate

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```sh
uv run cad/generate.py                        # ots: STEP + STL into export/, clearance report
uv run cad/views.py                           # docs/carriage_views.png
WHEEL_SOURCE=machined uv run cad/generate.py  # fallback variant into export/machined/
WHEEL_SOURCE=machined uv run cad/views.py     # docs/carriage_views_machined.png
uv run cad/preview.py                         # docs/cross_section.png (machined wheel)
```

## Outputs

| File | Use |
|---|---|
| `export/body.step`, `axle_pin.step`, `ots_spacer.step` | to the CNC shop, with the tolerance tables in `docs/design.md` |
| `export/ots_wheel_ref.step` | dummy of the bought wheel, for reference |
| `export/carriage_fit_proto.stl` | **one-piece printed fit-check**: body + thrust collar + solid wheels; screws straight onto the case with the existing M5 bolt |
| `export/body_proto.stl` | printed body for bushing/axle fit checks |
| `export/carriage_assembly.step` | full assembly with dummy wheels, for viewing |
| `export/machined/…` | the same set for the machined-wheel variant, plus `hub.step`, `spacer.step`, `tire.step`/`.stl`, `wheel_assembly.step` |

STL files are not committed (regenerate them); STEP files are.

## Status

Envelope fully measured; a printed one-piece proto **fits the recess, pivots
freely and matches the OEM ride height**. Direction is now bought Ø50 × 12
wheels on the machined body. Next: buy a pack, measure them, print
`body_proto.stl`, then order metal. Open questions are in `docs/design.md`.
