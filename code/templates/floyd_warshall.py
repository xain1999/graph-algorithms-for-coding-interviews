def floyd_warshall(n: int,
                   edges: list[list[int]]) -> list[list[float]]:
    """dist[i][j] for every pair of nodes (directed edges)."""
    inf = float("inf")
    dist = [[0 if i == j else inf for j in range(n)]
            for i in range(n)]
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
    for k in range(n):                  # allow k as a middle stop
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == inf:
                continue
            row = dist[i]
            for j in range(n):
                if dik + dk[j] < row[j]:
                    row[j] = dik + dk[j]
    return dist
