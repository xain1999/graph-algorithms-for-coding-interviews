def equations_possible_brute(equations: list[str]) -> bool:
    """For each inequality, search the equality graph for a path."""
    graph: dict[str, list[str]] = {}
    for eq in equations:
        if eq[1] == "=":
            graph.setdefault(eq[0], []).append(eq[3])
            graph.setdefault(eq[3], []).append(eq[0])

    for eq in equations:
        if eq[1] != "!":
            continue
        start, goal = eq[0], eq[3]
        seen, stack = {start}, [start]
        while stack:                    # DFS from start
            letter = stack.pop()
            if letter == goal:
                return False            # forced equal, yet !=
            for nxt in graph.get(letter, []):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return True
