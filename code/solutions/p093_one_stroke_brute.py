def can_draw_in_one_stroke_brute(n: int,
                                 segments: list[list[int]]) -> bool:
    """Try every start point and every order of segments."""
    m = len(segments)
    if m == 0:
        return True
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(segments):
        graph[u].append((v, i))
        graph[v].append((u, i))
    used = [False] * m

    def extend(node: int, drawn: int) -> bool:
        if drawn == m:
            return True
        for nxt, i in graph[node]:
            if not used[i]:
                used[i] = True
                if extend(nxt, drawn + 1):
                    return True
                used[i] = False         # undo and try another
        return False

    return any(extend(start, 0) for start in range(n) if graph[start])
