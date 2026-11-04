from collections import deque


def eventual_safe_nodes_kahn(graph: list[list[int]]) -> list[int]:
    """Kahn on the reversed graph, starting from terminal nodes."""
    n = len(graph)
    parents: list[list[int]] = [[] for _ in range(n)]
    outdegree = [len(children) for children in graph]
    for node, children in enumerate(graph):
        for nxt in children:
            parents[nxt].append(node)   # reversed edge nxt -> node

    queue = deque(v for v in range(n) if outdegree[v] == 0)
    safe = [False] * n
    while queue:
        node = queue.popleft()
        safe[node] = True
        for parent in parents[node]:
            outdegree[parent] -= 1      # one more child known safe
            if outdegree[parent] == 0:
                queue.append(parent)
    return [v for v in range(n) if safe[v]]
