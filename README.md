# Rotherhithe–Canary Wharf tunnel

The analysis behind a blog post ([writing/main.md](writing/main.md)) on building a walking and cycling
tunnel from Rotherhithe to Canary Wharf and paying for it with land readjustment.

It is an [nbdev](https://nbdev.fast.ai) project: the notebooks in `nbs/` are the source, and the code
they share is exported to the `tunnel` package.

## Notebooks

| Notebook | Blog section | Makes |
|---|---|---|
| `00_config` | | The route, catchment, assumptions and chart style (`tunnel.config`) |
| `01_data` | | Cached loaders for every input (`tunnel.data`) |
| `02_route_and_ownership` | History, Support | `route_map.png`, `land_supermajority.png` and the ownership numbers (`tunnel.ownership`) |
| `03_access` | | Travel times to Canary Wharf with and without the tunnel, `minutes_saved.png` (`tunnel.access`) |
| `04_uplift` | Funding, Viability | Hedonic price model and the uplift on existing homes (about £75m), `uplift_map.png` |
| `05_viability` | Viability | Tunnel cost (about £440m), development value and how it splits, `value_split.png`, `funding_vs_cost.png` |
| `crossing_map/crossing_map` | Illustration | The interactive map in `crossing_map/` |

Assumptions you might want to change (portals, catchment radius, walking and cycling speeds) are in
`00_config`. Development and cost assumptions are at the top of `05_viability`.

## Running

```bash
uv sync
```

Two inputs need an HM Land Registry account, so they aren't downloaded automatically. Point to them in
a `.env` file at the project root (copy `.env.example`):

- **National Polygon Service** title plans: set `NPS_DIR` to the folder of `LR_POLY_FULL_*.shp` files.
- **CCOD and OCOD** owners: the `CCOD_FULL_*.zip` and `OCOD_FULL_*.zip` bulk files, in `data/` or the folder set in `COD_DIR`.

Only `02_route_and_ownership` reads them. It saves the plots it needs to `data/derived/`, so the other
notebooks run without them. MHCLG's 2023 land value workbook goes in `data/raw/land_values_2023.xlsx`.
Everything else downloads on first run and is cached in `data/raw/`.

Run the notebooks in order, because later ones read what earlier ones save to `data/derived/`:

```bash
cd nbs && uv run jupyter nbconvert --to notebook --execute --inplace 0*.ipynb crossing_map/crossing_map.ipynb
```

After editing an exported cell (`#| export`), regenerate the package and tidy the notebooks:

```bash
uv run nbdev-export && uv run nbdev-clean
```

## Data licences

HM Land Registry data (NPS, CCOD/OCOD, Price Paid) and ONS Census 2021 data are © Crown copyright,
licensed under the OGL v3.0. Street networks and other map features are © OpenStreetMap contributors (ODbL).
