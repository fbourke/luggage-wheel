# Replacement spinner carriage — design notes

Replacement for a failed dual-wheel spinner carriage (Rimowa-style knockoff):
the whole unit that bolts onto the case's Ø10 swivel shaft and carries two
Ø50 × ~12 mm wheels. The original's wheels ran on plain plastic bores, which
wore out.

![carriage](carriage_views.png)

## Two wheel variants, one body

`params.py` has a `WHEEL_SOURCE` switch (environment variable; default `ots`):

- **`ots`** — off-the-shelf Ø50 × 12 dual-spinner luggage wheels (PU tread,
  plastic hub, one Ø6-bore ball bearing, 13.7 over the hub bosses; ~$2.50
  each in 8-packs). Ø6 axle, trail 16. **This is the plan** — see
  [`wheel_sourcing.md`](wheel_sourcing.md) for the research.
- **`machined`** — our turned Al hub on 2× 688 with a printed TPU tire. Ø8
  axle, trail 18.1. Kept as the fallback if the bought wheels disappoint;
  builds into `export/machined/`.

The body is the same part except for the axle bore (Ø6 vs Ø8) and its
position (trail). Everything below applies to both unless it says otherwise;
the "Wheel" chapter is the machined variant.

## Architecture (`ots`)

| Part | Material | Made by | Qty / carriage |
|---|---|---|---|
| Body | Al 6061-T6 | outsourced CNC (3-axis milled) | 1 |
| Axle pin | Ø6 h6 ground steel shaft, 51.6 long, 2 circlip grooves | cut + grooved, or CNC order | 1 |
| Circlip | DIN 471 Ø6 | purchased | 2 |
| Wheel | generic Ø50 × 12 PU luggage wheel, Ø6 bearing | purchased, 8-pack | 2 |
| Inboard spacer bush | Ø8 / Ø6.1 × 1.0, steel or Al (kits include similar) | kit / turned / printed | 2 |
| Outboard ring | steel 6×10×0.5 washer | purchased | 2 |
| Swivel thrust bearing | AXK1024 needle thrust + 2× AS1024 washers | purchased | 1 set |
| Swivel bushing | Oilite SAE 841, 10×12×15 | purchased | 1 |
| Retention bolt | existing M5 button head, 19 under head — bears directly on the body | reuse | 1 |

For `machined` swap the wheel rows for: Ø8 axle pin 46.4 long, DIN 471 Ø8
circlips, 2× Al hub, 4× 688-2RS, 2× Al spacer ring, 4× 8×12×0.5 speed rings,
2× TPU tire.

Everything is parametrised in [`cad/params.py`](../cad/params.py); regenerate
with `uv run cad/generate.py`.

## Coordinate frame

`X` fore/aft with the shaft axis at X = 0 and the wheels at X = +TRAIL (16 for
`ots`, 18.1 for `machined`);
`Y` across; `Z` up with **Z = 0 at the land** — the raised plastic face at the
ceiling of the corner recess that the swivel bears on. The case's bottom skin
is at Z = −22.92, flush with the shaft end; floor at Z = −53.5.

## Envelope — why the body looks the way it does

Each corner of the case has a **quarter-circle recess**, ~47.4 mm radius about
the shaft axis and 22.9 mm deep. The Ø10 shaft hangs from the recess ceiling
and ends flush with the case skin, so the whole shaft, the swivel, and the
upper 19 mm of the wheels live inside the recess; the wheels stick out ~30 mm
below the skin. Measured: land → floor 53.5, so **the wheel top is 3.5 mm
below the land** and the axle is 28.5 mm down. Consequences:

- Nothing can sit above the wheels. Everything that spans wider than the
  **16 mm neck** (wheel gap 17 − 2 × 0.5) has to be in front of the wheel
  circle or sculpted to it.
- **Swivel boss**: a Ø26 round about the shaft axis (covers the Ø24 thrust
  washer), half-round in front, tapering into the neck 3 mm behind the axis.
  It runs from the top face at Z −4 down to a **flat at Z −24.6**, enclosing
  the whole 15 mm bushing (where the tilting moment from the trailing wheels
  goes) and the shaft end. Where the boss overhangs the wheels (|Y| > 8) it is
  scooped to a cylinder 1.5 mm outside the tire; those two small "ears" are
  the minimum needed to back the thrust washer.
- **Arm**: in side view, a Ø18 round about the axle joined to the boss by two
  tangent lines — one from the boss rear at Z −12 (nothing above it), one from
  the flat just behind the bolt head. Nothing sits under the bolt head.
- The whole body is inside the recess above the skin plane (max 27 mm from
  the axis; the wall is at 47).
- **Width is capped by the recess wall.** The farthest point from the swivel
  axis is the outer tread edge where the wheel crosses the skin plane; the
  original (16.63 gap, 11.5 wheels) swings at R 46.86 against a ~47.4 wall.
  Width and trail trade off against each other: `machined` keeps 11.5 mm
  wheels at the original 18.1 trail (swing R 46.86, overall 39.6); `ots`
  wheels are 13.7 over the bosses so the trail drops to 16.0, which brings the
  swing radius *in* to 45.9 (overall 43.7). `params.py` asserts the swing
  radius never exceeds the original's.

`generate.py` prints an analytic clearance report (thrust washer ↔ tire, neck
↔ tire, wheel swing ↔ recess wall, body and bolt head ↔ floor). Check it
after every parameter change.

## Swivel

The Ø10 (measured 9.82) shaft is fixed to the case; the body rotates on it and
the case's weight bears on the Ø20.4 plastic land molded around the shaft,
with radial ribs at the same height.

**Thrust — AXK1024 needle roller thrust bearing (10×24×2) between two AS1024
hardened washers (10×24×1)**, 4 mm total, between the land and the body's top
face. The upper washer is stationary against the plastic, the lower one turns
with the body, needles between. The Ø24 washer overhangs the Ø20.4 land by
1.8 mm but sits on the ribs there, and spreads the load on the plastic far
better than the old body did.

**Radial — Oilite bronze sleeve bushing 10×12×15**, pressed into a Ø12 H7 bore
from the top, flush with the top face. A swivel turns a few degrees at near
zero speed under moderate load: that is textbook sintered-bronze territory, and
no ball bearing with a Ø10 bore fits inside an 18 mm neck anyway (6800 is
Ø19 OD). Shaft finish matters more than the bushing: if the shaft is rough or
plated-and-chipped, polish it.

**Retention** — OEM style, closed bore. The Ø10.4 shaft clearance bore stops
at an internal **step 0.3 mm below the shaft end** (Z −22.62); a **Ø5.5 hole**
for the bolt shank continues through a **2 mm step** to the boss's bottom flat
(Z −24.62). The existing **M5 button-head bolt (Ø9.5 head, 19 mm under head)**
threads into the shaft end with its head bearing directly on the flat. Under
normal rolling nothing touches (the 0.3 float); lift the case and the bolt
head pulls the body up by the step. No washer, and the shaft end is captured
inside the body. A 3 mm hex key reaches the bolt from below between the
wheels (point the key's long arm forward).

Why not a plain flat with a washer (the previous revision): it worked on the
printed proto — the shaft sat 1.8 mm proud, by design — but the closed bore is
one part fewer, stiffer around the shaft end, and matches what the OEM did.

Bushing bottom (Z −19) to the step (Z −22.62): 3.6 mm of clearance bore.

## Wheel axle — single through-pin

One **ground steel pin** (Ø6 h6 for `ots`, Ø8 h6 for `machined`) through the
body with a **DIN 471 circlip** at each end. Stack, from the body outward on
each side:

```
ots:      body | spacer bush 1.0 | wheel 13.7 (bosses + bearing) | ring 0.5 | 0.3 float | circlip | 1.5 stub
machined: body | speed ring 0.5  | hub 11.5 (2× 688 + spacer)     | ring 0.5 | 0.3 float | circlip | 1.5 stub
```

For `ots` the inboard bush is a small flanged tube that seats in the wheel's
bearing inner race and holds the rotating plastic hub boss off the body face
(the Amazon kits include these). Ø6 pin bending stress at full corner load is
~60 MPa — fine for any steel.

Why not two shoulder screws: M6×Ø8 shoulder screws from opposite sides each
need ~9.5 mm of thread and would collide inside a 16 mm body. The pin has no
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
| Axle bore | Ø6.00 (`ots`) / Ø8.00 (`machined`) | +0.005 / +0.015 | light slip fit for an h6 pin, Loctite 638 |
| Axle bore ⟂ to the Y faces of the neck | — | ≤ 0.02 | wheels must run parallel |
| Neck width | 16.0 | ±0.05 | sets wheel gap |
| Step ceiling (bottom of Ø10.4 bore) | 18.62 below the top face | **±0.05** | sets the 0.3 shaft-end float; too shallow and the shaft bottoms, lifting the thrust stack |
| Boss bottom flat | 20.62 below the top face | ±0.1 | bolt head seat |
| Bolt hole | Ø5.5 through the step | ±0.1 | M5 shank clearance |
| Shaft clearance bore | Ø10.4 | ±0.1 | must never touch the Ø9.8 shaft |
| Everything else | as STEP | ±0.1 | — |

Finish: as-machined or bead-blast + anodise. Break all edges.

# Wheel (`machined` variant only)

Fallback if the bought Ø50 × 12 wheels turn out badly. Skip this chapter for
the `ots` build.

![wheel cross-section](cross_section.png)

## Why two bearings per wheel

Each wheel hangs off the side of the body on the axle pin. A single bearing
would let it rock under side load (which is what killed the plastic bore). Two
688s (8×16×5), one at each face of the 11.5 mm hub, give a 6.5 mm span between
bearing centres and turn the rocking load into a simple radial couple.
Load-wise a 688 is still heavily over-rated (Cr ≈ 1.1 kN each; a wheel sees
< 150 N). The 11.5 mm wheel width is forced by the recess (see Envelope): a
608 (7 wide) would only fit singly, and 2× 688 is the widest pair that fits
with a shoulder between them.

Use **2RS** (rubber sealed) variants — the wheel lives at ankle height in grit
and rain. Alternatives are in the `BEARINGS` table in `params.py`.

SKF abutment limits for 688: housing shoulder ≤ Ø14.6, shaft shoulder ≥ Ø9.4.
Design uses a Ø14.0 shoulder and Ø11 spacer.

## Hub — tolerances for the machinist

The hub is a lathe-only part. Callouts that matter:

| Feature | Nominal | Tolerance | Why |
|---|---|---|---|
| Bearing bore (×2) | Ø16.00 | **−0.008 / −0.016** (i.e. Ø15.984–15.992) | light press fit for a 688 (OD 16 h0/−0.008). Bearing goes in with a vise or arbor press, no retaining compound needed. |
| Bore concentricity, both ends | — | ≤ 0.02 TIR | both bearings must share an axis or the wheel binds |
| Shoulder Ø14 | Ø14.0 | ±0.1 | non-critical, just clears the seal |
| Shoulder width | 1.50 | ±0.05 | sets bearing spacing; spacer is matched |
| Hub width (face to face) | 11.50 | ±0.05 | sets the axle stack length |
| Ø38 / Ø36 | — | ±0.1 | tire is stretch-fit, forgiving |
| Chamfers | 0.5 × 45° | — | bore chamfer is the press lead-in, don't omit |

Finish: as-machined is fine. Anodise optional (looks good, no functional need).

If the shop asks for a drawing rather than "STEP + this table", the table above
is the drawing.

## Spacer

Ring Ø11 / Ø8.2 × 1.50 between the inner races — effectively a thick shim
washer. Its length must equal the shoulder width to within ±0.05 so that any
axial load goes through the two inner races and the spacer, **not** the outer
races through the shoulder. Too thin to print well; order it in aluminium with
the hubs (trivial add to the CNC order) or stack 8×11 shim washers to 1.5.

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

1. ~~Measure the open questions~~ — done 2026-09-15.
2. ~~Print `carriage_fit_proto.stl` and screw it on~~ — done 2026-09-16 with
   the 11.5-wide/18.1-trail geometry: fits, pivots freely, ride height matches
   the other corners. The `ots` geometry (13.7 wheels, trail 16) swings
   *inside* that envelope, so it doesn't need its own fit check.
3. **Buy an 8-pack of Ø50 × 12 PU luggage wheels** (e.g. Amazon B0DLNMPGF9,
   ~$20) and measure them: OD, tread width, width over the bosses, bore, boss
   diameter. Update `OTS_*` in `params.py` if they differ from 50 / 12 / 13.7 /
   6 / 20. Spin one on a Ø6 pin: if the bearing feels gritty or the wheel rocks
   noticeably, that's the cue to fall back to `machined`.
4. Print `body_proto.stl` (PETG, 100 % infill) with the real Ø6 axle bore and
   trail; ream the Ø6 and Ø12 bores to a slip fit. Mount the bought wheels on
   a 6 mm pin (or the kit's own axle) and check the wheel ↔ boss scoop and
   thrust-washer gaps in the flesh.
5. Buy the rest: AXK1024 + 2× AS1024, Oilite 10×12×15, Ø6 h6 precision shaft
   (or a 6 mm dowel pin ≥ 55 long), 2× DIN 471 Ø6 circlips, 6×10×0.5
   washers — or just use the wheel kit's axle + screw, which fit.
6. Assemble on the case. Check: wheel ↔ recess ceiling, swing through 360°,
   thrust washer ↔ tire, body ↔ tire, swivel free under load, lift retention,
   case level.
7. Adjust → regenerate → send `body.step` + `axle_pin.step` (+ the spacer
   bushes if the kit's don't suit) with the tolerance tables to a CNC shop.
   Four of each; the other three corners will fail the same way.
8. For the `machined` fallback: `WHEEL_SOURCE=machined uv run cad/generate.py`,
   then hubs/spacers/pins from `export/machined/`, 688s, printed TPU tires.

# Open questions

Measured 2026-09-15 (all now in `params.py`):

- [x] Land → shaft end 22.92; shaft end flush with the case skin; shaft Ø9.82.
- [x] Land Ø20.39, raised, with radial ribs at the same height (backs the Ø24
      thrust washer).
- [x] Retention bolt: M5 button head, 19 under head.
- [x] Original wheels 11.5 wide, gap 16.63, ~40 overall.
- [x] Corner recess: quarter circle, wall ~42.4 from the shaft OD (R ≈ 47.4).
- [x] All four carriages eventually.

Test-fit 2026-09-16 (blocky body, 11.5 wheels, trail 18.1): fits the recess,
pivots perfectly, height matches the OEM corners.

Still open:

- [ ] Actual dimensions of the bought Ø50 × 12 wheels (see prototype step 3).

- [x] Recess radius: the printed proto swings a full 360° at swing R 46.86;
      the `ots` geometry swings at 45.9.
- [ ] Is the recess wall vertical, or does it flare? (Only matters if we ever
      want wider wheels.)
- [ ] Shaft surface: plain steel? chrome? any wear from the old plastic bore?
      Oilite 10 mm ID on a 9.82 shaft is ~0.2 mm loose — acceptable for a swivel,
      but if it feels sloppy, a 3D-printed or bronze 9.9 ID sleeve is the fix.
- [ ] Bolt thread pitch: M5×0.8 assumed (standard coarse).
