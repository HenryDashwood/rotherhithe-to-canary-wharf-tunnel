"""Join HMLR CCOD/OCOD corporate ownership onto the tunnel catchment polygons.

Titles with no CCOD/OCOD match are owned by private individuals (CCOD/OCOD
only cover companies, public bodies and overseas entities).

Outputs:
  tunnel_catchment_owners.gpkg - catchment polygons + tenure / proprietor fields
  tunnel_catchment_owners.csv  - same, without geometry
"""

from __future__ import annotations

import glob

import geopandas as gpd
import pandas as pd

CATCHMENT = "tunnel_catchment_400m.gpkg"
COLS = {
    "Title Number": "title_no",
    "Tenure": "tenure",
    "Property Address": "address",
    "Proprietor Name (1)": "owner",
    "Company Registration No. (1)": "company_no",
    "Proprietorship Category (1)": "owner_category",
    "Date Proprietor Added": "owner_added",
}


def load_ownership(titles: set[str]) -> pd.DataFrame:
    frames = []
    for zip_path in sorted(glob.glob("data/[CO]COD_FULL_*.zip")):
        source = "OCOD" if "OCOD" in zip_path else "CCOD"
        print(f"Reading {zip_path}")
        for chunk in pd.read_csv(zip_path, usecols=list(COLS), dtype=str, chunksize=500_000):
            chunk = chunk[chunk["Title Number"].isin(titles)].rename(columns=COLS)
            chunk["source"] = source
            frames.append(chunk)
    return pd.concat(frames, ignore_index=True).drop_duplicates("title_no")


def main() -> None:
    g = gpd.read_file(CATCHMENT)
    owners = load_ownership(set(g.title_no))
    g = g.merge(owners, on="title_no", how="left")
    g["owner_category"] = g.owner_category.fillna("Private individual(s)")

    g.to_file("tunnel_catchment_owners.gpkg", layer="owners", driver="GPKG")
    g.drop(columns="geometry").to_csv("tunnel_catchment_owners.csv", index=False)
    print(f"Matched {owners.title_no.nunique()} of {g.title_no.nunique()} titles")


if __name__ == "__main__":
    main()
