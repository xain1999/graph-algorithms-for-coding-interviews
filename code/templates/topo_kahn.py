from collections import deque


def topo_order(n: int, edges: list[list[int]]) -> list[int]:
    """Kahn's algorithm: an order with u before v for every edge
    [u, v], or [] if the graph has a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    queue = deque(v for v in range(n) if indegree[v] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()          # nothing left points to it
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1          # remove the edge node -> nxt
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []
