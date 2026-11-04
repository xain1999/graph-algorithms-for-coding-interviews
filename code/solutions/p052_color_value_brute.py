def largest_path_value_brute(colors: str,
                             edges: list[list[int]]) -> int:
    """Walk every simple path from every node (tiny inputs only)."""
    n = len(colors)
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    on_path = [False] * n
    tally = [0] * 26                    # colors on the current path
    best = 0
    found_cycle = False

    def walk(node: int) -> None:
        nonlocal best, found_cycle
        c = ord(colors[node]) - ord("a")
        on_path[node] = True
        tally[c] += 1
        best = max(best, tally[c])
        for nxt in graph[node]:
            if on_path[nxt]:
                found_cycle = True      # an edge back into the path
            else:
                walk(nxt)
        tally[c] -= 1                   # undo before backtracking
        on_path[node] = False

    for start in range(n):
        walk(start)
    return -1 if found_cycle else best
