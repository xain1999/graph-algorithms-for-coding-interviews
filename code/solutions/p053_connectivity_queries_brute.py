def connectivity_queries_brute(
        n: int, operations: list[tuple[str, int, int]]) -> list[bool]:
    """Answer every "ask" with a fresh DFS over the links so far."""
    graph: list[list[int]] = [[] for _ in range(n)]
    answers: list[bool] = []
    for kind, a, b in operations:
        if kind == "link":
            graph[a].append(b)
            graph[b].append(a)
            continue
        seen = {a}
        stack = [a]
        while stack and b not in seen:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        answers.append(b in seen)
    return answers
