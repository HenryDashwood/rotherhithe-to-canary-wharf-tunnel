# Crossing map

One interactive map of the Rotherhithe to Canary Wharf crossing. Open `crossing_map.html` in a browser.
Every layer is a GeoJSON file in `layers/` and can be switched on and off in the top-right panel.

| Layer file | What |
|---|---|
| `ownership.geojson` | HMLR plots in the readjustment area (750 m of Durand's Wharf, Rotherhithe side), coloured by owner group |
| `tunnel_proposed.geojson` | The proposed tunnel, Durand's Wharf to the West India Docks impound lock |
| `tunnel_tfl_2017.geojson` | TfL's 2017 immersed tube option, on the dock-to-dock route IanVisits described |
| `tunnels_existing.geojson` | Jubilee line, Thames Tunnel (Overground), Rotherhithe road tunnel, DLR Lewisham tunnel, Greenwich and Woolwich foot tunnels, Elizabeth line, Blackwall Tunnel (both bores), Silvertown Tunnel |
| `tunnels_historic.geojson` | The abandoned Thames Archway driftway (1805 to 1809), Rotherhithe to Limehouse |
| `tunnels_utility.geojson` | Thames Tideway and Lee sewer tunnels |

On the map, solid lines are built, dashed lines proposed and dotted lines abandoned, and line width
scales with the bore width (`width_m`). Each feature also has `source` and `confidence`
properties (click it to see them). Anything marked **indicative** was drawn from written descriptions,
not from a published drawing.

## Rebuild

Everything is built by `../nbs/crossing_map/crossing_map.ipynb`, which writes the layers here and
`crossing_map.html`. It reads the ownership plots saved by `../nbs/02_route_and_ownership.ipynb`, so run that first.

```bash
cd nbs/crossing_map
uv run jupyter nbconvert --to notebook --execute --inplace crossing_map.ipynb
```

## Adding layers and annotations

- **New layer:** save any GeoJSON (WGS84) into `layers/` and re-run the crossing map notebook. It appears
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
- TfL 2017 immersed tube: IanVisits (8 November 2017) and TfL consultation Factsheet 2.
