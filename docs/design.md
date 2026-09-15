# Replacement spinner carriage — design notes

Replacement for a failed dual-wheel spinner carriage (Rimowa-style knockoff):
the whole unit that bolts onto the case's Ø10 swivel shaft and carries two
Ø50 × 19 mm wheels. The original's wheels ran on plain plastic bores, which
wore out.

![carriage](carriage_views.png)

## Architecture

| Part | Material | Made by | Qty / carriage |
|---|---|---|---|
| Body | Al 6061-T6 | outsourced CNC (3-axis milled) | 1 |
| Axle pin | Ø8 h6 ground steel shaft, 63.4 long, 2 circlip grooves | cut + grooved, or CNC order | 1 |
| Circlip | DIN 471 Ø8 | purchased | 2 |
| Hub | Al 6061-T6 | outsourced CNC (pure turned part) | 2 |
| Wheel bearing | 608-2RS (8×22×7) | purchased | 4 |
| Bearing spacer | Al or printed | same CNC order / FDM | 2 |
| Speed rings | steel 8×12×0.5 | skateboard "speed rings" | 4 |
| Tire | TPU 95A | FDM | 2 |
| Swivel thrust bearing | AXK1024 needle thrust + 2× AS1024 washers | purchased | 1 set |
| Swivel bushing | Oilite SAE 841, 10×12×15 | purchased | 1 |
| Retention washer | nylon 10×14×1 | purchased | 1 |
| Retention bolt | existing (thread TBD) | reuse | 1 |

Everything is parametrised in [`cad/params.py`](../cad/params.py); regenerate
with `uv run cad/generate.py`.

## Coordinate frame

`X` fore/aft with the shaft axis at X = 0 and the wheels at X = +18.1 (trail);
`Y` across; `Z` up with **Z = 0 at the case bottom skin**, floor at Z = −53.5.

## Envelope — why the body looks the way it does

The case sits 53.5 mm above the floor on Ø50 wheels, so **the wheel top is only
3.5 mm below the case skin** and the axle is 28.5 mm down. Consequences:

- Nothing can sit above the wheels. The body is an **18 mm neck** between
  them (wheel gap 19 − 2 × 0.5) from the swivel back to a rounded boss around
  the axle.
- The shaft is 18.1 mm ahead of the axle, and at the shaft axis the wheel only
  exists between Z ≈ −11 and −46. So a **34 mm wide head** can live in front
  of the wheels, from the top face down to Z = −20, with its rear sculpted to a
  cylinder 1.5 mm outside the tire. It ends at X = +4 with a 2 mm thick edge
  rather than running out to a knife edge.
- The head is deliberately deep enough to enclose the whole 15 mm bushing —
  that's where the tilting moment from the trailing wheels goes.

`generate.py` prints an analytic clearance report (thrust washer ↔ tire, neck
↔ tire, body ↔ floor, counterbore wall). Check it after every parameter change.

## Swivel

The Ø10 shaft is fixed to the case; the body rotates on it and the case's
weight bears on a plastic shoulder molded around the shaft.

**Thrust — AXK1024 needle roller thrust bearing (10×24×2) between two AS1024
hardened washers (10×24×1)**, 4 mm total, between the plastic shoulder and the
body's top face. The upper washer is stationary against the plastic, the lower
one turns with the body, needles between. The hardened Ø24 washer also spreads
the load on the plastic far better than the old body did.

**Radial — Oilite bronze sleeve bushing 10×12×15**, pressed into a Ø12 H7 bore
from the top, flush with the top face. A swivel turns a few degrees at near
zero speed under moderate load: that is textbook sintered-bronze territory, and
no ball bearing with a Ø10 bore fits inside an 18 mm neck anyway (6800 is
Ø19 OD). Shaft finish matters more than the bushing: if the shaft is rough or
plated-and-chipped, polish it.

**Retention** — the existing bolt threads into the shaft end and lives in a
Ø15 counterbore from below, with a nylon 10×14×1 washer between the bolt head
and the counterbore ceiling. The ceiling is placed at
`shaft end + washer + 0.3 mm`, so under normal rolling nothing touches; when
the case is lifted the body hangs on that washer. The counterbore leaves a
1.5 mm wall in the neck — thin, but it only ever sees the carriage's own weight.

**This depends on two numbers not yet measured**: `SHOULDER_DEPTH` (case skin
→ plastic shoulder; assumed 0 = flush) and `SHAFT_PROTRUSION` (shoulder →
shaft end; assumed 22). Both are single parameters. Shoulder depth also drives
the thrust-washer ↔ tire clearance (1.9 mm at depth 0; every mm of depth eats
most of a mm of clearance — if it comes out > 1.5 mm we switch to a Ø18
thrust washer or a bronze thrust washer).

## Wheel axle — single through-pin

One **Ø8 h6 ground steel pin** through the body with a **DIN 471 circlip** at
each end. Stack, from the body outward on each side:

```
body | speed ring 0.5 | hub 19 (2× 608 + spacer) | speed ring 0.5 | 0.3 float | circlip | 1.5 stub
```

Why not two shoulder screws: M6×Ø8 shoulder screws from opposite sides each
need ~9.5 mm of thread and would collide inside an 18 mm body. The pin has no
threads, is trapped by the wheels which are trapped by the circlips, and a
wheel comes off by popping one clip. Fix the pin in the body with Loctite 638
(or leave it floating — it cannot go anywhere). A small printed cap can hide
each circlip.

Speed rings guarantee the inner races, not the outer races or hub faces, touch
the body and the circlips.

## Body — tolerances for the machinist

| Feature | Nominal | Tolerance | Why |
|---|---|---|---|
| Bushing bore | Ø12 H7 (+0 / +0.018) | — | Oilite press fit; bushing closes ~0.02 on its ID when pressed, which is what gives the running fit on the Ø10 shaft |
| Bushing bore ⟂ to top face | — | ≤ 0.03 over 15 mm | swivel axis must be square to the thrust washer |
| Axle bore | Ø8.00 | +0.005 / +0.015 | light slip fit for an 8 h6 pin, Loctite 638 |
| Axle bore ⟂ to the Y faces of the neck | — | ≤ 0.02 | wheels must run parallel |
| Neck width | 18.0 | ±0.05 | sets wheel gap |
| Retention counterbore | Ø15, to the ceiling depth in the STEP | ±0.1 | non-critical |
| Everything else | as STEP | ±0.1 | — |

Finish: as-machined or bead-blast + anodise. Break all edges.

# Wheel

![wheel cross-section](cross_section.png)

## Why two bearings per wheel

Each wheel hangs off the side of the body on the axle pin. A single bearing
would let it rock under side load (which is what killed the plastic bore). Two
608s, one at each face, give a 12 mm span between bearing centres and turn the
rocking load into a simple radial couple. Load-wise a 608 is absurdly
over-rated (Cr ≈ 3.3 kN each; a wheel sees < 150 N) — the choice is driven by
geometry and price: they're skateboard bearings, ~$1 each.

Use **2RS** (rubber sealed) variants — the wheel lives at ankle height in grit
and rain. Alternatives are in the `BEARINGS` table in `params.py`.

SKF abutment limits for 608: housing shoulder ≤ Ø20.4, shaft shoulder ≥ Ø9.6.
Design uses a Ø20.0 shoulder and Ø11 spacer.

## Hub — tolerances for the machinist

The hub is a lathe-only part. Callouts that matter:

| Feature | Nominal | Tolerance | Why |
|---|---|---|---|
| Bearing bore (×2) | Ø22.00 | **−0.010 / −0.020** (i.e. Ø21.98–21.99) | light press fit for a 608 (OD 22 h0/−0.008). Bearing goes in with a vise or arbor press, no retaining compound needed. |
| Bore concentricity, both ends | — | ≤ 0.02 TIR | both bearings must share an axis or the wheel binds |
| Shoulder Ø20 | Ø20.0 | ±0.1 | non-critical, just clears the seal |
| Shoulder width | 5.00 | ±0.05 | sets bearing spacing; spacer is matched |
| Hub width (face to face) | 19.00 | ±0.05 | sets the axle stack length |
| Ø38 / Ø36 | — | ±0.1 | tire is stretch-fit, forgiving |
| Chamfers | 0.5 × 45° | — | bore chamfer is the press lead-in, don't omit |

Finish: as-machined is fine. Anodise optional (looks good, no functional need).

If the shop asks for a drawing rather than "STEP + this table", the table above
is the drawing.

## Spacer

Tube Ø11 / Ø8.2 × 5.00 between the inner races. Its length must equal the
shoulder width to within ±0.05 so that any axial load goes through the two
inner races and the spacer, **not** the outer races through the shoulder.
Printed PETG works for testing; order it in aluminium with the hubs for the
final build — it's a trivial add to the CNC order.

## Speed rings

8×12×0.5 steel washers on both sides of each hub. Their OD (12) touches only
the inner race (Ø8–12.1), so the body face and the circlip bear on the inner
races and never drag on the outer race or the hub face.

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

# Prototype sequence

1. Measure the open questions below; update `params.py`; regenerate; read the
   clearance report.
2. Print `body_proto.stl` (PETG, 100 % infill), `hub_proto.stl` ×2 (PLA),
   `tire.stl` ×2 (TPU). FDM bores come out undersize — ream/scrape the Ø22 bores
   until a 608 pushes in by hand and the Ø8/Ø12 bores to a slip fit. This is a
   **fit and envelope check only**; a printed body will flex.
3. Buy: 4× 608-2RS, AXK1024 + 2× AS1024, Oilite 10×12×15, a length of 8 mm
   precision shaft (or an 8 mm dowel pin ≥ 65 long), 2× DIN 471 Ø8 circlips,
   speed rings, nylon 10×14×1 washer.
4. Assemble on the case. Check: wheel ↔ case skin, thrust washer ↔ tire, body
   ↔ tire, swivel free under load, lift retention works, case sits level.
5. Adjust → regenerate → send `body.step`, `hub.step`, `spacer.step`,
   `axle_pin.step` + the tolerance tables to a CNC shop. Order for all four
   corners if the budget allows; the other three will fail the same way.
6. Print 8 tires (~21 g TPU each), press bearings, fit tires, install.

# Open questions

- [ ] **`SHOULDER_DEPTH`** — case skin → plastic shoulder face. Assumed 0.
- [ ] **`SHAFT_PROTRUSION`** — shoulder face → shaft end. Assumed 22.
- [ ] Retention bolt thread and head (M6 SHCS assumed, Ø10 × 6 head).
- [ ] Diameter of the plastic shoulder face (must be ≥ Ø24 for the AS1024
      washer to bear fully; if smaller, use a Ø18–20 thrust washer).
- [ ] Shaft surface: plain steel? chrome? any wear from the old plastic bore?
- [ ] Is the 19 mm wheel gap exact, and is there room to widen it? (+2 mm
      would give the counterbore a healthier wall.)
- [ ] Anything else under the case near the carriage that limits the 34 mm
      head width or the −16 mm nose?
- [ ] Replace one carriage or all four?
