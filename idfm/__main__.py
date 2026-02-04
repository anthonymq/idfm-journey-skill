import argparse
import json
from .client import PrimClient


def _pick_best_place(places_json: dict):
    places = places_json.get("places") or []
    if not places:
        return None
    # Prefer stop_area when available
    for p in places:
        if p.get("embedded_type") == "stop_area":
            return p
    return places[0]


def cmd_places(client: PrimClient, args):
    data = client.places(args.query, count=args.count)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    best = _pick_best_place(data)
    if not best:
        print("No results")
        return
    print(f"best: {best.get('name')} ({best.get('embedded_type')} / {best.get('id')})")
    for p in (data.get("places") or [])[: args.count]:
        print(f"- {p.get('name')}\t{p.get('embedded_type')}\t{p.get('id')}")


def _summarize_journey(j: dict):
    dur = j.get("duration")
    dep = j.get("departure_date_time")
    arr = j.get("arrival_date_time")
    sections = j.get("sections") or []
    parts = []
    for s in sections:
        st = s.get("type")
        mode = (s.get("mode") or "").upper()
        name = None
        if s.get("display_informations"):
            di = s["display_informations"]
            name = " ".join(x for x in [di.get("commercial_mode"), di.get("label"), di.get("direction")] if x)
        parts.append(" - ".join(x for x in [st, mode, name] if x))
    return {
        "departure": dep,
        "arrival": arr,
        "duration_s": dur,
        "sections": parts,
    }


def cmd_journeys(client: PrimClient, args):
    from_data = client.places(args.from_query, count=5)
    to_data = client.places(args.to_query, count=5)
    from_best = _pick_best_place(from_data)
    to_best = _pick_best_place(to_data)
    if not from_best or not to_best:
        raise SystemExit("Could not resolve from/to")

    data = client.journeys(from_best["id"], to_best["id"], count=args.count)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"from: {from_best.get('name')} ({from_best.get('id')})")
    print(f"to:   {to_best.get('name')} ({to_best.get('id')})")

    journeys = data.get("journeys") or []
    if not journeys:
        print("No journeys")
        return

    for i, j in enumerate(journeys[: args.count], 1):
        s = _summarize_journey(j)
        print(f"\n#{i} dep={s['departure']} arr={s['arrival']} dur={s['duration_s']}s")
        for line in s["sections"]:
            print(f"  {line}")


def cmd_incidents(client: PrimClient, args):
    filt = args.filter
    if args.line_id:
        filt = f"line.id={args.line_id}"
    if not filt:
        raise SystemExit("Provide --line-id or --filter")

    data = client.disruptions(filt)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    disruptions = data.get("disruptions") or []
    if not disruptions:
        print("No disruptions")
        return

    for d in disruptions:
        status = d.get("status")
        severity = (d.get("severity") or {}).get("name")
        msg = (d.get("messages") or [{}])[0].get("text")
        print(f"- [{status}] {severity}: {msg}")


def main():
    p = argparse.ArgumentParser(prog="idfm")
    p.add_argument("--json", action="store_true")
    sp = p.add_subparsers(dest="cmd", required=True)

    p_places = sp.add_parser("places")
    p_places.add_argument("query")
    p_places.add_argument("--count", type=int, default=5)

    p_j = sp.add_parser("journeys")
    p_j.add_argument("--from", dest="from_query", required=True)
    p_j.add_argument("--to", dest="to_query", required=True)
    p_j.add_argument("--count", type=int, default=3)

    p_i = sp.add_parser("incidents")
    p_i.add_argument("--line-id")
    p_i.add_argument("--filter")

    args = p.parse_args()
    client = PrimClient()

    if args.cmd == "places":
        cmd_places(client, args)
    elif args.cmd == "journeys":
        cmd_journeys(client, args)
    elif args.cmd == "incidents":
        cmd_incidents(client, args)


if __name__ == "__main__":
    main()
