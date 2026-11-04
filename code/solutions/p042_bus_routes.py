from collections import defaultdict, deque


def num_buses_to_destination(routes: list[list[int]], source: int,
                             target: int) -> int:
    """Fewest buses from source to target, or -1 if unreachable."""
    if source == target:
        return 0                        # no bus needed at all

    routes_at = defaultdict(list)       # stop -> buses that serve it
    for bus, stops in enumerate(routes):
        for stop in stops:
            routes_at[stop].append(bus)

    boarded = set(routes_at[source])    # mark when enqueued
    queue = deque(boarded)
    seen_stops = {source}
    buses = 1
    while queue:
        for _ in range(len(queue)):     # one layer = one more bus
            bus = queue.popleft()
            for stop in routes[bus]:
                if stop == target:
                    return buses
                if stop in seen_stops:
                    continue
                seen_stops.add(stop)    # scan its bus list once
                for nxt in routes_at[stop]:
                    if nxt not in boarded:
                        boarded.add(nxt)
                        queue.append(nxt)
        buses += 1
    return -1
