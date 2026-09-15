# Replacement spinner wheel — design notes

Replacement for a failed Ø50 × 19 mm dual-wheel spinner wheel (Rimowa-style
knockoff). Original was a one-piece PU-over-plastic wheel running directly on
the axle with a plain plastic bore; the bore wore out.

![cross-section](cross_section.png)

## Architecture

| Part | Material | Made by | Qty / wheel |
|---|---|---|---|
| Hub | Al 6061-T6 | outsourced CNC (pure turned part) | 1 |
| Bearing | 608-2RS (8×22×7) | purchased | 2 |
| Spacer | Al or printed | outsourced / FDM | 1 |
| Tire | TPU 95A | FDM | 1 |
| Speed rings / shims | steel 8×12×0.5 | purchased (skateboard "speed rings") | 0–2 as needed |

Everything is parametrised in [`cad/params.py`](../cad/params.py); regenerate
with `uv run cad/generate.py`.

## Why two bearings

In a dual-wheel spinner each wheel is cantilevered on a stub axle. A single
bearing would let the wheel rock on the axle under side load (which is what
killed the plastic bore). Two bearings, one at each face, give a 12 mm span
between bearing centres and turn the rocking load into a simple radial couple.
Load-wise a 608 is absurdly over-rated for this (Cr ≈ 3.3 kN each, a wheel
sees < 150 N), so the choice is driven purely by geometry and price.

## Bearing selection

Assumption: **Ø8 mm axle** → 608. Confirm by measuring the axle. Alternatives
are in the `BEARINGS` table in `params.py`; changing `BEARING = "626"` (Ø6
axle) regenerates everything. Use **2RS** (rubber sealed) variants — the wheel
lives at ankle height in grit and rain.

SKF abutment limits for 608: housing shoulder ≤ Ø20.4, shaft shoulder ≥ Ø9.6.
Design uses Ø20.0 shoulder and Ø11 spacer.

## Tolerances for the machinist

The hub is a lathe-only part. Callouts that matter:

| Feature | Nominal | Tolerance | Why |
|---|---|---|---|
| Bearing bore (×2) | Ø22.00 | **−0.010 / −0.020** (i.e. Ø21.98–21.99) | light press fit for a 608 (OD 22 h0/−0.008). Bearing goes in with a vise or arbor press, no retaining compound needed. |
| Bore concentricity, both ends | — | ≤ 0.02 TIR | both bearings must share an axis or the wheel binds |
| Shoulder Ø20 | Ø20.0 | ±0.1 | non-critical, just clears the seal |
| Shoulder width | 5.00 | ±0.05 | sets bearing spacing; spacer is matched |
| Hub width (face to face) | 19.00 | ±0.05 | sets clearance to housing/cap |
| Ø38 / Ø36 | — | ±0.1 | tire is stretch-fit, forgiving |
| Chamfers | 0.5 × 45° | — | bore chamfer is the press lead-in, don't omit |

Finish: as-machined is fine. Anodise optional (looks good, no functional need).

If the shop asks for a drawing rather than "STEP + this table", the table above
is the drawing.

## Spacer

Tube Ø11 / Ø8.2 × 5.00 between the inner races. Its length must equal the
shoulder width to within ±0.05 so that clamping the axle cap loads the two
inner races against each other through the spacer and **not** the outer races
through the shoulder. Printed PETG works for testing; order it in aluminium
with the hubs for the final build — it's a trivial add to the CNC order.

## Bearing faces vs housing

Only the **inner** races may touch the housing boss and the axle cap. If the
existing axle shoulder or cap head is larger than ~Ø12, drop an 8×12×0.5
skateboard speed ring on each side so the outer race and hub face have
clearance. Check this before final assembly by spinning the wheel with the cap
torqued down: if it drags, it needs a ring.

## Tire

- TPU 95A (e.g. NinjaFlex Cheetah, Polymaker TPU95, Overture TPU). Softer
  (85A) rolls quieter but wears faster and prints worse.
- Modelled **1.5 % undersize** on the ID so it stretches onto the Ø36 bed and
  snaps over the Ø38 flanges. It has to be stretched over a Ø38 flange to
  install (≈ 7 % strain at the lip) — trivial for TPU. Warm water helps.
- Two flanges capture it axially; friction + stretch handle torque. If it ever
  creeps, a thin smear of CA on the bed fixes it permanently.
- Print orientation: **flat on its side** (axis vertical), so layer lines run
  circumferentially — that's the quiet orientation and the strong one.
- Print settings that matter: 100 % infill (or ≥ 4 walls + gyroid ≥ 40 %),
  slow (20–30 mm/s), retraction minimal, dry filament. Tread will be slightly
  slick when new; it scuffs in.
- Minimum wall is 6 mm over the flange. Below ~4 mm TPU starts to feel like
  riding on the aluminium.

## Prototype sequence

1. Print `hub_proto.stl` in PLA (0.12 mm layers, 100 % infill) and `tire.stl`
   in TPU. Bore will come out slightly undersize on FDM — ream/scrape until a
   608 pushes in by hand. This is a **fit and envelope check only**.
2. Fit two bearings + spacer, mount on the case, spin, check clearance to the
   housing and whether speed rings are needed.
3. Adjust `params.py` (axle diameter, width, clearances) → regenerate.
4. Send `hub.step` + `spacer.step` + the tolerance table to a CNC shop. Order
   `WHEELS_TOTAL` (8) hubs if replacing all corners; the per-part price drops
   steeply with quantity and the other seven wheels will fail the same way.
5. Print 8 tires (~20 g TPU each), press bearings, fit tires, install.

## Open questions

- [ ] **Axle diameter** — 8 mm assumed. Measure.
- [ ] Axle retention: screw (what thread/head?) or rivet (needs drilling out
      and replacing with an M-screw + nyloc or a shoulder bolt).
- [ ] Stub axle length and boss diameter at the housing → decides speed rings.
- [ ] Gap between wheel inner face and housing when installed (need ≥ 0.5 mm).
- [ ] Replace one wheel or all eight?
