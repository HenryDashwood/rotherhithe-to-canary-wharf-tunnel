"""Shared paths and assumptions for the tunnel value-uplift notebooks."""

from __future__ import annotations

from pathlib import Path

import pyproj

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"
for _d in (RAW, DERIVED, FIGURES):
    _d.mkdir(parents=True, exist_ok=True)

# (lon, lat)
# Durand's Wharf to the West India Docks impound lock (~460 m). Stays ~50 m south of the
# Jubilee line; the earlier Westferry Circus alignment (-0.0268760, 51.5057567) crossed it.
SOUTH_PORTAL = (-0.032771, 51.501797)  # Durand's Wharf park, Rotherhithe
NORTH_PORTAL = (-0.026450, 51.503040)  # impound lock land, Westferry Road
CANARY_WHARF = (-0.0195700, 51.5049700)  # One Canada Square: stand-in for "the jobs"

# (west, south, east, north): Rotherhithe, Bermondsey, Deptford, Isle of Dogs, Wapping
STUDY_BBOX = (-0.085, 51.470, 0.012, 51.522)

# Postcode districts whose sales form the hedonic comparison set
DISTRICTS = ["SE16", "SE8", "E14", "E1W"]
SALES_FROM = "2018-01-01"

# --- Tunnel assumptions (edit and re-run) ---------------------------------
TUNNEL_DETOUR = 1.10  # bored length / straight-line portal distance
PORTAL_DELAY_MIN = 1.5  # per portal: lift wait + ride (or escalator/ramp)
WALK_KMH = 4.8
CYCLE_KMH = 15.0

BNG = "EPSG:27700"
WGS84 = "EPSG:4326"
_to_bng = pyproj.Transformer.from_crs(WGS84, BNG, always_xy=True)


def to_bng(lonlat: tuple[float, float]) -> tuple[float, float]:
    return _to_bng.transform(*lonlat)


ACCESS_COLS = ["walk_before", "walk_after", "pt_before", "pt_after", "access_before", "access_after"]
CYCLE_COLS = ["cycle_before", "cycle_after"]


def attach_access(points):
    """Nearest street-node join of before/after travel times (from notebook 01) onto points."""
    import geopandas as gpd

    access = DERIVED / "access_nodes.gpkg"
    walk = gpd.read_file(access, layer="walk_pt")[ACCESS_COLS + ["geometry"]]
    bike = gpd.read_file(access, layer="cycle")[CYCLE_COLS + ["geometry"]]
    pts = points.to_crs(BNG)
    for layer in (walk, bike):
        pts = gpd.sjoin_nearest(pts, layer, how="left").drop(columns="index_right")
        pts = pts[~pts.index.duplicated()]  # equidistant ties
    return pts


ONS_ARCGIS = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/{}/FeatureServer/0/query"


def ons_layer(service: str, bbox=STUDY_BBOX):
    """ONS Open Geography features intersecting bbox (cached to data/raw/<service>.gpkg)."""
    import geopandas as gpd
    import requests

    path = RAW / f"{service}.gpkg"
    if path.exists():
        return gpd.read_file(path)
    frames, offset = [], 0
    while True:
        r = requests.get(
            ONS_ARCGIS.format(service),
            timeout=120,
            params={
                "where": "1=1",
                "outFields": "*",
                "f": "geojson",
                "outSR": 4326,
                "geometry": ",".join(map(str, bbox)),
                "geometryType": "esriGeometryEnvelope",
                "inSR": 4326,
                "spatialRel": "esriSpatialRelIntersects",
                "resultOffset": offset,
                "resultRecordCount": 2000,
            },
        )
        r.raise_for_status()
        gdf = gpd.read_file(r.text) if r.json().get("features") else None
        if gdf is None or gdf.empty:
            break
        frames.append(gdf)
        offset += len(gdf)
    import pandas as pd

    out = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=WGS84)
    out.to_file(path, driver="GPKG")
    return out
