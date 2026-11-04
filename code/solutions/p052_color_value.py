from collections import deque


def largest_path_value(colors: str, edges: list[list[int]]) -> int:
    """Most frequent color count on any path, or -1 on a cycle."""
    n = len(colors)
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    # count[v][c]: most nodes of color c on a path that ends at v
    count = [[0] * 26 for _ in range(n)]
    queue = deque(v for v in range(n) if indegree[v] == 0)
    seen = 0
    best = 0
    while queue:
        node = queue.popleft()          # every predecessor is done
        seen += 1
        own = ord(colors[node]) - ord("a")
        count[node][own] += 1           # the node itself
        best = max(best, count[node][own])
        for nxt in graph[node]:
            # extend to nxt, keeping the best of each color
            count[nxt] = list(map(max, count[nxt], count[node]))
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return best if seen == n else -1    # leftovers mean a cycle
