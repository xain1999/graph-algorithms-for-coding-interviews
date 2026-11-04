from collections import defaultdict


def find_itinerary_brute(tickets: list[list[str]]) -> list[str]:
    """Backtracking: try destinations in sorted order, undo dead ends.

    Recursion depth is the number of tickets; exponential worst case.
    """
    graph: defaultdict[str, list[str]] = defaultdict(list)
    for src, dst in sorted(tickets):
        graph[src].append(dst)
    used = {src: [False] * len(dsts) for src, dsts in graph.items()}
    route = ["JFK"]

    def extend() -> bool:
        if len(route) == len(tickets) + 1:
            return True
        airport = route[-1]
        tried = set()                   # equal tickets: try one only
        for i, dst in enumerate(graph.get(airport, [])):
            if used[airport][i] or dst in tried:
                continue
            tried.add(dst)
            used[airport][i] = True
            route.append(dst)
            if extend():
                return True
            route.pop()
            used[airport][i] = False
        return False

    extend()
    return route
