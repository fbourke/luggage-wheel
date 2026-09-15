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

EXPORT = Path(__file__).resolve().parent.parent / "export"
STL_OPTS = dict(tolerance=0.01, angular_tolerance=0.05)


def step(shape, name: str) -> None:
    export_step(shape, str(EXPORT / f"{name}.step"))


def stl(shape, name: str) -> None:
    export_stl(shape, str(EXPORT / f"{name}.stl"), **STL_OPTS)


def main() -> None:
    EXPORT.mkdir(exist_ok=True)

    # ---- wheel parts -------------------------------------------------------
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

    # ---- report ------------------------------------------------------------
    print(f"bearing       : {P.BEARING}  {P.BRG_ID}x{P.BRG_OD}x{P.BRG_W}  x{P.BEARINGS_PER_WHEEL} per wheel")
    print(f"hub           : Ø{P.FLANGE_D}/Ø{P.BED_D} x {P.HUB_W}  bore Ø{P.BORE_D}  "
          f"shoulder Ø{P.SHOULDER_D} x {P.SHOULDER_W}   {W.mass_g(hub, 'Al6061'):.1f} g Al")
    print(f"tire          : Ø{P.WHEEL_OD} x {P.TIRE_W}, printed ID Ø{P.BED_D*(1-P.TIRE_STRETCH):.2f} "
          f"(stretch {P.TIRE_STRETCH*100:.1f}%)   {W.mass_g(tire, 'TPU95A'):.1f} g TPU")
    print(f"body          : {P.HEAD_W} wide head / {P.NECK_W} neck, top Z={P.BODY_TOP_Z}, "
          f"bottom Z={P.BODY_BOTTOM_Z}   {W.mass_g(body, 'Al6061'):.1f} g Al")
    print(f"axle pin      : Ø{P.AXLE_PIN_D} x {P.AXLE_PIN_L:.1f}, circlip grooves at ±{P.AXLE_GROOVE_Y:.2f}")
    print(f"swivel        : AXK1024 thrust + Oilite {P.BUSHING_ID:g}x{P.BUSHING_OD:g}x{P.BUSHING_L:g} bushing, "
          f"{P.RETAIN_BOLT} retention bolt in Ø{P.RETAIN_CBORE_D} cbore")
    print(f"overall width : {P.OVERALL_W:.1f} mm  (wheel centres ±{P.WHEEL_CENTRE_Y:.2f})")
    print("clearances:")
    for line in C.clearance_report():
        print("   " + line)
    print(f"exported to   : {EXPORT}")


if __name__ == "__main__":
    main()
