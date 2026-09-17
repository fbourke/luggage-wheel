"""
Generate all parts from params.py and export STEP/STL to ../export.

Run from repo root:  uv run cad/generate.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from build123d import Compound, Location, export_step, export_stl  # noqa: E402

import carriage as C  # noqa: E402
import params as P  # noqa: E402
import wheel as W  # noqa: E402

EXPORT = Path(__file__).resolve().parent.parent / "export" / ("" if P.OTS else "machined")
STL_OPTS = dict(tolerance=0.01, angular_tolerance=0.05)


def step(shape, name: str) -> None:
    export_step(shape, str(EXPORT / f"{name}.step"))


def stl(shape, name: str) -> None:
    export_stl(shape, str(EXPORT / f"{name}.stl"), **STL_OPTS)


def main() -> None:
    EXPORT.mkdir(parents=True, exist_ok=True)

    print(f"wheel source  : {P.WHEEL_SOURCE}  (set WHEEL_SOURCE=machined|ots)")

    # ---- wheel parts -------------------------------------------------------
    if P.OTS:
        spacer = W.make_ots_spacer()
        step(spacer, "ots_spacer"); stl(spacer, "ots_spacer")
        step(W.make_ots_wheel(), "ots_wheel_ref")
    else:
        hub, spacer, tire, brg = W.make_hub(), W.make_spacer(), W.make_tire(), W.make_bearing()
        step(hub, "hub"); step(spacer, "spacer"); step(tire, "tire")
        stl(hub, "hub_proto"); stl(spacer, "spacer"); stl(tire, "tire")

        z_brg = P.HUB_W / 2 - P.BRG_W / 2
        kids = []
        for label, shape in [
            ("hub", copy.copy(hub)), ("spacer", copy.copy(spacer)),
            ("tire", W.make_tire(installed=True)),
            ("bearing_outer", brg.moved(Location((0, 0, +z_brg)))),
            ("bearing_inner", brg.moved(Location((0, 0, -z_brg)))),
        ]:
            shape.label = label
            kids.append(shape)
        step(Compound(children=kids, label="wheel"), "wheel_assembly")

    # ---- carriage parts ----------------------------------------------------
    body, pin = C.make_body(), C.make_axle_pin()
    step(body, "body"); step(pin, "axle_pin")
    stl(body, "body_proto")
    step(C.make_assembly(), "carriage_assembly")
    proto = C.make_fit_proto()
    step(proto, "carriage_fit_proto"); stl(proto, "carriage_fit_proto")

    # ---- report ------------------------------------------------------------
    if P.OTS:
        print(f"wheel         : off-the-shelf Ø{P.WHEEL_OD:g} x {P.OTS_TREAD_W:g} tread, {P.OTS_WHEEL_W:g} over bosses, "
              f"Ø{P.OTS_BORE_D:g} bore; inboard spacer Ø{P.OTS_SPACER_OD:g} x {P.OTS_INBOARD_SPACER:g}")
    else:
        print(f"bearing       : {P.BEARING}  {P.BRG_ID}x{P.BRG_OD}x{P.BRG_W}  x{P.BEARINGS_PER_WHEEL} per wheel")
        print(f"hub           : Ø{P.FLANGE_D}/Ø{P.BED_D} x {P.HUB_W}  bore Ø{P.BORE_D}  "
              f"shoulder Ø{P.SHOULDER_D} x {P.SHOULDER_W}   {W.mass_g(hub, 'Al6061'):.1f} g Al")
        print(f"tire          : Ø{P.WHEEL_OD} x {P.TIRE_W}, printed ID Ø{P.BED_D*(1-P.TIRE_STRETCH):.2f} "
              f"(stretch {P.TIRE_STRETCH*100:.1f}%)   {W.mass_g(tire, 'TPU95A'):.1f} g TPU")
    print(f"body          : Ø{2*P.BOSS_R:g} boss / {P.NECK_W} neck / Ø{2*P.AXLE_BOSS_R:g} axle boss, top Z={P.BODY_TOP_Z}, "
          f"bottom Z={P.BODY_BOTTOM_Z}   {W.mass_g(body, 'Al6061'):.1f} g Al")
    print(f"axle pin      : Ø{P.AXLE_PIN_D:g} x {P.AXLE_PIN_L:.1f}, DIN 471 grooves Ø{P.CIRCLIP_GROOVE_D:g}x{P.CIRCLIP_GROOVE_W:g} at ±{P.AXLE_GROOVE_Y:.2f}; trail {P.TRAIL:g}")
    print(f"swivel        : AXK1024 thrust + Oilite {P.BUSHING_ID:g}x{P.BUSHING_OD:g}x{P.BUSHING_L:g} bushing, "
          f"{P.RETAIN_BOLT} retention bolt bearing on the closed-bore flat at Z={P.BOSS_BOTTOM_Z:.2f}")
    print(f"overall width : {P.OVERALL_W:.1f} mm  (wheel centres ±{P.WHEEL_CENTRE_Y:.2f})")
    print(f"fit proto     : one piece, {W.mass_g(proto, 'PLA'):.0f} g PLA / {W.mass_g(proto, 'PLA') * 1.27 / 1.24:.0f} g PETG, "
          f"Ø{P.PROTO_SHAFT_BORE_D} shaft bore, screws on with the M5 bolt")
    print("clearances:")
    for line in C.clearance_report():
        print("   " + line)
    print(f"exported to   : {EXPORT}")


if __name__ == "__main__":
    main()
