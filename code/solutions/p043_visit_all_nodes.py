from collections import deque


def shortest_path_length(graph: list[list[int]]) -> int:
    """Fewest edges in a walk that visits every node at least once."""
    n = len(graph)
    full = (1 << n) - 1                 # n one-bits: everyone visited
    # A state is (node you stand on, set of visited nodes as bits).
    starts = [(node, 1 << node) for node in range(n)]
    seen = set(starts)
    queue = deque(starts)               # all n starts at distance 0
    steps = 0
    while queue:
        for _ in range(len(queue)):
            node, mask = queue.popleft()
            if mask == full:
                return steps
            for nxt in graph[node]:
                state = (nxt, mask | (1 << nxt))
                if state not in seen:   # mark when enqueued
                    seen.add(state)
                    queue.append(state)
        steps += 1
    return -1                           # only if the graph is split
