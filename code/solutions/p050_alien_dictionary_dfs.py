WHITE, GRAY, BLACK = 0, 1, 2    # unvisited, on the path, finished


def alien_order_dfs(words: list[str]) -> str:
    """Same letter graph, ordered by three-color DFS."""
    graph: dict[str, list[str]] = {}
    for word in words:
        for ch in word:
            graph.setdefault(ch, [])
    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:
                graph[a].append(b)  # duplicates are harmless here
                break
        else:
            if len(first) > len(second):
                return ""

    color = dict.fromkeys(graph, WHITE)
    finished: list[str] = []
    for start in graph:
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack = [(start, iter(graph[start]))]
        while stack:
            ch, children = stack[-1]
            for nxt in children:
                if color[nxt] == GRAY:
                    return ""       # back edge: a cycle
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:
                stack.pop()
                color[ch] = BLACK
                finished.append(ch)
    return "".join(reversed(finished))
