def connects_all(n: int, chosen: list[list[int]]) -> bool:
    """DFS from computer 0 over the chosen cables."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v, _ in chosen:
        graph[u].append(v)
        graph[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen) == n


def wire_office_brute(n: int, cables: list[list[int]]) -> int:
    """Try every subset of cables; keep the cheapest that connects."""
    best = -1
    for mask in range(1 << len(cables)):
        chosen = [cables[i] for i in range(len(cables))
                  if mask >> i & 1]
        cost = sum(c for _, _, c in chosen)
        if (best == -1 or cost < best) and connects_all(n, chosen):
            best = cost
    return best
