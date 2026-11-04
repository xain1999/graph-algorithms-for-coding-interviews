def count_scc_tarjan(n: int, edges: list[list[int]]) -> int:
    """Number of strongly connected components in one DFS (Tarjan)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    disc = [-1] * n         # discovery time, -1 = not seen yet
    low = [0] * n           # smallest disc reachable on the stack
    on_stack = [False] * n
    pending: list[int] = []     # nodes in no finished component yet
    time = count = 0
    for root in range(n):
        if disc[root] != -1:
            continue
        disc[root] = low[root] = time
        time += 1
        pending.append(root)
        on_stack[root] = True
        stack = [(root, iter(graph[root]))]
        while stack:
            node, children = stack[-1]
            for nxt in children:
                if disc[nxt] == -1:
                    disc[nxt] = low[nxt] = time
                    time += 1
                    pending.append(nxt)
                    on_stack[nxt] = True
                    stack.append((nxt, iter(graph[nxt])))
                    break
                if on_stack[nxt]:
                    low[node] = min(low[node], disc[nxt])
            else:
                stack.pop()
                if stack:
                    parent = stack[-1][0]
                    low[parent] = min(low[parent], low[node])
                if low[node] == disc[node]:     # node is a root
                    count += 1
                    while True:
                        member = pending.pop()
                        on_stack[member] = False
                        if member == node:
                            break
    return count
