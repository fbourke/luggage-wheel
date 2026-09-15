"""
Render a 2D cross-section of the assembled wheel to docs/cross_section.png.

Run from repo root:  uv run cad/preview.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon as MplPoly  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
import params as P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "docs" / "cross_section.png"


def hub_profile():
    hw, zb, zf = P.HUB_W / 2, P.HUB_W / 2 - P.BRG_W, P.HUB_W / 2 - P.FLANGE_W
    rb, rs, rf, rbed = P.BORE_D / 2, P.SHOULDER_D / 2, P.FLANGE_D / 2, P.BED_D / 2
    return [(rb, -hw), (rb, -zb), (rs, -zb), (rs, zb), (rb, zb), (rb, hw),
            (rf, hw), (rf, zf), (rbed, zf), (rbed, -zf), (rf, -zf), (rf, -hw)]


def tire_profile():
    # Drawn in the *installed* (stretched) state, i.e. nominal hub dims.
    hw, zf = P.TIRE_W / 2, P.HUB_W / 2 - P.FLANGE_W
    rbed, rf, ro = P.BED_D / 2, P.FLANGE_D / 2, P.WHEEL_OD / 2
    return [(rbed, -zf), (rbed, zf), (rf, zf), (rf, hw), (ro, hw), (ro, -hw),
            (rf, -hw), (rf, -zf)]


def rect(r0, r1, z0, z1):
    return [(r0, z0), (r0, z1), (r1, z1), (r1, z0)]


def main() -> None:
    fig, ax = plt.subplots(figsize=(7, 9))
    hw = P.HUB_W / 2

    def draw(pts, color, label, alpha=0.8):
        for sign in (1, -1):  # mirror about the axle for a full section
            ax.add_patch(MplPoly([(sign * r, z) for r, z in pts], closed=True,
                                 fc=color, ec="k", lw=0.6, alpha=alpha,
                                 label=label if sign == 1 else None))

    draw(tire_profile(), "#444444", "tire (TPU 95A)")
    draw(hub_profile(), "#b0b8c4", "hub (Al 6061)")
    zb = hw - P.BRG_W
    for z0, z1 in ((zb, hw), (-hw, -zb)):
        draw(rect(P.BRG_ID / 2, P.BRG_OD / 2, z0, z1), "#f2c14e",
             f"{P.BEARING} bearing" if z0 > 0 else None, alpha=0.9)
    draw(rect(P.SPACER_ID / 2, P.SPACER_OD / 2, -P.SPACER_L / 2, P.SPACER_L / 2),
         "#7fb069", "spacer")
    draw(rect(0, P.AXLE_D / 2, -hw - 4, hw + 4), "#888888", f"axle Ø{P.AXLE_D:g}", alpha=0.4)

    # dimension annotations
    def dim_h(r, z, text):
        ax.annotate("", xy=(-r, z), xytext=(r, z), arrowprops=dict(arrowstyle="<->", lw=0.8))
        ax.text(0, z + 0.4, text, ha="center", va="bottom", fontsize=8)

    dim_h(P.WHEEL_OD / 2, hw + 6, f"Ø{P.WHEEL_OD:g} tire OD")
    dim_h(P.FLANGE_D / 2, -hw - 6.5, f"Ø{P.FLANGE_D:g} flange / Ø{P.BED_D:g} bed")
    dim_h(P.BORE_D / 2, -hw - 9.5, f"Ø{P.BORE_D:g} bearing bore (press fit)")
    ax.annotate("", xy=(P.WHEEL_OD / 2 + 4, -hw), xytext=(P.WHEEL_OD / 2 + 4, hw),
                arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(P.WHEEL_OD / 2 + 5, 0, f"{P.HUB_W:g} hub\n{P.TIRE_W:g} tire", va="center", fontsize=8)

    ax.set_aspect("equal")
    ax.set_xlim(-P.WHEEL_OD / 2 - 12, P.WHEEL_OD / 2 + 12)
    ax.set_ylim(-hw - 13, hw + 10)
    ax.axhline(0, color="k", lw=0.3, ls="--")
    ax.axvline(0, color="k", lw=0.3, ls="-.")
    ax.set_xlabel("radial (mm)")
    ax.set_ylabel("axial (mm)")
    ax.set_title(f"Wheel cross-section — {P.BEARING} x{P.BEARINGS_PER_WHEEL}, Ø{P.AXLE_D:g} axle")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, lw=0.3, alpha=0.5)
    OUT.parent.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
