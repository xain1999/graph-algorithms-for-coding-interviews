from collections import deque


def find_smallest_set_of_vertices_brute(
        n: int, edges: list[list[int]]) -> list[int]:
    """BFS from every node; keep the nodes no other node reaches."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for frm, to in edges:
        graph[frm].append(to)

    reached_by_other = [False] * n
    for start in range(n):
        seen = {start}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    reached_by_other[nxt] = True
                    queue.append(nxt)
    return [node for node in range(n) if not reached_by_other[node]]
