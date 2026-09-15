"""
Generate all wheel parts from params.py and export STEP/STL to ../export.

Run from repo root:  uv run cad/generate.py
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Compound,
    GeomType,
    Location,
    Part,
    Plane,
    Polygon,
    ShapeList,
    chamfer,
    export_step,
    export_stl,
    fillet,
    revolve,
)

sys.path.insert(0, str(Path(__file__).parent))
import params as P  # noqa: E402

EXPORT = Path(__file__).resolve().parent.parent / "export"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def revolved(profile_rz: list[tuple[float, float]]) -> Part:
    """Revolve a closed (r, z) half-profile about the Z axis."""
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            Polygon(*profile_rz, align=None)
        revolve(axis=Axis.Z)
    return bp.part


def circ_edges(part: Part, radius: float, z: float | None = None) -> ShapeList:
    """Circular edges of a given radius, optionally at a given |z|."""
    out = []
    for e in part.edges().filter_by(GeomType.CIRCLE):
        if abs(e.radius - radius) > 1e-3:
            continue
        if z is not None and abs(abs(e.center().Z) - abs(z)) > 1e-3:
            continue
        out.append(e)
    return ShapeList(out)


def mass_g(part: Part, material: str) -> float:
    return part.volume * P.DENSITY[material]


# ---------------------------------------------------------------------------
# hub  (aluminium, turned)
# ---------------------------------------------------------------------------
def make_hub() -> Part:
    hw = P.HUB_W / 2
    z_brg = hw - P.BRG_W                 # inner face of each bearing pocket
    z_flg = hw - P.FLANGE_W              # inner face of each flange
    r_bore, r_sh = P.BORE_D / 2, P.SHOULDER_D / 2
    r_flg, r_bed = P.FLANGE_D / 2, P.BED_D / 2

    profile = [
        (r_bore, -hw), (r_bore, -z_brg),
        (r_sh, -z_brg), (r_sh, z_brg),
        (r_bore, z_brg), (r_bore, hw),
        (r_flg, hw), (r_flg, z_flg),
        (r_bed, z_flg), (r_bed, -z_flg),
        (r_flg, -z_flg), (r_flg, -hw),
    ]
    hub = revolved(profile)

    with BuildPart() as bp:
        bp._add_to_context(hub)  # noqa: SLF001 - adopt existing solid
        chamfer(circ_edges(bp.part, r_flg, hw), P.EDGE_CHAMFER)
        chamfer(circ_edges(bp.part, r_bore, hw), P.BORE_CHAMFER)
    return bp.part


# ---------------------------------------------------------------------------
# spacer  (aluminium or printed tube between inner races)
# ---------------------------------------------------------------------------
def make_spacer() -> Part:
    hl = P.SPACER_L / 2
    ri, ro = P.SPACER_ID / 2, P.SPACER_OD / 2
    return revolved([(ri, -hl), (ri, hl), (ro, hl), (ro, -hl)])


# ---------------------------------------------------------------------------
# tire  (TPU, printed undersize for stretch fit)
# ---------------------------------------------------------------------------
def make_tire() -> Part:
    s = 1.0 - P.TIRE_STRETCH
    hw = P.TIRE_W / 2
    z_flg = P.HUB_W / 2 - P.FLANGE_W
    r_bed, r_flg = s * P.BED_D / 2, s * P.FLANGE_D / 2
    r_od = P.WHEEL_OD / 2

    profile = [
        (r_bed, -z_flg), (r_bed, z_flg),
        (r_flg, z_flg), (r_flg, hw),
        (r_od, hw), (r_od, -hw),
        (r_flg, -hw), (r_flg, -z_flg),
    ]
    tire = revolved(profile)
    try:
        with BuildPart() as bp:
            bp._add_to_context(tire)  # noqa: SLF001
            fillet(circ_edges(bp.part, r_od, hw), P.TIRE_EDGE_FILLET)
        return bp.part
    except Exception as exc:  # pragma: no cover
        print(f"  ! tread fillet failed ({exc}); exporting sharp-edged tire")
        return tire


# ---------------------------------------------------------------------------
# bearing dummy (for assembly visualisation only)
# ---------------------------------------------------------------------------
def make_bearing() -> Part:
    hw = P.BRG_W / 2
    ri, ro = P.BRG_ID / 2, P.BRG_OD / 2
    return revolved([(ri, -hw), (ri, hw), (ro, hw), (ro, -hw)])


# ---------------------------------------------------------------------------
def main() -> None:
    EXPORT.mkdir(exist_ok=True)

    hub, spacer, tire, brg = make_hub(), make_spacer(), make_tire(), make_bearing()

    # Individual parts first: Compound(children=...) takes ownership of its
    # children, so build the assembly afterwards from copies.
    export_step(hub, str(EXPORT / "hub.step"))
    export_step(spacer, str(EXPORT / "spacer.step"))
    export_step(tire, str(EXPORT / "tire.step"))
    export_stl(hub, str(EXPORT / "hub_proto.stl"), tolerance=0.01, angular_tolerance=0.05)
    export_stl(spacer, str(EXPORT / "spacer.stl"), tolerance=0.01, angular_tolerance=0.05)
    export_stl(tire, str(EXPORT / "tire.stl"), tolerance=0.01, angular_tolerance=0.05)

    z_brg = P.HUB_W / 2 - P.BRG_W / 2
    children = []
    for label, shape in [
        ("hub", copy.copy(hub)),
        ("spacer", copy.copy(spacer)),
        ("tire", copy.copy(tire)),
        ("bearing_outer", brg.moved(Location((0, 0, +z_brg)))),
        ("bearing_inner", brg.moved(Location((0, 0, -z_brg)))),
    ]:
        shape.label = label
        children.append(shape)
    assembly = Compound(children=children, label="wheel")
    export_step(assembly, str(EXPORT / "wheel_assembly.step"))

    print(f"bearing       : {P.BEARING}  {P.BRG_ID}x{P.BRG_OD}x{P.BRG_W}  x{P.BEARINGS_PER_WHEEL}")
    print(f"hub           : Ø{P.FLANGE_D}/Ø{P.BED_D} x {P.HUB_W}  bore Ø{P.BORE_D}  "
          f"shoulder Ø{P.SHOULDER_D} x {P.SHOULDER_W}")
    print(f"hub mass      : {mass_g(hub, 'Al6061'):.1f} g (Al)   {mass_g(hub, 'PLA'):.1f} g (PLA proto)")
    print(f"spacer        : Ø{P.SPACER_OD}/Ø{P.SPACER_ID} x {P.SPACER_L}")
    print(f"tire          : Ø{P.WHEEL_OD} x {P.TIRE_W}, printed ID Ø{P.BED_D*(1-P.TIRE_STRETCH):.2f} "
          f"(stretch {P.TIRE_STRETCH*100:.1f}%), min wall {P.TIRE_MIN_THICKNESS:.1f}")
    print(f"tire mass     : {mass_g(tire, 'TPU95A'):.1f} g (TPU, solid)")
    print(f"wheel mass    : ~{mass_g(hub,'Al6061') + mass_g(tire,'TPU95A') + 2*12 + mass_g(spacer,'Al6061'):.0f} g "
          f"(608-2RS ≈ 12 g each)")
    print(f"exported to   : {EXPORT}")


if __name__ == "__main__":
    main()
