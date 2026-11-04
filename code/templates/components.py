def count_components(graph: list[list[int]]) -> int:
    """Number of connected components of an undirected graph."""
    seen: set[int] = set()
    count = 0
    for start in range(len(graph)):
        if start in seen:
            continue
        count += 1                      # a new, untouched component
        seen.add(start)
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return count
