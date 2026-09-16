"""
Carriage: the aluminium body that swivels on the case's Ø10 shaft and carries
both wheels on a single Ø8 through-axle.

Frame (see params.py): X fore/aft (+X toward wheels), Y across, Z up,
Z=0 = case bottom skin, shaft axis = Z axis.
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
    Pos,
    Rectangle,
    Rot,
    Location,
    extrude,
    fillet,
)

import params as P
import wheel as W


def _cyl_y(radius: float, length: float, x: float, z: float) -> Part:
    """Cylinder along Y, centred at (x, 0, z)."""
    return Pos(x, 0, z) * Rot(90, 0, 0) * Cylinder(radius, length)


def _cyl_z(radius: float, z0: float, z1: float, x: float = 0.0) -> Part:
    """Cylinder along Z from z0 to z1 at (x, 0)."""
    return Pos(x, 0, (z0 + z1) / 2) * Cylinder(radius, abs(z1 - z0))


# ---------------------------------------------------------------------------
# body
# ---------------------------------------------------------------------------
def make_body() -> Part:
    top, bot = P.BODY_TOP_Z, P.BODY_BOTTOM_Z
    ax, az, R = P.TRAIL, P.AXLE_Z, P.NECK_REAR_R
    x0 = P.HEAD_FRONT_X

    # --- neck: side profile. Full-depth front only where the head is; below
    #     the head the front steps back to LOWER_FRONT_X; rear rounded on axle.
    hb, xl = P.HEAD_BOTTOM_Z, P.LOWER_FRONT_X
    upper = Pos((x0 + ax + R) / 2, (hb + top) / 2) * Rectangle(ax + R - x0, top - hb)
    mid = Pos((xl + ax + R) / 2, (az + hb) / 2) * Rectangle(ax + R - xl, hb - az)
    lower = Pos((xl + ax) / 2, (az + bot) / 2) * Rectangle(ax - xl, az - bot)
    rear = Pos(ax, az) * Circle(R)
    neck = extrude(Plane.XZ * (upper + mid + lower + rear), amount=P.NECK_W / 2, both=True)

    # --- head: wide block in front of the wheels, sculpted to the wheel circle
    xr = P.HEAD_REAR_X
    head = Pos((x0 + xr) / 2, 0, (hb + top) / 2) * Box(xr - x0, P.HEAD_W, top - hb)
    head -= _cyl_y(P.WHEEL_OD / 2 + P.WHEEL_CLEAR, P.HEAD_W + 10, ax, az)

    body = neck + head

    # --- vertical-edge fillets (front corners, neck rear corners)
    try:
        vert = [e for e in body.edges().filter_by(Axis.Z) if e.length > 2 * P.BODY_EDGE_R]
        body = fillet(vert, P.BODY_EDGE_R)
    except Exception as exc:  # pragma: no cover
        print(f"  ! body edge fillet failed ({exc}); continuing unfilleted")

    # --- swivel bore: bushing seat from the top, clearance bore below it,
    #     retention counterbore from the bottom
    body -= _cyl_z(P.BUSHING_BORE_D / 2, top - P.BUSHING_L, top + 1)
    body -= _cyl_z(P.SHAFT_CLEAR_BORE_D / 2, P.RETAIN_CEILING_Z - 1, top - P.BUSHING_L + 1)
    body -= _cyl_z(P.RETAIN_CBORE_D / 2, bot - 1, P.RETAIN_CEILING_Z)

    # --- axle bore through the neck
    body -= _cyl_y(P.AXLE_PIN_D / 2, P.NECK_W + 2, ax, az)
    return body


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
    hub, spacer, tire, brg = W.make_hub(), W.make_spacer(), W.make_tire(installed=True), W.make_bearing()
    z_brg = P.HUB_W / 2 - P.BRG_W / 2
    children = []

    def add(shape, label):
        shape.label = label
        children.append(shape)

    add(make_body(), "body")
    add(Pos(P.TRAIL, 0, P.AXLE_Z) * make_axle_pin(), "axle_pin")
    add(Pos(0, 0, P.BODY_TOP_Z - P.BUSHING_L) * make_bushing(), "bushing")
    add(Pos(0, 0, P.BODY_TOP_Z) * make_thrust_stack(), "thrust_AXK1024")
    add(make_shaft(), "case_shaft_ref")
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
    y_in = P.WHEEL_CENTRE_Y - P.TIRE_W / 2       # tire inner face

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

    # head rear surface is offset WHEEL_CLEAR from the tire by construction
    out.append(f"body head -> tire       : {P.WHEEL_CLEAR:5.2f} mm  (by construction)")

    # neck side faces vs tire inner faces
    out.append(f"neck face -> tire face  : {y_in - P.NECK_W / 2:5.2f} mm")

    # floor vs body bottom
    out.append(f"body bottom -> floor    : {P.BODY_BOTTOM_Z + P.LAND_TO_FLOOR:5.2f} mm")
    out.append(f"body below case skin    : {P.SKIN_Z - P.BODY_BOTTOM_Z:5.2f} mm")

    # counterbore wall
    out.append(f"counterbore wall (neck) : {P.CBORE_WALL:5.2f} mm")
    return out
