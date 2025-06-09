
"""M_State_TSP — brute-force optimal tour through all ‘M’ state capitals.
   Start: Des Moines, Iowa.  End: Washington DC.
   Output: JSON with route, leg distances (km), total (km).
"""

import json
import itertools
from pathlib import Path
from distance_utils import haversine

CAPITALS_FILE = Path(__file__).with_name("us_state_capitals_verified.json")
DC_COORD = (38.8977, -77.0365)

M_STATES = [
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
]

START_STATE = "Iowa"


def load_capitals(path: Path):
    with open(path) as fp:
        data = json.load(fp)
    return {row["state"]: (row["latitude"], row["longitude"]) for row in data}


def solve(coords):
    start_coord = coords[START_STATE]
    best_total = float("inf")
    best_perm = None
    best_legs = None

    for perm in itertools.permutations(M_STATES):
        total = 0.0
        legs = []
        current = start_coord
        for state in perm:
            nxt = coords[state]
            d = haversine(current, nxt)
            total += d
            legs.append(d)
            current = nxt
        # last leg to DC
        d = haversine(current, DC_COORD)
        total += d
        legs.append(d)

        if total < best_total:
            best_total = total
            best_perm = perm
            best_legs = legs

    route = [START_STATE, *best_perm, "Washington DC"]
    return {
        "route": route,
        "legs_km": [round(d, 3) for d in best_legs],
        "total_km": round(best_total, 3),
    }


def main():
    coords = load_capitals(CAPITALS_FILE)
    result = solve(coords)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
