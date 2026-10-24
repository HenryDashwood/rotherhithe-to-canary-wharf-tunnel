"""Render a colour-coded ownership map of the tunnel catchment for the pitch.

Reads tunnel_catchment_owners.gpkg (from match_ownership.py) and writes
ownership_map.png.
"""

from __future__ import annotations

from typing import Any

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

BUFFER_M = 400

# (label, colour); order is legend order.
GROUPS = {
    "southwark": ("Southwark Council", "#d62728"),
    "tower_hamlets": ("Tower Hamlets Council", "#ff9896"),
    "canary_wharf": ("Canary Wharf Group", "#1f77b4"),
    "public_body": ("TfL / Canal & River Trust", "#9467bd"),
    "pla": ("Port of London Authority (riverbed)", "#aec7e8"),
    "housing": ("Housing associations", "#2ca02c"),
    "company": ("Other companies", "#ff7f0e"),
    "private": ("Private individuals", "#bdbdbd"),
}


def classify(row) -> str:
    owner = str(row.owner or "").upper()
    cat = str(row.owner_category)
    if "SOUTHWARK" in owner:
        return "southwark"
    if "TOWER HAMLETS" in owner:
        return "tower_hamlets"
    if "PORT OF LONDON" in owner:
        return "pla"
    if "CANARY WHARF" in owner or "HERON QUAYS" in owner:
        return "canary_wharf"
    if "TRANSPORT FOR LONDON" in owner or "CANAL & RIVER" in owner:
        return "public_body"
    if any(
        k in cat
        for k in ("Housing Association", "Community Benefit", "Registered Society", "Industrial and Provident")
    ):
        return "housing"
    if cat == "Private individual(s)":
        return "private"
    return "company"


def main() -> None:
    g = gpd.read_file("tunnel_catchment_owners.gpkg")
    g = g[g.top_level].copy()
    g["group"] = g.apply(classify, axis=1)

    route = gpd.read_file("tunnel_alignment.kml").force_2d().to_crs(27700)
    area = route.buffer(BUFFER_M).union_all()
    g = gpd.clip(g, area)

    # Big plots first so smaller ones sit on top; among identical footprints
    # draw freeholds last so they win over leases registered on the same shape.
    g["freehold"] = g.tenure.eq("Freehold")
    g = g.sort_values(["area_m2", "freehold"], ascending=[False, True])
    g = g.to_crs(3857)

    fig, ax = plt.subplots(figsize=(12, 10))
    g.plot(ax=ax, color=g.group.map(lambda k: GROUPS[k][1]), edgecolor="white", linewidth=0.3, alpha=0.85)
    gpd.GeoSeries([area], crs=27700).to_crs(3857).boundary.plot(ax=ax, color="#555", linewidth=1, linestyle="--")

    r = route.to_crs(3857)
    r.plot(ax=ax, color="black", linewidth=3.5)
    (sx, sy), (nx, ny) = r.geometry.iloc[0].coords[0], r.geometry.iloc[0].coords[-1]
    ax.scatter([sx, nx], [sy, ny], s=90, color="black", zorder=5)
    label: dict[str, Any] = {
        "fontsize": 11,
        "fontweight": "bold",
        "zorder": 6,
        "bbox": {"boxstyle": "round,pad=0.25", "fc": "white", "ec": "none", "alpha": 0.85},
    }
    ax.annotate(
        "Durand's Wharf\n(Rotherhithe)", (sx, sy), xytext=(-75, -10), textcoords="offset points", ha="center", **label
    )
    ax.annotate(
        "Westferry Circus\n(Canary Wharf)",
        (nx, ny),
        xytext=(110, 40),
        textcoords="offset points",
        ha="center",
        **label,
    )

    ax.set_axis_off()

    handles: list[Patch | Line2D] = [Patch(facecolor=c, label=l) for l, c in GROUPS.values()]
    handles.append(Line2D([0], [0], color="black", lw=3.5, label="Proposed tunnel"))
    handles.append(Line2D([0], [0], color="#555", lw=1, ls="--", label=f"{BUFFER_M} m catchment"))
    ax.legend(handles=handles, loc="lower right", fontsize=10, framealpha=0.95, title="Registered owner")

    ax.set_title(
        "Who owns the land around a Rotherhithe–Canary Wharf tunnel?", fontsize=16, fontweight="bold", loc="left"
    )
    fig.text(
        0.01,
        0.01,
        "Contains HM Land Registry data © Crown copyright and database right 2026, licensed under the OGL v3.0. "
        "Contains OS data © Crown copyright 2026.\n"
        "Titles not in CCOD/OCOD assumed privately owned; where plots overlap, the smallest/freehold is shown.",
        fontsize=7.5,
        color="#555",
        va="bottom",
    )
    fig.savefig("ownership_map.png", dpi=200, bbox_inches="tight")


if __name__ == "__main__":
    main()
