from collections import defaultdict


def smallest_valid_arrangement(
        pairs: list[list[int]]) -> list[list[int]]:
    """Lexicographically smallest valid arrangement of the pairs."""
    graph: defaultdict[int, list[int]] = defaultdict(list)
    balance: defaultdict[int, int] = defaultdict(int)  # out - in
    for a, b in pairs:
        graph[a].append(b)
        balance[a] += 1
        balance[b] -= 1

    forced = [node for node, diff in balance.items() if diff == 1]
    start = forced[0] if forced else min(graph)  # circuit: smallest
    for targets in graph.values():
        targets.sort(reverse=True)      # pop() takes the smallest

    route: list[int] = []
    stack = [start]
    while stack:
        node = stack[-1]
        if graph[node]:
            stack.append(graph[node].pop())
        else:
            route.append(stack.pop())
    route.reverse()
    return [[route[i], route[i + 1]] for i in range(len(route) - 1)]
