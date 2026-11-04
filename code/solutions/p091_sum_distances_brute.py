from collections import deque


def sum_of_distances_brute(n: int,
                           edges: list[list[int]]) -> list[int]:
    """Run a BFS from every node and add up its distances."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    answer = []
    for start in range(n):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if dist[nxt] == -1:
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
        answer.append(sum(dist))
    return answer
