"""
Wheel parts: hub (Al), spacer, tire (TPU), bearing dummy.

Wheel-local frame: axis of rotation = Z, centred at the origin.
"""

from __future__ import annotations

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    GeomType,
    Part,
    Plane,
    Polygon,
    ShapeList,
    chamfer,
    fillet,
    revolve,
)

import params as P


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
def make_tire(installed: bool = False) -> Part:
    """installed=True draws it at nominal (stretched-on) size for assemblies."""
    s = 1.0 if installed else 1.0 - P.TIRE_STRETCH
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
# off-the-shelf wheel dummy: Ø50 x 12 PU tread on a plastic hub whose bosses
# stand 0.85 proud each side, single Ø6-bore bearing. Modelled as one solid.
# ---------------------------------------------------------------------------
def make_ots_wheel() -> Part:
    ht, hb = P.OTS_TREAD_W / 2, P.OTS_WHEEL_W / 2
    r_bore, r_boss, r_od = P.OTS_BORE_D / 2, P.OTS_BOSS_D / 2, P.WHEEL_OD / 2
    profile = [
        (r_bore, -hb), (r_bore, hb), (r_boss, hb), (r_boss, ht),
        (r_od, ht), (r_od, -ht), (r_boss, -ht), (r_boss, -hb),
    ]
    wheel = revolved(profile)
    try:
        with BuildPart() as bp:
            bp._add_to_context(wheel)  # noqa: SLF001
            fillet(circ_edges(bp.part, r_od, ht), P.TIRE_EDGE_FILLET)
        return bp.part
    except Exception:  # pragma: no cover
        return wheel


def make_ots_spacer() -> Part:
    """Flanged bush between the body face and the wheel's bearing inner race."""
    hl = P.OTS_INBOARD_SPACER / 2
    ri, ro = P.OTS_BORE_D / 2 + 0.1, P.OTS_SPACER_OD / 2
    return revolved([(ri, -hl), (ri, hl), (ro, hl), (ro, -hl)])


# ---------------------------------------------------------------------------
# bearing dummy (for assembly visualisation only)
# ---------------------------------------------------------------------------
def make_bearing() -> Part:
    hw = P.BRG_W / 2
    ri, ro = P.BRG_ID / 2, P.BRG_OD / 2
    return revolved([(ri, -hw), (ri, hw), (ro, hw), (ro, -hw)])
