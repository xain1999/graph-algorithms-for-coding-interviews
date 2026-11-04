from collections import deque


def all_paths_bfs(graph: list[list[int]]) -> list[list[int]]:
    """BFS whose queue holds whole partial paths, not nodes."""
    target = len(graph) - 1
    paths: list[list[int]] = []
    queue = deque([[0]])
    while queue:
        path = queue.popleft()
        if path[-1] == target:
            paths.append(path)
            continue
        for nxt in graph[path[-1]]:
            queue.append(path + [nxt])  # copies the whole path
    return paths
