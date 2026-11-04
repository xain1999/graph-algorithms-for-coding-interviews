def kosaraju(n: int, edges: list[list[int]]) -> list[int]:
    """Component id of every node; ids follow a topological
    order of the condensation (sources first)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    rev: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        rev[v].append(u)

    seen = [False] * n
    finish: list[int] = []
    for s in range(n):                  # pass 1: finishing order
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, iter(graph[s]))]
        while stack:
            node, it = stack[-1]
            for nxt in it:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:
                stack.pop()
                finish.append(node)

    comp = [-1] * n
    count = 0
    for s in reversed(finish):          # pass 2: on reversed edges
        if comp[s] != -1:
            continue
        comp[s] = count
        todo = [s]
        while todo:
            node = todo.pop()
            for nxt in rev[node]:
                if comp[nxt] == -1:
                    comp[nxt] = count
                    todo.append(nxt)
        count += 1
    return comp
