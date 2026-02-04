#!/usr/bin/env python3
"""Minimal PRIM/Navitia helper for Île-de-France Mobilités.

Requires:
- python3
- requests
- env IDFM_PRIM_API_KEY

This is a lightweight fallback when the companion CLI isn't installed.
"""

import argparse
import os
import sys
import requests

BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia"


def _client():
    key = os.environ.get("IDFM_PRIM_API_KEY")
    if not key:
        raise SystemExit("Missing env var IDFM_PRIM_API_KEY")
    s = requests.Session()
    s.headers.update({"apikey": key})
    return s


def places(q: str, count: int):
    s = _client()
    r = s.get(f"{BASE_URL}/places", params={"q": q, "count": count}, timeout=30)
    r.raise_for_status()
    return r.json()


def journeys(fr: str, to: str, count: int):
    s = _client()
    # resolve ids via places
    frj = places(fr, 5)
    toj = places(to, 5)

    def pick(pj):
        ps = pj.get("places") or []
        for p in ps:
            if p.get("embedded_type") == "stop_area":
                return p
        return ps[0] if ps else None

    frp = pick(frj)
    top = pick(toj)
    if not frp or not top:
        raise SystemExit("Could not resolve from/to")

    r = s.get(f"{BASE_URL}/journeys", params={"from": frp["id"], "to": top["id"], "count": count}, timeout=30)
    r.raise_for_status()
    return {"from": frp, "to": top, "journeys": r.json().get("journeys") or []}


def disruptions(filt: str):
    s = _client()
    r = s.get(f"{BASE_URL}/disruptions", params={"filter": filt}, timeout=30)
    r.raise_for_status()
    return r.json()


def main(argv):
    p = argparse.ArgumentParser(prog="idfm_prim")
    sp = p.add_subparsers(dest="cmd", required=True)

    pp = sp.add_parser("places")
    pp.add_argument("query")
    pp.add_argument("--count", type=int, default=5)

    pj = sp.add_parser("journeys")
    pj.add_argument("--from", dest="from_q", required=True)
    pj.add_argument("--to", dest="to_q", required=True)
    pj.add_argument("--count", type=int, default=3)

    pd = sp.add_parser("disruptions")
    pd.add_argument("--filter", required=True)

    args = p.parse_args(argv)

    if args.cmd == "places":
        print(places(args.query, args.count))
        return 0
    if args.cmd == "journeys":
        print(journeys(args.from_q, args.to_q, args.count))
        return 0
    if args.cmd == "disruptions":
        print(disruptions(args.filter))
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
