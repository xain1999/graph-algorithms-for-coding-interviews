from collections import defaultdict


def find_itinerary(tickets: list[list[str]]) -> list[str]:
    """Smallest route from JFK that uses every ticket exactly once."""
    graph: defaultdict[str, list[str]] = defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)
    for dests in graph.values():
        dests.sort(reverse=True)        # smallest destination last

    route: list[str] = []
    stack = ["JFK"]
    while stack:
        airport = stack[-1]
        if graph[airport]:              # an unused ticket: fly on
            stack.append(graph[airport].pop())
        else:                           # stuck: airport is final here
            route.append(stack.pop())
    return route[::-1]
