"""
Orthographic + isometric line renders of the carriage assembly.

Run from repo root:  uv run cad/views.py   ->  docs/carriage_views.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from build123d import Vector  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
import carriage as C  # noqa: E402
import params as P  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "docs" / "carriage_views.png"

COLORS = {
    "body": "#2b5d8c", "axle_pin": "#555555", "bushing": "#b87333",
    "thrust_AXK1024": "#c9a227", "case_shaft_ref": "#999999",
}


def color_for(label: str) -> str:
    for k, v in COLORS.items():
        if label.startswith(k):
            return v
    if label.startswith("tire"):
        return "#333333"
    if label.startswith("hub"):
        return "#7f8c9a"
    if label.startswith("bearing"):
        return "#e0b040"
    return "#444444"


def render(ax, shapes, view_dir, up, title, floor: bool):
    for shape in shapes:
        visible, hidden = shape.project_to_viewport(view_dir, up, look_at=(0, 0, 0))
        col = color_for(shape.label)
        for edges, style, lw, alpha in ((hidden, ":", 0.3, 0.25), (visible, "-", 0.7, 1.0)):
            for e in edges:
                pts = [e.position_at(t / 40) for t in range(41)]
                ax.plot([p.X for p in pts], [p.Y for p in pts], style, color=col, lw=lw, alpha=alpha)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=9)
    ax.tick_params(labelsize=7)
    ax.grid(True, lw=0.3, alpha=0.4)


def main() -> None:
    asm = C.make_assembly()
    shapes = list(asm.children)

    fig, axes = plt.subplots(2, 2, figsize=(12, 11))
    # project_to_viewport: viewport_origin is the eye position, viewport_up the up vector
    render(axes[0, 0], shapes, (0, -1000, 0), (0, 0, 1), "side view (from -Y): X fore/aft, Z up", True)
    render(axes[0, 1], shapes, (1000, 0, 0), (0, 0, 1), "rear view (from +X): Y across, Z up", True)
    render(axes[1, 0], shapes, (0, 0, 1000), (-1, 0, 0), "top view (from +Z)", False)
    body_only = [s for s in shapes if s.label in ("body", "axle_pin")]
    render(axes[1, 1], body_only, (-700, -900, 600), (0, 0, 1), "isometric — body + axle pin only", False)

    # floor + case skin lines on the side and rear views (projected coords are viewport-local)
    for a in (axes[0, 0], axes[0, 1]):
        xl = a.get_xlim()
        a.axhline(0, color="k", lw=0.8, ls="--")
        a.axhline(P.SKIN_Z, color="k", lw=0.8, ls=":")
        a.axhline(-P.LAND_TO_FLOOR, color="k", lw=0.8)
        a.text(xl[0], 0.8, "land (recess ceiling)", fontsize=7)
        a.text(xl[0], P.SKIN_Z + 0.8, "case skin / shaft end", fontsize=7)
        a.text(xl[0], -P.LAND_TO_FLOOR + 0.8, "floor", fontsize=7)

    fig.suptitle(
        f"Carriage — Ø{P.WHEEL_OD:g}x{P.HUB_W:g} wheels, trail {P.TRAIL:g}, neck {P.NECK_W:g}, "
        f"overall {P.OVERALL_W:.1f} wide, shaft {P.SHAFT_PROTRUSION:g} land→end, "
        f"recess R{P.RECESS_R:.1f} (swing margin {P.SWING_MARGIN:.1f})",
        fontsize=10,
    )
    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=130)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
