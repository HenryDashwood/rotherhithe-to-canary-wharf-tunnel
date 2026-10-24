# Crossing map

One interactive map of the Rotherhithe to Canary Wharf crossing. Open `crossing_map.html` in a browser.
Every layer is a GeoJSON file in `layers/` and can be switched on and off in the top-right panel.

| Layer file | What | Made by |
|---|---|---|
| `ownership.geojson` | HMLR plots in the 400 m catchment, coloured by owner group | notebook 07, from `../tunnel_catchment_owners.gpkg` and `classify()` in `../ownership_map.py` |
| `tunnels_existing.geojson` | Jubilee line, Thames Tunnel (Overground), Rotherhithe road tunnel, DLR Lewisham tunnel, Greenwich and Woolwich foot tunnels, Elizabeth line, Blackwall Tunnel (both bores), Silvertown Tunnel | notebook 07 |
| `tunnels_historic.geojson` | The abandoned Thames Archway driftway (1805 to 1809), Rotherhithe to Limehouse | notebook 07 |
| `bridge_*.geojson` | Main spans, approach spans, ramps and landings of Sustrans 2016, TfL's three 2017 options and TfL's 2019 design | notebook 07 |

On the map, solid lines are built, dashed lines proposed and dotted lines abandoned, and line width
scales with the bore or deck width (`width_m`). Each feature also has `source` and `confidence`
properties (click it to see them). Anything marked **indicative** was drawn from written descriptions,
not from a published drawing. No bridge drawings were ever published, so all bridge geometry is indicative; the landing sites
themselves are documented (see `research/sustrans-bridge-landing-sites.md` in the project files).

## Rebuild

Everything is built by `../notebooks/07_crossing_map.ipynb`, which writes the layers here and `crossing_map.html`:

```bash
cd notebooks
uv run jupyter nbconvert --to notebook --execute --inplace 07_crossing_map.ipynb
uv run jupyter trust 07_crossing_map.ipynb   # only needed in Jupyter itself; VS Code ignores it
```

## Adding layers and annotations

- **New layer:** save any GeoJSON (WGS84) into `layers/` and re-run notebook 07. It appears
  automatically with a default style; add it to `LAYER_STYLES` in the notebook to name and colour it.
- **Annotating:** draw on the map with the tools on the left, click **Export** (top right) to download
  the drawings as `annotations.geojson`, move that file into `layers/`, and rebuild. Give features
  `name` and `note` properties (in QGIS or geojson.io) and they show in popups.
- **Measuring:** the ruler tool measures distances and areas; the cursor position shows bottom right.

## Data sources

- Ownership: HM Land Registry NPS, CCOD and OCOD, © Crown copyright, OGL v3.0.
- Rail tunnel lines: OpenStreetMap contributors (ODbL), via Oliver O'Brien's
  [tfl_lines.json](https://github.com/oobrien/vis/tree/master/tubecreature/data), cached in `sources/`.
- Rotherhithe Tunnel shafts, Greenwich and Woolwich foot tunnel entrances, Blackwall Tunnel portals, Silvertown Tunnel midpoint: Wikipedia coordinates.
- Thames Archway: [russiadock.blogspot.com](https://russiadock.blogspot.com/2015/08/before-thames-tunnel-thames-archway.html).
- Bridge designs: TfL consultation Factsheet 3 (2017), ICE review for TfL (April 2019), Building,
  East London Advertiser, road.cc, Southwark News.
