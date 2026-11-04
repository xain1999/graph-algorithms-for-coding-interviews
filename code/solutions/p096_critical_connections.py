def critical_connections(
        n: int, connections: list[list[int]]) -> list[list[int]]:
    """Bridges of a connected graph (Tarjan's low-link, iterative)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in connections:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n         # discovery time, -1 = not visited yet
    low = [0] * n           # earliest disc reachable from the subtree
    parent = [-1] * n
    bridges: list[list[int]] = []
    time = 0
    disc[0] = low[0] = time
    stack = [(0, iter(graph[0]))]
    while stack:
        node, children = stack[-1]
        for nxt in children:
            if disc[nxt] == -1:                 # tree edge: go down
                time += 1
                disc[nxt] = low[nxt] = time
                parent[nxt] = node
                stack.append((nxt, iter(graph[nxt])))
                break
            if nxt != parent[node]:             # back edge
                low[node] = min(low[node], disc[nxt])
        else:                                   # node is finished
            stack.pop()
            if stack:
                up = stack[-1][0]
                low[up] = min(low[up], low[node])
                if low[node] > disc[up]:        # no way around
                    bridges.append([up, node])
    return bridges
