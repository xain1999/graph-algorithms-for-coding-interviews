def min_cost_connect_points(points: list[list[int]]) -> int:
    """Total Manhattan length of a minimum spanning tree (O(n^2))."""
    n = len(points)
    inf = float("inf")
    dist = [inf] * n        # cheapest link from v to the tree
    in_tree = [False] * n
    dist[0] = 0             # start the tree at point 0
    total = 0
    for _ in range(n):
        # Closest point outside the tree: a plain scan, no heap.
        u = -1
        for v in range(n):
            if not in_tree[v] and (u == -1 or dist[v] < dist[u]):
                u = v
        in_tree[u] = True
        total += int(dist[u])           # finite: u is reachable
        ux, uy = points[u]
        # u is in the tree now: it may offer cheaper links.
        for v in range(n):
            if not in_tree[v]:
                x, y = points[v]
                d = abs(x - ux) + abs(y - uy)
                if d < dist[v]:
                    dist[v] = d
    return total
