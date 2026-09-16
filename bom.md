# Bill of materials

Per carriage (one corner, two wheels), and for all four corners.

## Machined (send STEP + tolerance tables from `docs/design.md`)

| # | Item | File | Material | Per carriage | ×4 | Est. cost (×4) |
|---|---|---|---|---|---|---|
| 1 | Body | `export/body.step` | Al 6061-T6, 3-axis milled | 1 | 4 | $120–240 |
| 2 | Hub | `export/hub.step` | Al 6061-T6, turned | 2 | 8 | $60–120 |
| 3 | Bearing spacer | `export/spacer.step` | Al (PETG print for protos) | 2 | 8 | $10–20 |
| 4 | Axle pin | `export/axle_pin.step` | steel, Ø8 h6 × 46.4, two DIN 471 grooves | 1 | 4 | $20–40, or cut from 8 mm precision shaft and groove by hand/Dremel |

Services: PCBWay / JLCCNC / Xometry / Protolabs, or a local shop. Ask for one quote with all four line items — setup dominates at these quantities.

## Purchased

| # | Item | Spec | Per carriage | ×4 | Source | Est. (×4) |
|---|---|---|---|---|---|---|
| 5 | Wheel bearing | **688-2RS** 8×16×5, sealed (a.k.a. 688ZZ/688RS; common in RC cars and fidget spinners) | 4 | 16 | Amazon / AliExpress / bearing supplier, packs of 10 | $10–20 |
| 6 | Circlip | **DIN 471 Ø8** external retaining ring (groove Ø7.6 × 0.9) | 2 | 8 | hardware / McMaster 98541A112-ish | $3 |
| 7 | Speed rings | 8 mm ID × ~12 OD × 0.5 steel washers ("skateboard speed rings") | 4 | 16 | skate shop | $5 |
| 8 | Thrust bearing | **AXK1024** needle roller thrust, 10×24×2 | 1 | 4 | bearing supplier / Amazon / AliExpress | $8–12 |
| 9 | Thrust washers | **AS1024** hardened, 10×24×1 | 2 | 8 | same, often bundled with AXK1024 | $5–8 |
| 10 | Swivel bushing | **Oilite SAE 841 sleeve, 10 ID × 12 OD × 15 L** | 1 | 4 | McMaster 6391K-series / bearing supplier | $6–10 |
| 11 | Retention washer | nylon (or PTFE) ~6 ID × 14 OD × 1.5, fits over the M5 bolt; the OD is what matters | 1 | 4 | hardware / Amazon assortment | $2 |
| 12 | Retention bolt | existing — reuse. If replacing: M5×0.8 button head (ISO 7380) × 20, + blue Loctite | 1 | 4 | — | $0 |
| 13 | Retaining compound | Loctite 638 (axle pin in body) | — | 1 tube | — | $10 |

## Printed

| # | Item | File | Material | Per carriage | ×4 |
|---|---|---|---|---|---|
| 14 | Tire | `export/tire.stl` | TPU 95A, ~12 g, print on its side, 100 % infill | 2 | 8 |
| 15 | Circlip cap (optional, TBD) | — | any | 2 | 8 |
| — | One-piece fit proto | `export/carriage_fit_proto.stl` | PETG or PLA, ~80 g, supports on | 1 | — |
| — | Body proto | `export/body_proto.stl` | PETG, 100 % infill | 1 | — |
| — | Hub proto | `export/hub_proto.stl` | PLA | 2 | — |

**Rough total for four corners: $270–500**, dominated by the milled body. One corner only: ~$120–180 (small-quantity CNC pricing hurts).

## Tools

- Bench vise or arbor press + a socket that bears on the 688 outer race only
- 3 mm hex key (retention bolt head is exposed under the boss, reached from below between the wheels)
- Circlip pliers (external, small)
- Digital calipers
- Optional: 8 mm and 12 mm reamers for the printed prototypes
