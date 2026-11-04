def all_paths(graph: list[list[int]]) -> list[list[int]]:
    """All paths from node 0 to node n - 1, by DFS backtracking."""
    target = len(graph) - 1
    paths: list[list[int]] = []
    path = [0]                          # the walk so far, shared

    def extend(node: int) -> None:
        if node == target:
            paths.append(path[:])       # save a copy, not path itself
            return
        for nxt in graph[node]:
            path.append(nxt)            # choose
            extend(nxt)                 # explore
            path.pop()                  # un-choose

    extend(0)
    return paths
