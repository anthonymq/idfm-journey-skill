---
name: idfm-journey-command
description: Île-de-France Mobilités PRIM/Navitia journeys + disruptions helper. Use to resolve place ids, fetch next RER/metro/bus journeys between two points, and check incidents/disruptions (e.g., RER C). Requires IDFM_PRIM_API_KEY.
---

# IDFM Journey Command (PRIM/Navitia)

Use this skill to quickly query **Île-de-France Mobilités PRIM** (Navitia v2) for:
- place search (stop areas)
- journeys (next departures, arrival times, sections)
- disruptions/incidents for a line or filter

## Required config

Set env var:
- `IDFM_PRIM_API_KEY` (PRIM Marketplace API key)

Auth header used by PRIM:
- `apikey: <IDFM_PRIM_API_KEY>`

Base URL:
- `https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia`

## Quick usage (CLI)

This skill is designed to be used with the companion CLI repo:
- https://github.com/anthonymq/idfm-journey-command

Common commands:
- `idfm places "Boulainvilliers"`
- `idfm journeys --from "Boulainvilliers" --to "Ivry-sur-Seine"`
- `idfm incidents --filter "line.id=line:IDFM:C01727"`

If the CLI is not installed, you can use the bundled script below.

## Bundled script

- `scripts/idfm_prim.py`

Examples:

```bash
python3 scripts/idfm_prim.py places "Ivry-sur-Seine"
python3 scripts/idfm_prim.py journeys --from "Boulainvilliers" --to "Ivry-sur-Seine" --count 1
python3 scripts/idfm_prim.py disruptions --filter "line.id=line:IDFM:C01727"
```

## Output guidance

When replying to a human, prefer:
- next departure time, arrival time, duration
- the main public transport section (mode + line label + direction)
- only the first 1–3 journeys unless asked for more
