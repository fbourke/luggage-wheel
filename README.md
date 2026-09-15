# luggage-wheel

Replacement Ø50 × 19 mm dual-spinner wheel for Rimowa-style luggage:
CNC aluminium hub, twin 608 bearings, 3D-printed TPU tire.
The original wheel failed at its plain plastic bore.

![cross-section](docs/cross_section.png)

- [`docs/design.md`](docs/design.md) — design rationale, bearing selection, machinist tolerances, print settings, open questions
- [`bom.md`](bom.md) — parts, quantities, sources
- [`cad/params.py`](cad/params.py) — every dimension, single source of truth
- [`cad/generate.py`](cad/generate.py) — build123d model → `export/*.step`, `export/*.stl`
- [`cad/preview.py`](cad/preview.py) — cross-section PNG

## Regenerate

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```sh
uv run cad/generate.py   # STEP + STL into export/
uv run cad/preview.py    # docs/cross_section.png
```

## Outputs

| File | Use |
|---|---|
| `export/hub.step`, `export/spacer.step` | send to CNC shop with the tolerance table in `docs/design.md` |
| `export/tire.stl` | print in TPU 95A, on its side, 100 % infill |
| `export/hub_proto.stl` | PLA fit-check before ordering metal |
| `export/wheel_assembly.step` | full assembly with dummy bearings, for viewing |

STL files are not committed (regenerate them); STEP files are.
