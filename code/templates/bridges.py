def bridges(n: int, edges: list[list[int]]) -> list[list[int]]:
    """Edges whose removal increases the number of components.
    Iterative Tarjan: low[v] = earliest discovery time
    reachable from v's subtree using one back edge."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        graph[u].append((v, i))
        graph[v].append((u, i))
    disc = [-1] * n
    low = [0] * n
    time = 0
    result: list[list[int]] = []
    for s in range(n):
        if disc[s] != -1:
            continue
        disc[s] = low[s] = time
        time += 1
        stack = [(s, -1, iter(graph[s]))]   # node, edge in, children
        while stack:
            node, via, it = stack[-1]
            for nxt, eid in it:
                if eid == via:
                    continue                # the edge we came along
                if disc[nxt] == -1:
                    disc[nxt] = low[nxt] = time
                    time += 1
                    stack.append((nxt, eid, iter(graph[nxt])))
                    break
                low[node] = min(low[node], disc[nxt])   # back edge
            else:
                stack.pop()
                if stack:
                    parent = stack[-1][0]
                    low[parent] = min(low[parent], low[node])
                    if low[node] > disc[parent]:
                        result.append([parent, node])
    return result
