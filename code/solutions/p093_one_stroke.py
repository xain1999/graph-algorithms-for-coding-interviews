def can_draw_in_one_stroke(n: int, segments: list[list[int]]) -> bool:
    """True if the segments form one trail (Euler's degree test)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in segments:
        graph[u].append(v)
        graph[v].append(u)
    odd = sum(len(nbrs) % 2 for nbrs in graph)
    if odd > 2:                 # odd points must be the pen's ends
        return False

    inked = [node for node in range(n) if graph[node]]
    if not inked:               # an empty drawing needs no stroke
        return True
    seen = {inked[0]}
    stack = [inked[0]]
    while stack:
        node = stack.pop()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen) == len(inked)  # all inked points in one piece
