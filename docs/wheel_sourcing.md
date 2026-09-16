# Wheel sourcing — off-the-shelf options

Research notes, 2026-09-16. Goal: stop making our own wheels (Al hub + printed
TPU tire) and buy a professionally moulded PU wheel instead. Hard constraints
from the case (see `design.md`, "Envelope"):

| Constraint | Value | Why |
|---|---|---|
| Diameter | 50 (47–52 tolerable if all four corners are done) | ride height must match the other corners |
| Width per wheel | ≤ ~12.5 tread, ≤ ~14 over any hub bosses | recess wall caps the swing radius at ≈ 47 mm |
| Bore | anything — we make the axle | — |
| Bearings | ball bearings strongly preferred | the plain plastic bore is what failed |

## Shortlist

| # | Product | OD × width | Bore / bearing | Tread | Price / wheel | Fit | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **Generic "50 × 12 mm luggage replacement wheel" 8-packs** (Amazon B0DLNMPGF9 — FLIHONST; many identical listings) | Ø50 × 12 tread, **13.7 over the hub bosses** | Ø6, one ball bearing in a PP hub, flanged spacer bushes each side | PU | **$2.50** ($20 / 8, incl. axles, screws, washers, Ø42 caps, hex keys) | **Drop-in** with a Ø6 axle | **Buy one pack now.** Exactly the OEM format. |
| 2 | Zoofen 50 × 12 8-pack (Amazon B0CTDM5851) | Ø50 × 12, 14 overall | Ø6, one bearing | **TPE** (softer, wears faster) | $3 | drop-in | Skip in favour of #1 (PU). |
| 3 | Floyd wheel set (floyd.one) | **Ø55 × ~19** (55 and 85A printed on the wheel; width measured from a photo of Floyd's rear carriage — 31 px against 89 px of diameter, an upper bound) | 608 skate bearings ×2, skate axle + nut | PU 85A, made in China | $9.40 ($75 / 8) | ✗ dual (needs trail ≤ 11) · ✓ **single centred wheel** | The narrowest 55 mm skate-type wheel we found. Needs a fork body — see below. |
| 4 | Aggressive-inline 55 mm wheels: IQON EQO 55/88A (proskatersplace.com), Ground Control Moon 55/92A (intuitionskate.com); also Undercover, Eulogy, Dead in 55–58 | **Ø55 × 24** (stated) | 608 ×2 (+ standard 8 mm bearing spacer) | cast PU 88–92A | $9–11 ($36–45 / 4) | ✓ single only | Real skate-grade urethane, many brands, any skate shop. 88A is the quieter end; 92A is hard. |
| 4b | Soft skateboard/cruiser 55 mm wheels (OJ, Ricta Clouds, Bones ATF…) 78–85A | Ø55 × 30–35 | 608 ×2 | PU 78–85A | $8–10 | ✓ single, fork gets ~48 wide | Quietest urethane, but chunky. |
| 4c | Generic "55 mm luggage replacement wheel" 8-packs (Amazon B0DM7HD933 etc.) | Ø55 × 12, ~13.7 over bosses | Ø6, one bearing | PU/TPU | $2.50 | ✓ dual at trail ≤ 15, +4.5 mm ride height | The 55 mm version of #1, if you'd rather go up a size. |
| 5 | Rimowa OEM replacement wheels (Topas / Classic / Original / Salsa carry-on) | **Ø47** ("1.85 in"), width not listed | not listed | PU | **$53** ($212 / 4) | −1.5 mm ride height | Overpriced for what it is; Rimowa's own dual wheel is just a nicer #1. |
| 6 | Hinomoto (JP OEM: Rimowa Essential, Tumi, Proteca, Monos) | — | — | — | — | — | See "premium thread" below; Hinomoto sells caster *units* to brands, not bare wheels at retail, as far as we could find. |

## What Floyd actually sells

The Floyd "wheel set" is eight **55 mm, 85A** urethane wheels with two ABEC‑7
(608) bearings each, "designed and developed for Floyd cases only", made in
China. The product photos show a plain skate-wheel profile with the bearing
face exposed, a hex axle nut and a skate-style ratchet tool. In other words
it's a narrow skate wheel with Floyd's graphics, and the $75 is brand +
colourway. The width isn't published; measuring a product photo of Floyd's
rear carriage edge-on (31 px wide vs 89 px tall, and any viewing angle can
only make it look *wider*) gives **≈ 19 mm** — narrower than aggressive-inline
wheels (24) and much narrower than street skate wheels (30–34).

Floyd's carriage is a **fork**: two wheels on a through-axle with a ~30 mm
neck between them, ~68 mm overall. Their case's corner recess is built for
that; ours (R ≈ 47) is not.

## Dual vs single at 55 mm — the numbers

The recess caps the swing radius at the original's 46.86 (wall ≈ 47.4). For a
wheel of radius r whose axle sits `dz` below the skin plane, the tread crosses
the skin at `x = trail + √(r² − dz²)`, and the swing radius is
`hypot(x, half-width)`. Raising the case (lower axle) shrinks the chord, but
slowly:

| Wheel | Layout | Half-width | Ride height | Max trail |
|---|---|---|---|---|
| 55 × 19 | dual (neck 16 + 1 mm spacers) | 28.0 | +4.5 | **11.1** |
| 55 × 19 | dual | 28.0 | +9.5 | 13.1 |
| 55 × 19 | **single, centred** | 9.5 | +4.5 | **19.5** |
| 55 × 24 | single, centred | 12.0 | +4.5 | 18.9 |
| 55 × 32 | single, centred | 16.0 | +4.5 | 17.6 |
| 50 × 12 (bought, `ots`) | dual | 21.85 | 0 | 17.4 (we use 16) |

So a dual of 55 × 19 would need trail ≈ 11 (0.2 D — a caster that short
flutters), and every extra 5 mm of ride height only buys ~1 mm of trail.
A **single centred 55 mm wheel keeps the full 18 mm trail** at +4.5 mm ride
height, for any width up to ~30. That's the route for Floyd or skate wheels.

## Why generic 50 × 12 wins

The case was designed around this exact wheel: Ø50, 12 tread, ~14 over the
hub bosses, Ø6 axle, snap caps. The dozens of 8-pack kits on Amazon are the
same moulding family (the marketing images even show the 11.5–19.5 mm fork
slot they fit). What they are not is *good*: a single small bearing in a PP
hub, so the wheel can rock a little on the axle, and tread quality varies by
listing. That's still far better than the plain bore that failed, and at
$2.50 a wheel they're consumables — keep the other four from the pack as
spares.

The **carriage variant for these wheels** is the default in `params.py`
(`WHEEL_SOURCE=ots`):

- Axle pin Ø6 h6 × 51.6 with DIN 471 Ø6 circlips (groove Ø5.7 × 0.8).
- Neck 16 as before; a flanged Ø8 × 1.0 spacer bush between each body face and
  the wheel's bearing inner race, so the plastic hub boss never rubs the body.
- **Trail 16.0** (was 18.1). The pair is 2.2 mm wider than the originals over
  the tread, so the axle moves 2.1 mm forward to keep the swing radius inside
  the original's (45.9 vs 46.86; wall ≈ 47.4). 0.32 D is still plenty of
  caster trail.
- Overall width 43.7 over the tread; 39.6 for the machined variant.

`WHEEL_SOURCE=machined uv run cad/generate.py` still builds the Al-hub design
into `export/machined/`.

## Single-wheel fork — if you want skate wheels

A single Ø55 wheel centred under the swivel:

- Wheel top 3 mm below the land → axle at Z −30.5, **ride height +4.5 mm** at
  every corner (so all four carriages, no mixing with OEM corners).
- Trail stays at 18 (see table above).
- Body becomes a **fork**: Ø26 swivel boss in front as now, then two 5 mm arms
  either side of the wheel — 31 wide at the axle for a 19 mm wheel, 36 for a
  24 mm wheel, ~44 for a 32 mm cruiser wheel. Arm rear corners swing at R ≈
  31–35, far inside the wall. Or a Floyd-front-style cantilever (one arm,
  wheel outboard on a stub axle with a nut) — simpler to machine, asymmetric,
  and the wheel flips sides as you change direction.
- Axle: Ø8 skate standard, 608 ×2 with the standard 10 mm skate bearing
  spacer, an M8 shoulder bolt with a nyloc, or a Ø8 pin + circlips as now.
- Wheel choice: Floyd 55 × 19 85A ($9.40, buy 8 get 4 spares) or any
  aggressive-inline 55 × 24 (88A for quiet, $9–11). Street/cruiser skate
  wheels work too but make a wide fork.

This is a new body (~a day of CAD, `WHEEL_SOURCE=single55`) and a different
look. Parked unless you want it.

## Premium thread — unresolved leads

Not run to ground: every search engine we could reach ended up captcha- or
rate-walled partway through the evening. What we know and what's worth ten
minutes of manual searching:

- **Hinomoto** (Japan) is the OEM behind Rimowa Essential, Tumi, Proteca,
  Monos and others, and the only luggage-wheel brand people ask for by name.
  Everything we saw is sold as complete *caster units* to brands; the Amazon
  "Hinomoto" search results are generic look-alikes. Worth trying: Amazon JP /
  Rakuten for `スーツケース 交換 車輪 50mm ベアリング` (suitcase replacement
  wheel 50 mm bearing) — the Japanese-market kits tend to be a grade above the
  US Amazon ones, same format. Also Hinomoto's own site for a parts list.
- **Rimowa Essential** (post-LVMH) dual wheels: Reddit threads say they differ
  from the older 47 mm wheels, but nobody quotes dimensions. If a repair shop
  sells them bare they would be the premium version of #1; expect ~$15–25 each.
- **PU-coated bearing rollers**: industrial guide rollers exist as a bearing
  (688 / 6000 / 6001) overmoulded with a PU tyre, typically Ø30–60 × 10–16.
  A Ø50 × 12 on a 688 or 6000 would be a near-ideal wheel — steel hub, real
  bearing, moulded PU — and would justify a dedicated axle. Search
  AliExpress/Misumi for "PU coated bearing 50mm", "polyurethane roller
  bearing 8x50x12", "6000 PU wheel 50mm". Unverified.

## Dead ends

- Inline-skate anti-rocker/grind wheels: Ø42–47 but 24 wide.
- Skateboard / roller-skate wheels: Ø50–60 but 30+ wide (fine as singles).
- Nothing at Ø55 narrower than Floyd's ~19 turned up; 55 × 19 looks like a
  Floyd-specific mould.
- Casters with Ø50 PU tread: 18–20 wide, plain bores.
- DuckDuckGo (captcha), Bing (junk results), Reddit and Amazon product pages
  (block fetches) were unusable for automated research; Brave search worked.
