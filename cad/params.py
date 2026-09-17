"""
Single source of truth for every dimension in the wheel.

All units mm. Change values here, re-run generate.py, everything regenerates.

Naming: *_D = diameter, *_R = radius, *_W = axial width, *_L = length.
"""

import math
import os

# ---------------------------------------------------------------------------
# Wheel source. Two variants of the same carriage:
#   "ots"      – off-the-shelf Ø50x12 dual-spinner luggage wheels (PU tread on
#                a plastic hub, one Ø6-bore ball bearing, ~13.7 over the hub
#                bosses). Sold in 8-packs on Amazon/AliExpress; the format the
#                case shipped with. See docs/wheel_sourcing.md.   <- default
#   "machined" – our turned Al hub on 2x688 + printed TPU tire.
# Select with the WHEEL_SOURCE environment variable.
# ---------------------------------------------------------------------------
WHEEL_SOURCE = os.environ.get("WHEEL_SOURCE", "ots")
assert WHEEL_SOURCE in ("ots", "machined")
OTS = WHEEL_SOURCE == "ots"

# ---------------------------------------------------------------------------
# Envelope (measured from the original wheel)
# ---------------------------------------------------------------------------
WHEEL_OD = 50.0          # measured
HUB_W = 11.5             # measured: original wheel width, face to face
# Width is capped by the corner recess (see RECESS_R below), so we keep the
# original wheel width rather than going wider.

# ---------------------------------------------------------------------------
# Off-the-shelf wheel (generic "50 x 12 mm luggage replacement wheel")
# ---------------------------------------------------------------------------
OTS_TREAD_W = 12.0       # listed rim/tread width
OTS_WHEEL_W = 13.7       # overall, over the hub bosses (0.85 proud each side)
OTS_BOSS_D = 20.0        # hub boss diameter (estimated from photos; non-critical)
OTS_BORE_D = 6.0         # single ball bearing, Ø6 bore (626/696/606 class)
OTS_INBOARD_SPACER = 1.0 # flanged bush seated in the bearing inner race, wheel <-> body
OTS_SPACER_OD = 8.0

# ---------------------------------------------------------------------------
# Axle / bearing (machined variant: Ø8 pin -> two 688 bearings per 11.5 mm hub;
# OTS variant: Ø6 pin straight through the wheels' own bearings)
# ---------------------------------------------------------------------------
AXLE_D = OTS_BORE_D if OTS else 8.0

# Bearing catalogue: name -> (bore, OD, width, housing-shoulder max Ø per SKF)
BEARINGS = {
    "608": (8.0, 22.0, 7.0, 20.4),
    "698": (8.0, 19.0, 6.0, 17.6),
    "688": (8.0, 16.0, 5.0, 14.6),
    "626": (6.0, 19.0, 6.0, 17.4),
    "696": (6.0, 15.0, 5.0, 13.6),
}
BEARING = "688"          # 8x16x5: two of them fit an 11.5 mm hub with a 1.5 mm shoulder
BRG_ID, BRG_OD, BRG_W, BRG_SHOULDER_MAX = BEARINGS[BEARING]
assert OTS or BRG_ID == AXLE_D, "bearing bore must match axle"
BEARINGS_PER_WHEEL = 2

# Bearing bore in hub. Nominal = BRG_OD; the *tolerance* is what makes the
# press fit and is specified on the drawing / to the machinist, not modelled.
BORE_D = BRG_OD

# Internal shoulder that both outer races bottom against.
SHOULDER_D = 14.0
assert SHOULDER_D <= BRG_SHOULDER_MAX, "shoulder would touch bearing seal/cage"
SHOULDER_W = HUB_W - BEARINGS_PER_WHEEL * BRG_W        # 1.5 for 2x688 in 11.5 mm
assert SHOULDER_W >= 1.5, "not enough room between bearings for a shoulder"

# Inner-race spacer (aluminium shim ring or printed). Length = SHOULDER_W so
# the axle stack clamps inner races only. SKF shaft-abutment min for 688 ≈ Ø9.4.
SPACER_ID = AXLE_D + 0.2
SPACER_OD = 11.0
SPACER_L = SHOULDER_W

# ---------------------------------------------------------------------------
# Hub outer geometry
# ---------------------------------------------------------------------------
FLANGE_D = 38.0          # tire-retention flanges at each face
FLANGE_W = 1.5           # axial width of each flange
BED_D = 36.0             # tire seat between flanges
MIN_WALL = 3.0
assert (BED_D - BORE_D) / 2 >= MIN_WALL, "hub wall too thin over bearing"

EDGE_CHAMFER = 0.5       # all external circular edges
BORE_CHAMFER = 0.5       # lead-in for bearing press

# ---------------------------------------------------------------------------
# Tire (TPU 95A, FDM)
# ---------------------------------------------------------------------------
TIRE_SIDE_CLEAR = 0.2    # per side, so tire never rubs the housing/cap
TIRE_W = HUB_W - 2 * TIRE_SIDE_CLEAR
TIRE_STRETCH = 0.015     # print ID this fraction undersize -> stretch fit
TIRE_EDGE_FILLET = 2.0   # tread edge round-over
TIRE_MIN_THICKNESS = (WHEEL_OD - FLANGE_D) / 2
assert TIRE_MIN_THICKNESS >= 4.0, "tire too thin over flange"

# --- unified wheel-unit dimensions used by the carriage --------------------
WHEEL_W = OTS_WHEEL_W if OTS else HUB_W        # axial length the axle stack sees
TREAD_W = OTS_TREAD_W if OTS else TIRE_W       # what swings in the recess
INBOARD_T = OTS_INBOARD_SPACER if OTS else 0.5 # body face -> wheel unit
OUTBOARD_T = 0.5                               # wheel unit -> circlip side ring

# ===========================================================================
# CARRIAGE (the body that swivels on the case's Ø10 shaft and carries both
# wheels). Coordinate frame for the carriage assembly:
#   X = fore/aft, +X toward the wheels (trail direction), shaft axis at X=0
#   Y = across the case, body centred at Y=0
#   Z = up; Z=0 is the LAND: the raised plastic face (Ø20.4, with radial
#       ribs at the same height) at the ceiling of the corner recess that the
#       thrust stack bears on. The case's bottom skin is at SKIN_Z, level
#       with the shaft end; the whole shaft lives inside the recess.
#       Floor is at Z = -LAND_TO_FLOOR.
# ===========================================================================

# --- measured -------------------------------------------------------------
LAND_TO_FLOOR = 53.5       # land face to floor, on wheels
ORIG_TRAIL = 18.1          # original: shaft axis -> axle axis, horizontal
# Trail is ours to choose; the recess wall caps hypot(rear tread edge, half
# width). The OTS wheels are 2.2 mm wider over the pair, so we pull the axle
# forward to keep the swing radius at the original's. 0.32 D is still a
# healthy caster trail.
TRAIL = 16.0 if OTS else ORIG_TRAIL
SHAFT_D = 10.0             # measured 9.82: plain round, fixed to case; body swivels on it
SHAFT_PROTRUSION = 22.92   # land face -> shaft end face
SKIN_Z = -SHAFT_PROTRUSION # case bottom skin is flush with the shaft end
LAND_D = 20.39             # raised plastic land the thrust stack sits on
# Corner recess wall: quarter-circle about the shaft axis, measured ~42.4 mm
# from the shaft OD (rough, calipers). Everything above the skin plane must
# swing inside this radius.
RECESS_R = 42.4 + SHAFT_D / 2                 # 47.4
ORIG_WHEEL_GAP = 16.63     # original carriage, for reference
WHEEL_GAP = 17.0           # chosen: gap between the two wheels' inner faces
# Retention: existing M5 button-head (ISO 7380) bolt, 19 mm under head,
# threads into the shaft end.
RETAIN_BOLT = "M5 button head"
RETAIN_BOLT_HEAD_D = 9.5
RETAIN_BOLT_HEAD_H = 2.75
RETAIN_BOLT_L = 19.0

# --- derived envelope ------------------------------------------------------
AXLE_Z = -(LAND_TO_FLOOR - WHEEL_OD / 2)      # -28.5: axle centre height
WHEEL_TOP_GAP = LAND_TO_FLOOR - WHEEL_OD      # 3.5: wheel top to land
assert WHEEL_TOP_GAP >= 2.0, "wheel would touch the recess ceiling"
assert SKIN_Z > AXLE_Z, "skin plane expected above the axle (wheel partly in recess)"

# --- swivel thrust: needle roller thrust bearing + 2 hardened washers -----
# AXK1024 (10x24x2) + 2x AS1024 (10x24x1). Sits between the land and the body
# top face. Ø24 overhangs the Ø20.4 land by 1.8 mm but the radial ribs are at
# the same height, so the washer is backed.
THRUST_ID, THRUST_OD = 10.0, 24.0
THRUST_STACK_H = 2.0 + 2 * 1.0
BODY_TOP_Z = -THRUST_STACK_H                         # body top face

# --- swivel radial: Oilite (SAE 841) sleeve bushing 10 x 12 x L ----------
BUSHING_ID, BUSHING_OD = 10.0, 12.0
BUSHING_L = 15.0           # stock length; pressed flush with body top
BUSHING_BORE_D = 12.0      # H7 in body -> press fit for the bushing

# --- retention: closed bore, OEM style -----------------------------------
# The shaft clearance bore stops at an internal STEP just below the shaft end;
# only a bolt-shank hole continues through to the boss's bottom flat. The M5
# button head bears directly on that flat, so lifting the case pulls the bolt
# head against the body — no washer, and the shaft end is captured inside the
# body. The flat is open below and in front, so the bolt is reached with a
# 3 mm hex key from underneath, between the wheels.
SHAFT_CLEAR_BORE_D = SHAFT_D + 0.4   # between bushing and step; never touches the shaft
PROTO_SHAFT_BORE_D = SHAFT_D + 0.4   # one-piece printed proto: bare shaft in a plain bore (FDM prints undersize; ream if tight)
RETAIN_LIFT_CLEARANCE = 0.3          # axial float: shaft end -> step ceiling, when the case is lifted
STEP_T = 2.0                         # solid aluminium under the shaft end (carries only the carriage's own weight)
BOLT_HOLE_D = 5.5                    # M5 shank clearance through the step
STEP_CEILING_Z = -SHAFT_PROTRUSION + RETAIN_LIFT_CLEARANCE   # -22.62: shaft end floats 0.3 above this
BOSS_BOTTOM_Z = STEP_CEILING_Z - STEP_T                        # -24.62: boss bottom flat, bolt head bears here
RETAIN_CEILING_Z = STEP_CEILING_Z    # legacy name
assert (SHAFT_CLEAR_BORE_D - BOLT_HOLE_D) / 2 >= 2.0, "step annulus too narrow to carry the bolt head"
assert RETAIN_BOLT_HEAD_D > BOLT_HOLE_D + 2.0, "bolt head must overlap the step by >= 1 mm all round"
assert STEP_CEILING_Z < BODY_TOP_Z - BUSHING_L, \
    "shaft too short: bushing would run into the step"
BOLT_HEAD_BOTTOM_Z = BOSS_BOTTOM_Z - RETAIN_BOLT_HEAD_H        # -27.37, exposed

# --- body shape ------------------------------------------------------------
# Swivel boss: a round about the shaft axis, half-round in front, tapering
# into the neck behind. Arm: a round about the axle joined to the boss by two
# tangent lines. Nothing above the arm, nothing under the bolt head.
NECK_W = WHEEL_GAP - 2 * 0.5         # 16.0: body width between the wheels
WHEEL_CLEAR = 1.5                    # radial gap body <-> tire everywhere
BOSS_R = 13.0                        # covers the Ø24 thrust washer with 1 mm to spare
assert BOSS_R >= THRUST_OD / 2 + 0.5
BOSS_TAPER_X = 2.0                   # plan view: boss sides run from (0, ±BOSS_R) to (here, ±NECK_W/2)
# Where the boss overhangs the wheels (|y| > NECK_W/2) it is scooped to the
# wheel circle + WHEEL_CLEAR; this is the boss's minimum height over the tire.
_boss_wing_h = BODY_TOP_Z - (AXLE_Z + math.sqrt((WHEEL_OD / 2 + WHEEL_CLEAR) ** 2 - (BOSS_TAPER_X - TRAIL) ** 2))
assert _boss_wing_h >= 1.5, "boss wing feathers out over the wheel; reduce BOSS_TAPER_X"
AXLE_BOSS_R = 9.0                    # Ø18 round about the Ø8 axle bore -> 5 mm wall
ARM_FRONT_X = RETAIN_BOLT_HEAD_D / 2 + 1.25  # 6.0: arm leaves the flat just behind the bolt head
ARM_TOP_Z = -12.0                    # arm leaves the boss rear here (below this: arm; above: nothing)
BODY_BOTTOM_Z = AXLE_Z - AXLE_BOSS_R # -37.5, bottom of the axle boss
BODY_EDGE_R = 2.0                    # vertical-edge fillets on the body (boss taper corners)
# --- boss "cap" (revolved about the shaft axis) ----------------------------
# Full R13 only for the top band that backs the thrust washer; below it a
# 45° cone down to a stem around the bore. Ears = the rim of the cap.
CAP_T = 6.0                          # thickness of the full-radius band under the top face
STEM_R = 9.5                         # stem radius: 3.5 mm wall over the Ø12 bushing bore; meets the
                                     # neck faces at x=5.1 (33°) — keep it well clear of tangency (see design.md)
CONE_H = BOSS_R - STEM_R             # 45° cone
CAP_BAND_Z = BODY_TOP_Z - CAP_T      # -10: cap underside
STEM_TOP_Z = CAP_BAND_Z - CONE_H     # -13.5: cone -> stem
assert STEM_R > NECK_W / 2 + 1.0, "stem must stand clear of the neck faces (avoid a grazing intersection)"
assert STEM_R - BUSHING_BORE_D / 2 >= 2.5, "stem wall over the bushing bore too thin"
assert CAP_BAND_Z <= BODY_TOP_Z - 4.0, "cap band too thin to back the thrust washer"
CAP_EDGE_R = 2.0                     # round on the cap underside edge
STEM_EDGE_R = 2.0                    # round on the cone -> stem edge

# --- cosmetics / DFM --------------------------------------------------------
ARM_INNER_R = 3.0                    # internal corner radius where the arm meets the flat and the boss rear (>= tool radius, kills the stress riser)
ARM_EDGE_R = 2.5                     # round on the arm's outline edges (the "cast" look); 16 mm neck leaves 11 flat between the rounds
TOP_EDGE_R = 1.5                     # round on the boss top perimeter
EDGE_BREAK = 0.0                     # not modelled (OCCT chamfers fail on this topology); drawing note "break all edges 0.3-0.5"
assert ARM_TOP_Z > BOSS_BOTTOM_Z and ARM_TOP_Z < BODY_TOP_Z - 4
assert BOLT_HEAD_BOTTOM_Z > -LAND_TO_FLOOR + 10, "bolt head too close to the floor"


def _tangent_point(px, pz, cx, cz, r, pick):
    """Tangent point on circle (c, r) from external point p. pick(a, b) -> chosen."""
    d = math.hypot(px - cx, pz - cz)
    assert d > r, "point inside the circle"
    phi = math.atan2(pz - cz, px - cx)
    alpha = math.acos(r / d)
    cands = [(cx + r * math.cos(phi + s * alpha), cz + r * math.sin(phi + s * alpha)) for s in (+1, -1)]
    return pick(*cands)


# Side-view arm polygon (X, Z). Closed by the axle circle. Order: front-bottom
# of the flat -> underside tangent -> axle centre -> top tangent -> boss rear.
_p_a = (ARM_FRONT_X, BOSS_BOTTOM_Z)
_p_b = (BOSS_R, ARM_TOP_Z)
_t_a = _tangent_point(*_p_a, TRAIL, AXLE_Z, AXLE_BOSS_R, lambda a, b: a if a[1] < b[1] else b)   # lower
_t_b = _tangent_point(*_p_b, TRAIL, AXLE_Z, AXLE_BOSS_R, lambda a, b: a if a[0] > b[0] else b)   # upper/rear
ARM_PROFILE = [_p_a, _t_a, (TRAIL, AXLE_Z), _t_b, _p_b, (BOSS_R, BOSS_BOTTOM_Z)]
# the bolt head must stay clear of the arm underside: check at the head's rear edge
_head_rear_x = RETAIN_BOLT_HEAD_D / 2
assert _head_rear_x < ARM_FRONT_X, "arm would overlap the bolt head"

# --- wheel axle: single ground pin through the body, circlip each end -----
AXLE_PIN_D = AXLE_D                  # h6 precision shaft
SPEED_RING_T = OUTBOARD_T            # thin steel washer between wheel and circlip
# DIN 471 external retaining rings: shaft -> (groove Ø, groove width, ring thickness)
CIRCLIPS = {8.0: (7.6, 0.9, 0.8), 6.0: (5.7, 0.8, 0.7)}
CIRCLIP_GROOVE_D, CIRCLIP_GROOVE_W, CIRCLIP_T = CIRCLIPS[AXLE_PIN_D]
AXLE_END_CLEAR = 0.3                 # stack float
AXLE_END_STUB = 1.5                  # pin beyond the circlip groove
# stack from body face outward: inboard spacer | wheel unit | ring | clearance | circlip | stub
_half_stack = NECK_W / 2 + INBOARD_T + WHEEL_W + OUTBOARD_T + AXLE_END_CLEAR
AXLE_GROOVE_Y = _half_stack + CIRCLIP_GROOVE_W / 2
AXLE_PIN_L = 2 * (_half_stack + CIRCLIP_GROOVE_W + AXLE_END_STUB)
WHEEL_CENTRE_Y = NECK_W / 2 + INBOARD_T + WHEEL_W / 2
OVERALL_W = 2 * (WHEEL_CENTRE_Y + TREAD_W / 2)

# --- recess swing check ----------------------------------------------------
# The wheel's outer tread edge is the point farthest from the swivel axis.
# Above the skin plane the wheel is a chord of its circle; the widest chord
# inside the recess is at SKIN_Z. (Sharp-edge tire, conservative: the 2 mm
# tread fillet pulls the real corner in by ~0.6 mm.)
_tire_y_out = WHEEL_CENTRE_Y + TREAD_W / 2
_dz_skin = SKIN_Z - AXLE_Z
_x_rear_at_skin = TRAIL + math.sqrt((WHEEL_OD / 2) ** 2 - _dz_skin ** 2)
SWING_R = math.hypot(_x_rear_at_skin, _tire_y_out)
_orig_y_out = ORIG_WHEEL_GAP / 2 + 11.5
_orig_x_rear = ORIG_TRAIL + math.sqrt((WHEEL_OD / 2) ** 2 - _dz_skin ** 2)
ORIG_SWING_R = math.hypot(_orig_x_rear, _orig_y_out)   # what the case was built for
SWING_MARGIN = RECESS_R - SWING_R
assert SWING_R <= ORIG_SWING_R + 0.1, "wheels swing wider than the original; recess wall"
# Body (boss + arm) must clear the recess wall by a lot above the skin plane
_body_r = max(BOSS_R, math.hypot(TRAIL + AXLE_BOSS_R, NECK_W / 2))
assert _body_r < RECESS_R - 5, "body too close to the recess wall"

# ---------------------------------------------------------------------------
# Materials (for mass estimates only)
# ---------------------------------------------------------------------------
DENSITY = {              # g/mm^3
    "Al6061": 2.70e-3,
    "TPU95A": 1.21e-3,
    "PLA": 1.24e-3,
}

# ---------------------------------------------------------------------------
# Quantities
# ---------------------------------------------------------------------------
WHEELS_TOTAL = 8         # 4 corners x dual wheel (operator intends to do all four)
