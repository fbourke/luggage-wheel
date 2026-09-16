"""
Single source of truth for every dimension in the wheel.

All units mm. Change values here, re-run generate.py, everything regenerates.

Naming: *_D = diameter, *_R = radius, *_W = axial width, *_L = length.
"""

import math

# ---------------------------------------------------------------------------
# Envelope (measured from the original wheel)
# ---------------------------------------------------------------------------
WHEEL_OD = 50.0          # measured
HUB_W = 11.5             # measured: original wheel width, face to face
# Width is capped by the corner recess (see RECESS_R below), so we keep the
# original wheel width rather than going wider.

# ---------------------------------------------------------------------------
# Axle / bearing: Ø8 pin -> two 688 bearings per 11.5 mm hub
# ---------------------------------------------------------------------------
AXLE_D = 8.0

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
assert BRG_ID == AXLE_D, "bearing bore must match axle"
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
TRAIL = 18.1               # shaft axis -> axle axis, horizontal
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

# --- retention counterbore from below: bolt head + washer live inside -----
# The Ø9.5 button head is smaller than the shaft, so a washer under it is what
# actually catches the body when the case is lifted. It bears on the annulus
# between the shaft clearance bore and its own OD.
SHAFT_CLEAR_BORE_D = SHAFT_D + 0.4   # between bushing and counterbore; never touches
PROTO_SHAFT_BORE_D = SHAFT_D + 0.4   # one-piece printed proto: bare shaft in a plain bore (FDM prints undersize; ream if tight)
RETAIN_WASHER_OD = 12.0    # nylon washer 6.4x12x1.6 (M6 DIN 125) on the M5 bolt
RETAIN_WASHER_T = 1.6
RETAIN_CBORE_D = 13.0
RETAIN_LIFT_CLEARANCE = 0.3          # axial float when the case is lifted
assert RETAIN_WASHER_OD > RETAIN_BOLT_HEAD_D and RETAIN_WASHER_OD < RETAIN_CBORE_D
assert RETAIN_WASHER_OD - SHAFT_CLEAR_BORE_D >= 1.2, "washer lift face too narrow"
# Ceiling of the counterbore = shaft end + washer + clearance
RETAIN_CEILING_Z = -SHAFT_PROTRUSION + RETAIN_WASHER_T + RETAIN_LIFT_CLEARANCE
assert RETAIN_CEILING_Z < BODY_TOP_Z - BUSHING_L, \
    "shaft too short: bushing would run into the retention counterbore"

# --- body shape ------------------------------------------------------------
NECK_W = WHEEL_GAP - 2 * 0.5         # 16.0: body width between the wheels
HEAD_W = 34.0                        # wider head in front of the wheels
HEAD_FRONT_X = -(THRUST_OD / 2 + 4)  # head nose, 4 mm ahead of thrust washer
HEAD_BOTTOM_Z = -20.0                # head underside; covers the full bushing length
WHEEL_CLEAR = 1.5                    # radial gap body <-> tire everywhere
HEAD_REAR_X = 4.0                    # head ends here (avoids a knife edge at the arc)
LOWER_FRONT_X = -(RETAIN_CBORE_D / 2 + 2.5)   # neck front below the head: covers the cbore wall
# thickness of the head at its rear edge, on top (arc surface -> top face)
_arc_z_at_rear = AXLE_Z + math.sqrt((WHEEL_OD / 2 + WHEEL_CLEAR) ** 2 - (HEAD_REAR_X - TRAIL) ** 2)
HEAD_REAR_THICKNESS = BODY_TOP_Z - _arc_z_at_rear
assert HEAD_REAR_THICKNESS >= 2.0, "head rear edge too thin; reduce HEAD_REAR_X"
NECK_REAR_R = 7.0                    # material behind the axle bore
BODY_BOTTOM_Z = AXLE_Z - NECK_REAR_R # neck bottom
BODY_EDGE_R = 3.0                    # vertical-edge fillets on the body
assert BODY_BOTTOM_Z < RETAIN_CEILING_Z, "counterbore would break out of the neck bottom"
CBORE_WALL = (NECK_W - RETAIN_CBORE_D) / 2
assert CBORE_WALL >= 1.5, "counterbore wall too thin in the neck"
assert HEAD_BOTTOM_Z <= BODY_TOP_Z - BUSHING_L, "head should enclose the whole bushing"

# --- wheel axle: single Ø8 ground pin through the body, circlip each end --
AXLE_PIN_D = AXLE_D                  # 8 h6 precision shaft
SPEED_RING_T = 0.5                   # 8x12x0.5 steel washer, both sides of each hub
CIRCLIP_GROOVE_W = 0.9               # DIN 471 for Ø8: groove Ø7.6 x 0.9
CIRCLIP_GROOVE_D = 7.6
CIRCLIP_T = 0.8
AXLE_END_CLEAR = 0.3                 # stack float
AXLE_END_STUB = 1.5                  # pin beyond the circlip groove
# stack from body face outward: ring | hub | ring | clearance | circlip | stub
_half_stack = NECK_W / 2 + SPEED_RING_T + HUB_W + SPEED_RING_T + AXLE_END_CLEAR
AXLE_GROOVE_Y = _half_stack + CIRCLIP_GROOVE_W / 2
AXLE_PIN_L = 2 * (_half_stack + CIRCLIP_GROOVE_W + AXLE_END_STUB)
WHEEL_CENTRE_Y = NECK_W / 2 + SPEED_RING_T + HUB_W / 2
OVERALL_W = 2 * (WHEEL_CENTRE_Y + TIRE_W / 2)

# --- recess swing check ----------------------------------------------------
# The wheel's outer tread edge is the point farthest from the swivel axis.
# Above the skin plane the wheel is a chord of its circle; the widest chord
# inside the recess is at SKIN_Z. (Sharp-edge tire, conservative: the 2 mm
# tread fillet pulls the real corner in by ~0.6 mm.)
_tire_y_out = WHEEL_CENTRE_Y + TIRE_W / 2
_dz_skin = SKIN_Z - AXLE_Z
_x_rear_at_skin = TRAIL + math.sqrt((WHEEL_OD / 2) ** 2 - _dz_skin ** 2)
SWING_R = math.hypot(_x_rear_at_skin, _tire_y_out)
_orig_y_out = ORIG_WHEEL_GAP / 2 + 11.5
ORIG_SWING_R = math.hypot(_x_rear_at_skin, _orig_y_out)   # what the case was built for
SWING_MARGIN = RECESS_R - SWING_R
assert SWING_R <= ORIG_SWING_R + 0.1, "wheels swing wider than the original; recess wall"
# Body head corners must clear the recess wall by a lot (they're all above the skin)
_head_r = math.hypot(HEAD_FRONT_X, HEAD_W / 2)
assert _head_r < RECESS_R - 5, "body head too close to the recess wall"

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
