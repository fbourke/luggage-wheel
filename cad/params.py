"""
Single source of truth for every dimension in the wheel.

All units mm. Change values here, re-run generate.py, everything regenerates.

Naming: *_D = diameter, *_R = radius, *_W = axial width, *_L = length.
"""

# ---------------------------------------------------------------------------
# Envelope (measured from the original wheel)
# ---------------------------------------------------------------------------
WHEEL_OD = 50.0          # measured
HUB_W = 19.0             # measured: overall hub width, face to face

# ---------------------------------------------------------------------------
# Axle / bearing (ASSUMED Ø8 axle -> 608 bearings; confirm and edit)
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
BEARING = "608"
BRG_ID, BRG_OD, BRG_W, BRG_SHOULDER_MAX = BEARINGS[BEARING]
assert BRG_ID == AXLE_D, "bearing bore must match axle"
BEARINGS_PER_WHEEL = 2

# Bearing bore in hub. Nominal = BRG_OD; the *tolerance* is what makes the
# press fit and is specified on the drawing / to the machinist, not modelled.
BORE_D = BRG_OD

# Internal shoulder that both outer races bottom against.
SHOULDER_D = 20.0
assert SHOULDER_D <= BRG_SHOULDER_MAX, "shoulder would touch bearing seal/cage"
SHOULDER_W = HUB_W - BEARINGS_PER_WHEEL * BRG_W        # 5.0 for 608 in 19 mm
assert SHOULDER_W >= 3.0, "not enough room between bearings for a shoulder"

# Inner-race spacer tube (aluminium or printed). Length = SHOULDER_W so the
# axle cap clamps inner races only. SKF shaft-abutment min for 608 is Ø9.6.
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
WHEELS_TOTAL = 8         # 4 corners x dual wheel
