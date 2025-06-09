import json, math

RADIUS_KM = 6371.0088

def haversine(lat1, lon1, lat2, lon2):
    """Great‑circle distance in kilometres."""
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ     = φ2 - φ1
    Δλ     = math.radians(lon2 - lon1)
    a = math.sin(Δφ/2)**2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2)**2
    return 2 * RADIUS_KM * math.asin(math.sqrt(a))

def load_capitals(path: str = "us_state_capitals_verified.json") -> dict[str, tuple[float,float]]:
    """Return {'State': (lat, lon), … , 'Washington DC': (lat, lon)}"""
    with open(path) as f:
        rows = json.load(f)           # list[dict]
    caps = {row["state"]: (row["latitude"], row["longitude"]) for row in rows}
    caps["Washington DC"] = (38.8977, -77.0365)
    return caps