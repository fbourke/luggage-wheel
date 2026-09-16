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
| 3 | Floyd wheel set (floyd.one) | **Ø55 × ~24** (width estimated from photos; 55 and 85A printed on the wheel) | 608 skate bearings ×2, skate axle + nut | PU 85A, made in China | $9.40 ($75 / 8) | ✗ as a dual (2 × 24 + body ≫ 40) · ✓ as a **single centred wheel** | Fun alternative, needs a fork body — see below. |
| 4 | Generic 55 mm 85A "skateboard wheels with 608 bearings" (eBay, 4 for $15.90) | Ø55 × 30–36 typical | 608 ×2 | PU 85A | $4 | ✗ dual; single only if ≤ ~26 wide | Same idea as Floyd, cheaper, but most are wider than Floyd's. Check width before buying. |
| 5 | Rimowa OEM replacement wheels (Topas / Classic / Original / Salsa carry-on) | **Ø47** ("1.85 in"), width not listed | not listed | PU | **$53** ($212 / 4) | −1.5 mm ride height | Overpriced for what it is; Rimowa's own dual wheel is just a nicer #1. |
| 6 | Hinomoto (JP OEM: Rimowa Essential, Tumi, Proteca, Monos) | — | — | — | — | — | See "premium thread" below; Hinomoto sells caster *units* to brands, not bare wheels at retail, as far as we could find. |

## What Floyd actually sells

The Floyd "wheel set" is eight **55 mm, 85A** urethane wheels with two ABEC‑7
(608) bearings each, "designed and developed for Floyd cases only", made in
China. The product photos show a plain skate-wheel profile with the bearing
face exposed, a hex axle nut and a skate-style ratchet tool. In other words
it's a small cruiser skateboard wheel with Floyd's graphics, and the $75 is
brand + colourway. The width isn't published; scaling the photos against the
55 mm diameter gives ~24 mm, narrower than a street skate wheel (30–34) but
double what our recess allows for a dual.

Their carriage is a **cantilever**: one arm, wheel hung outboard on a stub
axle with a nut, like a skateboard truck cut in half. Eight wheels = four
corners × two, so Floyd cases are dual-wheel spinners too, just wide ones.

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

## Floyd-style single wheel — if you want the look

A single Ø55 × 24 wheel centred under the swivel also fits the recess:

- Wheel top 3 mm below the land → axle at Z −30.5, **ride height +4.5 mm** at
  every corner (so all four carriages, no mixing).
- Swing: at trail 18.1 the rear tread edge at the skin plane sits at
  hypot(44.5, 12) = 46.1 < 46.86 — inside the original's swing.
- Body becomes a **fork**: two 5 mm arms outside the wheel, 36 wide at the
  axle, Ø26 boss in front as now. Or a Floyd-style cantilever (one arm, wheel
  outboard, nut) — simpler to machine, asymmetric.
- Axle: Ø8 skate standard, 608 ×2 with a 10 mm skate spacer, M8 shoulder bolt
  or Ø8 pin + circlips.

This is a new body (~a day of CAD) and a different look; it buys real
skate-grade urethane and bearings you can get anywhere. Parked unless you
want it.

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
- Skateboard / roller-skate wheels: Ø50–60 but 30+ wide.
- Casters with Ø50 PU tread: 18–20 wide, plain bores.
- DuckDuckGo (captcha), Bing (junk results), Reddit and Amazon product pages
  (block fetches) were unusable for automated research; Brave search worked.
