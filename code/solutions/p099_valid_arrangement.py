from collections import defaultdict


def valid_arrangement(pairs: list[list[int]]) -> list[list[int]]:
    """Order the pairs so each one starts where the previous ended."""
    graph: defaultdict[int, list[int]] = defaultdict(list)
    balance: defaultdict[int, int] = defaultdict(int)  # out - in
    for a, b in pairs:
        graph[a].append(b)
        balance[a] += 1
        balance[b] -= 1

    start = pairs[0][0]                 # any node, if all balanced
    for node, diff in balance.items():
        if diff == 1:                   # one more out than in
            start = node
            break

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
