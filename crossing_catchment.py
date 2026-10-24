"""HMLR plots and owners within RADIUS_M of the TfL 2017 immersed tube entrances.

Scans the National Polygon Service shapefiles for polygons that touch the
catchment (a RADIUS_M circle round each entrance), adds the same `side`,
`area_m2` and `top_level` fields as tunnel_catchment_400m.gpkg, then joins
CCOD/OCOD owners as match_ownership.py does.

Outputs:
  crossing_catchment_1km.gpkg - polygons + owner fields (EPSG:27700)
  crossing_catchment_1km.csv  - same, without geometry
"""

from __future__ import annotations

import glob
import os
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from shapely.geometry import Point
from shapely.ops import linemerge, split

from match_ownership import load_ownership

NSD_DIR = "/Users/henrydashwood/serac/plp-mono/local_data/NSD_FULL_2026_03"
# Ramp heads of the immersed tube in notebooks/07_crossing_map (BNG)
ENTRANCES = {
    "south": (536565, 180175),  # Nelson Dock, Rotherhithe Street
    "north": (537111, 180094),  # impound lock inlet, Westferry Road
}
RADIUS_M = 1000
OUT = "crossing_catchment_1km"


THAMES = Path(__file__).parent / "data" / "raw" / "thames.gpkg"


def catchment_area() -> shapely.Geometry:
    return shapely.union_all([Point(xy).buffer(RADIUS_M) for xy in ENTRANCES.values()])


def rotherhithe_side() -> shapely.Geometry:
    """The part of the catchment south of the Thames centre line."""
    river = linemerge(gpd.read_file(THAMES).to_crs("EPSG:27700").union_all())
    south = Point(ENTRANCES["south"])
    return next(p for p in split(catchment_area(), river).geoms if p.contains(south))


def top_level(g: gpd.GeoDataFrame) -> np.ndarray:
    """False for plots at least 80% covered by a single larger plot (sub-titles, leases)."""
    left, right = g.sindex.query(g.geometry, predicate="intersects")
    area = g.area_m2.to_numpy()
    bigger = area[right] > area[left] * 1.05
    left, right = left[bigger], right[bigger]
    overlap = shapely.intersection(g.geometry.values[left], g.geometry.values[right])
    cover = shapely.area(overlap) / area[left]
    covered = np.zeros(len(g), dtype=bool)
    covered[left[cover >= 0.8]] = True
    return ~covered


def main() -> None:
    area = catchment_area()
    bbox = area.bounds
    hits = []
    for shp in sorted(glob.glob(os.path.join(NSD_DIR, "LR_POLY_FULL_*_[0-9].shp"))):
        part = gpd.read_file(shp, bbox=bbox, engine="pyogrio")
        part = part[part.intersects(area)]
        print(f"{os.path.basename(shp)}: {len(part)} polygons")
        hits.append(part)

    g = gpd.GeoDataFrame(pd.concat(hits, ignore_index=True), crs="EPSG:27700")
    g = g.drop_duplicates("POLY_ID")
    g.columns = [c.lower() if c.isupper() else c for c in g.columns]
    g = g.sort_values("poly_id").reset_index(drop=True)
    g["geometry"] = shapely.make_valid(g.geometry.values)

    pts = g.geometry.representative_point()
    dist = {side: pts.distance(Point(xy)) for side, xy in ENTRANCES.items()}
    g["side"] = np.where(dist["south"] < dist["north"], "south", "north")
    g["area_m2"] = g.area
    g["top_level"] = top_level(gpd.GeoDataFrame(g, geometry="geometry", crs="EPSG:27700"))

    owners = load_ownership(set(g.title_no))
    g = g.merge(owners, on="title_no", how="left")
    g["owner_category"] = g.owner_category.fillna("Private individual(s)")

    g.to_file(f"{OUT}.gpkg", layer="owners", driver="GPKG")
    g.drop(columns="geometry").to_csv(f"{OUT}.csv", index=False)
    print(
        f"{len(g)} polygons, {int(g.top_level.sum())} top-level; matched {owners.title_no.nunique()} of {g.title_no.nunique()} titles"
    )


if __name__ == "__main__":
    main()
