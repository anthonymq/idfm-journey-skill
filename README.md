# idfm-journey-command

Small helper CLI to query Île-de-France Mobilités **PRIM / Navitia** for:
- place resolution (`/places`)
- journey search (`/journeys`)
- disruptions (`/disruptions`)

## Prereqs
- Python 3.10+
- `IDFM_PRIM_API_KEY` env var

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Resolve places:
```bash
python -m idfm places "Ivry-sur-Seine"
```

Journeys:
```bash
python -m idfm journeys --from "Ivry-sur-Seine" --to "Boulainvilliers" --count 3
```

RER C disruptions:
```bash
python -m idfm incidents --line-id line:IDFM:C01727
```

## Notes
- This project intentionally keeps output simple (text + JSON option) so it can be used by an agent.
