import os
import requests

BASE_URL = "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia"


class PrimClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("IDFM_PRIM_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing IDFM_PRIM_API_KEY env var")
        self.base_url = base_url.rstrip("/")

    def get(self, path: str, params: dict | None = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        r = requests.get(url, headers={"apikey": self.api_key}, params=params, timeout=20)
        r.raise_for_status()
        return r.json()

    def places(self, q: str, count: int = 5):
        return self.get("places", {"q": q, "count": count})

    def journeys(self, from_id: str, to_id: str, count: int = 3):
        return self.get("journeys", {"from": from_id, "to": to_id, "count": count})

    def disruptions(self, filter_expr: str):
        return self.get("disruptions", {"filter": filter_expr})
