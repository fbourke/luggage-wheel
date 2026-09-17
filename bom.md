# Bill of materials

Per carriage (one corner, two wheels), and for all four corners. This is the
**`ots` build** (bought Ø50 × 12 wheels); the machined-wheel fallback is at the
bottom.

## Machined (send STEP + tolerance tables from `docs/design.md`)

| # | Item | File | Material | Per carriage | ×4 | Est. cost (×4) |
|---|---|---|---|---|---|---|
| 1 | Body | `export/body.step` | Al 6061-T6, 3-axis milled | 1 | 4 | $120–240 |
| 2 | Axle pin | `export/axle_pin.step` | steel, Ø6 h6 × 51.6, two DIN 471 grooves | 1 | 4 | $20–40, or cut from 6 mm precision shaft and groove by hand/Dremel |
| 3 | Inboard spacer bush | `export/ots_spacer.step` | steel or Al, Ø8 / Ø6.1 × 1.0 — only if the wheel kit's bushes don't fit | 2 | 8 | $10 |

Services: PCBWay / JLCCNC / Xometry / Protolabs, or a local shop. One quote for all line items — setup dominates at these quantities.

## Purchased

| # | Item | Spec | Per carriage | ×4 | Source | Est. (×4) |
|---|---|---|---|---|---|---|
| 4 | **Wheel** | generic **Ø50 × 12 mm PU luggage replacement wheel**, Ø6 bearing bore, ~13.7 over the hub bosses. e.g. Amazon B0DLNMPGF9 (FLIHONST, PU) — avoid TPE-tread listings. Kits include Ø6 axles, screws, washers, spacer bushes, Ø42 caps. | 2 | 8 | Amazon / AliExpress, 8-packs | **$20–25** (one pack) |
| 6 | Circlip | **DIN 471 Ø6** external retaining ring (groove Ø5.7 × 0.8) | 2 | 8 | hardware / McMaster | $3 |
| 7 | Outboard rings | 6 mm ID × 10 OD × 0.5 steel washers (DIN 988 shim rings) | 2 | 8 | McMaster / Amazon shim assortment | $5 |
| 8 | Thrust bearing | **AXK1024** needle roller thrust, 10×24×2 | 1 | 4 | bearing supplier / Amazon / AliExpress | $8–12 |
| 9 | Thrust washers | **AS1024** hardened, 10×24×1 | 2 | 8 | same, often bundled with AXK1024 | $5–8 |
| 10 | Swivel bushing | **Oilite SAE 841 sleeve, 10 ID × 12 OD × 15 L** | 1 | 4 | McMaster 6391K-series / bearing supplier | $6–10 |
| 12 | Retention bolt | existing — reuse; head bears directly on the body (closed bore, no washer). If replacing: M5×0.8 button head (ISO 7380) × 20, + blue Loctite | 1 | 4 | — | $0 |
| 13 | Retaining compound | Loctite 638 (axle pin in body) | — | 1 tube | — | $10 |

## Printed

| # | Item | File | Material | Per carriage | ×4 |
|---|---|---|---|---|---|
| 15 | Circlip cap (optional; the wheel kits' Ø42 snap caps may do) | — | any | 2 | 8 |
| — | One-piece fit proto | `export/carriage_fit_proto.stl` | PETG or PLA, ~75 g, supports on | 1 | — |
| — | Body proto | `export/body_proto.stl` | PETG, 100 % infill | 1 | — |

**Rough total for four corners: $220–380**, dominated by the milled body. One corner only: ~$100–150 (small-quantity CNC pricing hurts).

## Machined-wheel fallback (`WHEEL_SOURCE=machined`, files in `export/machined/`)

Replaces items 2–4, 6, 7 above: Ø8 h6 × 46.4 axle pin with DIN 471 Ø8 grooves
($20–40 ×4); 2 Al hubs per carriage (`hub.step`, $60–120 ×4); 2 Al spacer
rings (`spacer.step`, $10–20); 4× **688-2RS** 8×16×5 bearings per carriage
($10–20 for 16); DIN 471 Ø8 circlips; 8×12×0.5 skate speed rings; 2 printed
TPU 95A tires (`tire.stl`, ~12 g each, on their side, 100 % infill). Adds
~$100–200 to the four-corner total.

## Tools

- (machined variant only) bench vise or arbor press + a socket that bears on the 688 outer race
- 3 mm hex key (retention bolt head is exposed under the boss, reached from below between the wheels)
- Circlip pliers (external, small)
- Digital calipers
- Optional: 8 mm and 12 mm reamers for the printed prototypes
