from collections import deque


def is_rooted_tree(n: int, edges: list[list[int]]) -> bool:
    """One root, one parent for everyone else, all reachable."""
    indegree = [0] * (n + 1)
    children: list[list[int]] = [[] for _ in range(n + 1)]
    for u, v in edges:
        indegree[v] += 1
        children[u].append(v)
    roots = [x for x in range(1, n + 1) if indegree[x] == 0]
    if len(roots) != 1 or max(indegree) > 1:
        return False
    seen = {roots[0]}
    queue = deque(roots)
    while queue:
        node = queue.popleft()
        for child in children[node]:
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return len(seen) == n


def find_redundant_directed_brute(
        edges: list[list[int]]) -> list[int]:
    """Delete each edge, the last one first, until a tree is left."""
    n = len(edges)
    for i in range(n - 1, -1, -1):
        if is_rooted_tree(n, edges[:i] + edges[i + 1:]):
            return edges[i]
    raise ValueError("input is not a rooted tree plus one edge")
