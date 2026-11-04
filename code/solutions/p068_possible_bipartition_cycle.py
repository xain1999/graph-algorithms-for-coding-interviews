from collections import deque


def find_odd_cycle(n: int, dislikes: list[list[int]]) -> list[int]:
    """People around an odd cycle of dislikes, or [] if none."""
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)

    depth = [-1] * (n + 1)              # group = depth % 2
    parent = [0] * (n + 1)              # BFS tree
    for start in range(1, n + 1):
        if depth[start] != -1:
            continue
        depth[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if depth[v] == -1:
                    depth[v] = depth[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif depth[v] % 2 == depth[u] % 2:
                    # BFS: same parity means same depth, so climb
                    # both sides in step until they meet.
                    left, right = [u], [v]
                    while left[-1] != right[-1]:
                        left.append(parent[left[-1]])
                        right.append(parent[right[-1]])
                    return left + right[-2::-1]
    return []
