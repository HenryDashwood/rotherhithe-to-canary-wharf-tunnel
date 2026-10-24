# Rotherhithe–Canary Wharf tunnel: land and value research

Background research for a Centre for British Progress blog pitch on funding a pedestrian/cycle
tunnel through land readjustment.

## Ownership (scripts)

| File | What |
|---|---|
| `tunnel_alignment.kml` | Assumed route: Durand's Wharf → Westferry Circus (the old bridge alignment) |
| `tunnel_catchment_400m.*` | HMLR polygons within 400 m of the route (`../find_intersecting_polygons.py`) |
| `match_ownership.py` → `tunnel_catchment_owners.*` | Joins CCOD/OCOD corporate ownership onto those polygons |
| `ownership_map.py` → `ownership_map.png` | Colour-coded ownership map for the pitch |
| `crossing_catchment.py` → `crossing_catchment_1km.*` | HMLR polygons and owners within 1 km of the TfL 2017 immersed tube entrances, for the crossing map |

## Value uplift (notebooks)

Run the notebooks in order:

1. `01_accessibility`: walk, public transport and cycling times to Canary Wharf, before and after the tunnel (OSM networks)
2. `02_prices`: Land Registry Price Paid sales since 2018 in SE16/SE8/E14/E1W, geocoded, with access times attached
3. `03_commuting`: Census 2021 home→work flows to Canary Wharf (lockdown-affected)
4. `04_uplift`: hedonic price-vs-access model, applied to Census households to estimate the uplift on existing homes
5. `05_development`: new homes that land readjustment within 750 m of the south portal could deliver
   (override with `RADIUS_M=500` etc.), valued with MHCLG land values plus the tunnel premium, phased
   and discounted to show how much reserve land could fund
6. `06_cost`: tunnel cost from three angles (TfL's 2017 option estimate, HS2 unit rates, IPA/BTS benchmark)
   with optimism bias, and the final funding-vs-cost comparison in present values. This supersedes the placeholder costs in 04/05
7. `07_crossing_map`: interactive map of the crossing (`crossing_map/crossing_map.html`) with toggleable layers for
   ownership, nearby tunnels, earlier bridge designs and the proposed portals. Each layer is a GeoJSON in `crossing_map/layers/`

Tunnel assumptions (length factor, lift delay, speeds) are in `notebooks/common.py`.

```bash
cd notebooks
uv run jupyter nbconvert --to notebook --execute --inplace 01_accessibility.ipynb
```

Raw downloads are cached in `data/raw/`, intermediate outputs go to `data/derived/`, and charts to `figures/`.

## Data licences

HM Land Registry data (NPS, CCOD/OCOD, Price Paid) and ONS Census 2021 data are © Crown copyright,
licensed under the OGL v3.0. Street networks are © OpenStreetMap contributors (ODbL).
