# Crossing map

The blog's two illustrations, in the Centre for British Progress house style, with Inter and Merriweather
embedded so they render the same anywhere:

| File               | What                                                                                                                                          |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `crossing_map.svg` | Map of the crossing: the proposed tunnel, TfL's 2017 option, the tunnels already under this stretch of the Thames, and who owns the land within 750 m of the Rotherhithe portal |
| `timeline.svg`     | The tunnels under the Thames in east London by the year each was finished, ending with the proposed tunnel                                    |

Both were drafted on a Design canvas (https://claude.ai/artifact/9o3F2t9qs8jzHVzQoGQ9hT). Their label text
and positions are set in the notebook (`CARDS`, `PLACES` and `TIMELINE`), so a wording change on the canvas
needs making there too.

## Rebuild

Both are written by `../nbs/crossing_map/crossing_map.ipynb`. It reads the ownership plots saved by
`../nbs/02_route_and_ownership.ipynb`, so run that first.

```bash
cd nbs/crossing_map
uv run jupyter nbconvert --to notebook --execute --inplace crossing_map.ipynb
```

Downloads are cached in `sources/` (gitignored); delete a file there to fetch it again.

## Data sources

- Ownership: HM Land Registry NPS, CCOD and OCOD, © Crown copyright, OGL v3.0.
- Basemap (water, parks, roads), rail tunnel extents and the Rotherhithe Tunnel: OpenStreetMap contributors (ODbL), via Overpass.
- Rail lines: Oliver O'Brien's [tfl_lines.json](https://github.com/oobrien/vis/tree/master/tubecreature/data) (OpenStreetMap, ODbL).
- Thames Tideway Tunnel: safeguarding corridor from the City of London's INSPIRE map service.
- Thames Archway: [russiadock.blogspot.com](https://russiadock.blogspot.com/2015/08/before-thames-tunnel-thames-archway.html).
- TfL 2017 immersed tube: IanVisits (8 November 2017) and TfL consultation Factsheet 2.
