from collections import deque


def limited_paths_brute(n: int, edges: list[list[int]],
                        queries: list[list[int]]) -> list[bool]:
    """One BFS per query, over the edges shorter than its limit."""
    answers = []
    for u, v, limit in queries:
        graph: list[list[int]] = [[] for _ in range(n)]
        for a, b, length in edges:
            if length < limit:          # only the allowed edges
                graph[a].append(b)
                graph[b].append(a)
        seen = [False] * n
        seen[u] = True
        queue = deque([u])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    queue.append(nxt)
        answers.append(seen[v])
    return answers
