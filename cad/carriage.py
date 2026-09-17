"""
Carriage: the aluminium body that swivels on the case's Ø10 shaft and carries
both wheels on a single Ø8 through-axle.

Frame (see params.py): X fore/aft (+X toward wheels), Y across, Z up,
Z=0 = the land (recess ceiling) the swivel bears on, shaft axis = Z axis.
"""

from __future__ import annotations

import math

from build123d import (
    Axis,
    Box,
    Circle,
    Compound,
    Cylinder,
    Part,
    Plane,
    Polygon,
    Polyline,
    Pos,
    Rectangle,
    Rot,
    Location,
    ThreePointArc,
    Wire,
    chamfer,
    extrude,
    fillet,
    make_face,
    revolve,
)

import params as P
import wheel as W


def _cyl_y(radius: float, length: float, x: float, z: float) -> Part:
    """Cylinder along Y, centred at (x, 0, z)."""
    return Pos(x, 0, z) * Rot(90, 0, 0) * Cylinder(radius, length)


def _cyl_z(radius: float, z0: float, z1: float, x: float = 0.0) -> Part:
    """Cylinder along Z from z0 to z1 at (x, 0)."""
    return Pos(x, 0, (z0 + z1) / 2) * Cylinder(radius, abs(z1 - z0))


def _fillet_vertical(body: Part, r: float) -> Part:
    """Fillet every Z-parallel edge longer than 2r, individually; skip failures."""
    targets = [e.center() for e in body.edges().filter_by(Axis.Z) if e.length > 2 * r]
    done = skipped = 0
    for c in targets:
        edges = body.edges().filter_by(Axis.Z)
        e = min(edges, key=lambda e: (e.center() - c).length)
        if (e.center() - c).length > 0.5:
            skipped += 1
            continue
        try:
            body = fillet([e], r)
            done += 1
        except Exception:
            skipped += 1
    if skipped:
        print(f"  ! vertical fillets: {done} done, {skipped} skipped")
    return body


# ---------------------------------------------------------------------------
# body
# ---------------------------------------------------------------------------
def make_body(fit_proto: bool = False) -> Part:
    """The machined body. fit_proto=True makes the one-piece printable
    variant: thrust stack as a solid collar, straight bore for the bare shaft
    (no bushing), and no axle bore (the wheels get fused on)."""
    top, flat = P.BODY_TOP_Z, P.BOSS_BOTTOM_Z
    ax, az = P.TRAIL, P.AXLE_Z
    hw = P.NECK_W / 2

    # --- between the wheels (neck width): side profile = boss rectangle +
    #     tangent-line arm + round about the axle
    # rectangle from the shaft axis back to the boss rear; the front is the boss cap
    boss_rect = Pos(P.BOSS_R / 2, (top + flat) / 2) * Rectangle(P.BOSS_R, top - flat)
    arm = Polygon(*P.ARM_PROFILE, align=None)
    axle_boss = Pos(ax, az) * Circle(P.AXLE_BOSS_R)
    profile = boss_rect + arm + axle_boss
    # internal corner radii where the arm meets the flat (pA) and the boss rear (pB)
    vs = profile.vertices()
    corners = [v for v in vs if (abs(v.X - P.ARM_FRONT_X) < 0.05 and abs(v.Y - flat) < 0.05)
               or (abs(v.X - P.BOSS_R) < 0.05 and abs(v.Y - P.ARM_TOP_Z) < 0.05)]
    try:
        profile = fillet(corners, P.ARM_INNER_R)
    except Exception as exc:  # pragma: no cover
        print(f"  ! arm internal fillets failed ({exc})")
    neck = extrude(Plane.XZ * profile, amount=hw, both=True)

    # --- swivel boss, plan view: half-round in front of the shaft axis, then
    #     straight tapers to the neck width. Scooped to the wheel circle where
    #     it overhangs the wheels.
    #     One closed wire (arc + taper polyline): a face union of two touching
    #     faces would extrude as two solids and break the bell intersection.
    R = P.BOSS_R
    plan = make_face(Wire([ThreePointArc((0, R), (-R, 0), (0, -R))]
                          + list(Polyline((0, -R), (P.BOSS_TAPER_X, -hw), (P.BOSS_TAPER_X, hw), (0, R)).edges())))
    boss = extrude(Plane.XY.offset(flat) * plan, amount=top - flat)
    # revolved "cap": full radius for the top band, 45° cone, stem around the bore
    bell_prof = Polygon((0, top + 0.1), (R + 0.1, top + 0.1), (R + 0.1, P.CAP_BAND_Z + 0.1), (R, P.CAP_BAND_Z),
                        (P.STEM_R, P.STEM_TOP_Z), (P.STEM_R, flat - 0.1), (0, flat - 0.1), align=None)
    boss = boss & revolve(Plane.XZ * bell_prof, Axis.Z, 360)   # NB: .intersect() returns a ShapeList here
    assert isinstance(boss, Part) and len(boss.solids()) == 1
    # scoop to the wheel circle where the cap overhangs the wheels, sparing the neck
    scoop = _cyl_y(P.WHEEL_OD / 2 + P.WHEEL_CLEAR, 2 * R + 10, ax, az)
    scoop -= Pos(0, 0, -20) * Box(200, 2 * hw, 100)
    boss -= scoop

    body = neck + boss
    assert len(body.solids()) == 1, "body did not fuse into one solid"

    # --- vertical-edge fillets (taper/neck junction, boss rear corners),
    #     one edge at a time so an awkward edge at the scoop doesn't abort all
    # --- cosmetic rounds first (they need clean topology): arm outline (edges
    #     in the neck side planes, outside the boss footprint), boss top perimeter
    def _arm_outline(b):
        return [e for e in b.edges()
                if abs(abs(e.center().Y) - hw) < 1e-3 and e.length > 0.3
                and (e.center().X > P.BOSS_R + 0.2 or e.center().Z < flat - 0.2)]
    body = _try_fillet(body, _arm_outline(body), P.ARM_EDGE_R, "arm outline")
    # cap underside edge and cone -> stem edge (arcs at those heights, in front of the axis)
    def _arcs_at(b, z):
        return [e for e in b.edges() if abs(e.center().Z - z) < 0.3 and e.center().X < 0 and e.length > 0.3]
    body = _try_fillet(body, _arcs_at(body, P.CAP_BAND_Z), P.CAP_EDGE_R, "cap edge")
    body = _try_fillet(body, _arcs_at(body, P.STEM_TOP_Z), P.STEM_EDGE_R, "cone/stem edge", convex=False)
    body = _try_fillet(body, [e for e in body.edges() if abs(e.center().Z - top) < 1e-3], P.TOP_EDGE_R, "top perimeter")
    body = _fillet_vertical(body, P.BODY_EDGE_R)

    if fit_proto:
        body += _cyl_z(P.THRUST_OD / 2, top, 0.0)                 # thrust stack as a collar
        body -= _cyl_z(P.PROTO_SHAFT_BORE_D / 2, P.STEP_CEILING_Z, 1.0)
        body -= _cyl_z(P.BOLT_HOLE_D / 2, flat - 1, P.STEP_CEILING_Z + 1)
        return body

    # --- swivel bore: bushing seat from the top, clearance bore down to the step
    v_before = body.volume
    body -= _cyl_z(P.BUSHING_BORE_D / 2, top - P.BUSHING_L, top + 1)
    assert v_before - body.volume > 0.8 * math.pi * (P.BUSHING_BORE_D / 2) ** 2 * P.BUSHING_L, \
        "bushing bore did not cut: body solid is corrupt (check fillet stages)"
    body -= _cyl_z(P.SHAFT_CLEAR_BORE_D / 2, P.STEP_CEILING_Z, top - P.BUSHING_L + 1)
    body -= _cyl_z(P.BOLT_HOLE_D / 2, flat - 1, P.STEP_CEILING_Z + 1)      # bolt shank through the step

    # --- axle bore through the arm
    body -= _cyl_y(P.AXLE_PIN_D / 2, P.NECK_W + 2, ax, az)

    # --- break every remaining sharp edge that will take it (best effort)
    if P.EDGE_BREAK > 0:
        done = 0
        for e in list(body.edges()):
            if e.length < 1.0:
                continue
            q = min(body.edges(), key=lambda k: (k.center() - e.center()).length)
            if (q.center() - e.center()).length > 0.3:
                continue
            try:
                body = chamfer([q], P.EDGE_BREAK)
                done += 1
            except Exception:
                pass
        print(f"  edge breaks applied: {done}")
    return body


def _try_fillet(body: Part, edges, r: float, label: str, convex: bool = True) -> Part:
    """Fillet a group of edges, backing off the radius; leave sharp if nothing works.

    OCCT sometimes returns a fillet result that passes is_valid but is inside-out
    (volume goes the wrong way and later booleans become no-ops). A round on a
    convex edge must remove material, on a concave edge must add it; anything
    else is rejected and the next radius tried."""
    if not edges:
        return body
    v0 = body.volume
    for rr in (r, r * 0.75, r * 0.5):
        try:
            out = fillet(edges, rr)
        except Exception:
            continue
        dv = out.volume - v0
        good = (dv < 1e-6) if convex else (dv > -1e-6)
        if good and len(out.solids()) == 1:
            return out
        print(f"  ! {label} fillet R{rr:.2f} produced a bad solid (dV={dv:+.1f}); retrying smaller")
    print(f"  ! {label} fillet failed at R{r}; left sharp")
    return body


def make_fit_proto() -> Part:
    """One-piece printable fit check: body + thrust collar + solid wheels on a
    fused axle. Screws straight onto the case with the real M5 bolt + washer.
    Wheels don't turn; the point is the recess, the swing, and the retention."""
    proto = make_body(fit_proto=True)
    axle_l = 2 * (P.WHEEL_CENTRE_Y + P.WHEEL_W / 2)
    proto += _cyl_y(P.AXLE_PIN_D / 2, axle_l, P.TRAIL, P.AXLE_Z)
    if P.OTS:
        wheel = W.make_ots_wheel() + Cylinder(P.OTS_BOSS_D / 2, P.OTS_WHEEL_W)   # fill the bore
        for side in (+1, -1):
            proto += wheel.moved(wheel_location(side))
        return proto
    tire = W.make_tire(installed=True)
    for side in (+1, -1):
        loc = wheel_location(side)
        proto += Cylinder(P.FLANGE_D / 2, P.HUB_W).moved(loc)   # solid hub
        proto += tire.moved(loc)
    return proto


# ---------------------------------------------------------------------------
# axle pin (Ø8 h6 ground shaft with two circlip grooves)
# ---------------------------------------------------------------------------
def make_axle_pin() -> Part:
    pin = Rot(90, 0, 0) * Cylinder(P.AXLE_PIN_D / 2, P.AXLE_PIN_L)
    groove = Rot(90, 0, 0) * (
        Cylinder(P.AXLE_PIN_D / 2 + 1, P.CIRCLIP_GROOVE_W)
        - Cylinder(P.CIRCLIP_GROOVE_D / 2, P.CIRCLIP_GROOVE_W + 1)
    )
    for s in (+1, -1):
        pin -= Pos(0, s * P.AXLE_GROOVE_Y, 0) * groove
    return pin


# ---------------------------------------------------------------------------
# dummies for the assembly
# ---------------------------------------------------------------------------
def make_bushing() -> Part:
    return W.revolved([
        (P.BUSHING_ID / 2, 0), (P.BUSHING_ID / 2, P.BUSHING_L),
        (P.BUSHING_OD / 2, P.BUSHING_L), (P.BUSHING_OD / 2, 0),
    ])


def make_thrust_stack() -> Part:
    return W.revolved([
        (P.THRUST_ID / 2, 0), (P.THRUST_ID / 2, P.THRUST_STACK_H),
        (P.THRUST_OD / 2, P.THRUST_STACK_H), (P.THRUST_OD / 2, 0),
    ])


def make_shaft() -> Part:
    return _cyl_z(P.SHAFT_D / 2, -P.SHAFT_PROTRUSION, 5.0)


# ---------------------------------------------------------------------------
# assembly
# ---------------------------------------------------------------------------
def wheel_location(side: int) -> Location:
    """Place a wheel-local part (axis Z) onto the axle on side +1/-1."""
    return Location((P.TRAIL, side * P.WHEEL_CENTRE_Y, P.AXLE_Z), (90, 0, 0))


def make_assembly() -> Compound:
    children = []

    def add(shape, label):
        shape.label = label
        children.append(shape)

    add(make_body(), "body")
    add(Pos(P.TRAIL, 0, P.AXLE_Z) * make_axle_pin(), "axle_pin")
    add(Pos(0, 0, P.BODY_TOP_Z - P.BUSHING_L) * make_bushing(), "bushing")
    add(Pos(0, 0, P.BODY_TOP_Z) * make_thrust_stack(), "thrust_AXK1024")
    add(make_shaft(), "case_shaft_ref")

    if P.OTS:
        wheel, spacer = W.make_ots_wheel(), W.make_ots_spacer()
        z_sp = -(P.OTS_WHEEL_W + P.OTS_INBOARD_SPACER) / 2      # inboard of the wheel
        for side in (+1, -1):
            loc = wheel_location(side)
            tag = "L" if side > 0 else "R"
            add(wheel.moved(loc), f"ots_wheel_{tag}")
            add(spacer.moved(loc * Location((0, 0, side * z_sp))), f"spacer_{tag}")
        return Compound(children=children, label="carriage")

    hub, spacer, tire, brg = W.make_hub(), W.make_spacer(), W.make_tire(installed=True), W.make_bearing()
    z_brg = P.HUB_W / 2 - P.BRG_W / 2
    for side in (+1, -1):
        loc = wheel_location(side)
        tag = "L" if side > 0 else "R"
        add(hub.moved(loc), f"hub_{tag}")
        add(tire.moved(loc), f"tire_{tag}")
        add(spacer.moved(loc), f"spacer_{tag}")
        add(brg.moved(loc * Location((0, 0, +z_brg))), f"bearing_{tag}_outer")
        add(brg.moved(loc * Location((0, 0, -z_brg))), f"bearing_{tag}_inner")
    return Compound(children=children, label="carriage")


# ---------------------------------------------------------------------------
# analytic clearance checks (fast, no booleans)
# ---------------------------------------------------------------------------
def clearance_report() -> list[str]:
    """Distances between the tire torus envelope and fixed features."""
    out = []
    r_t = P.WHEEL_OD / 2
    ax, az = P.TRAIL, P.AXLE_Z
    y_in = P.WHEEL_CENTRE_Y - P.TREAD_W / 2      # tread inner face

    # thrust washer (Ø24 disc, z in [BODY_TOP_Z, BODY_TOP_Z + stack]) vs tire
    # worst point: washer rim toward the wheel, at the washer's lowest z
    best = math.inf
    for z in (P.BODY_TOP_Z, P.BODY_TOP_Z + P.THRUST_STACK_H):
        for ang in [i * math.pi / 180 for i in range(0, 181)]:
            x, y = (P.THRUST_OD / 2) * math.cos(ang), (P.THRUST_OD / 2) * math.sin(ang)
            if abs(y) < y_in:          # inside the wheel gap: no tire there
                continue
            d = math.hypot(x - ax, z - az) - r_t
            best = min(best, d)
    out.append(f"thrust washer -> tire   : {best:5.2f} mm  ({'OK' if best >= 0.8 else 'TIGHT/INTERFERES'})")

    # recess ceiling (land) vs tire top
    out.append(f"tire top -> land        : {P.WHEEL_TOP_GAP:5.2f} mm")

    # recess wall vs wheel swing (at the skin plane, sharp-edged tire)
    out.append(f"wheel swing -> recess   : {P.SWING_MARGIN:5.2f} mm  "
               f"(swing R {P.SWING_R:.2f}, original {P.ORIG_SWING_R:.2f}, wall R {P.RECESS_R:.1f})")

    # boss scoop is offset WHEEL_CLEAR from the tire by construction
    out.append(f"boss scoop -> tire      : {P.WHEEL_CLEAR:5.2f} mm  (by construction)")

    # neck side faces vs tire inner faces
    out.append(f"neck face -> tire face  : {y_in - P.NECK_W / 2:5.2f} mm")

    # floor vs body bottom and bolt head
    out.append(f"body bottom -> floor    : {P.BODY_BOTTOM_Z + P.LAND_TO_FLOOR:5.2f} mm")
    out.append(f"bolt head -> floor      : {P.BOLT_HEAD_BOTTOM_Z + P.LAND_TO_FLOOR:5.2f} mm  (exposed under the flat)")
    out.append(f"shaft end -> step       : {P.RETAIN_LIFT_CLEARANCE:5.2f} mm float; step {P.STEP_T:g} thick, Ø{P.BOLT_HOLE_D:g} bolt hole")
    out.append(f"body below case skin    : {P.SKIN_Z - P.BODY_BOTTOM_Z:5.2f} mm")

    # bushing wall at the neck sides
    out.append(f"bushing wall (neck side): {(P.NECK_W - P.BUSHING_BORE_D) / 2:5.2f} mm")
    return out
