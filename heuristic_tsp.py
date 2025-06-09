import json
from geo_utils import haversine, load_capitals

def nearest_neighbor(start: str, end: str, coords: dict) -> list[str]:
    unvisited = set(coords) - {start, end}
    path = [start]
    cur = start
    while unvisited:
        cur = min(unvisited, key=lambda city: haversine(*coords[cur], *coords[city]))
        path.append(cur)
        unvisited.remove(cur)
    path.append(end)
    return path

def two_opt(path: list[str], coords: dict) -> list[str]:
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if j - i == 1:           # skip adjacent edges
                    continue
                a, b, c, d = path[i-1], path[i], path[j], path[j+1]
                orig = haversine(*coords[a], *coords[b]) + haversine(*coords[c], *coords[d])
                novo = haversine(*coords[a], *coords[c]) + haversine(*coords[b], *coords[d])
                if novo + 1e-6 < orig:   # improvement
                    path[i:j+1] = reversed(path[i:j+1])
                    improved = True
        # loop until no change
    return path


def solve():
    coords = load_capitals()
    start, end = "Iowa", "Washington DC"

    # --- construct & refine route ---
    path = nearest_neighbor(start, end, coords)
    path = two_opt(path, coords)

    # --- build legs & distance ---
    legs, total = [], 0.0
    for a, b in zip(path, path[1:]):
        km = haversine(*coords[a], *coords[b])
        legs.append({"from": a, "to": b, "km": km})
        total += km

    # --- print in human‑friendly form ---
    print("ORDER OF STATES:")
    print(" -> ".join(path))
    print("\\nLEGS:")
    for idx, leg in enumerate(legs, 1):
        print(f"{idx:2d}. {leg['from']:15s} → {leg['to']:15s}: {leg['km']:.1f} km")
    print(f"\\nTOTAL DISTANCE: {total:,.1f} km")

    # --- JSON output ---
    json.dump({"route": legs, "total_km": total},
              open("politician_route_heuristic.json", "w"),
              indent=2)


if __name__ == "__main__":
    solve()




