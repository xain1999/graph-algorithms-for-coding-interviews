def find_the_city(n: int, roads: list[list[int]],
                  threshold: int) -> int:
    """City reaching the fewest others within threshold."""
    INF = float("inf")
    dist = [[0 if i == j else INF for j in range(n)]
            for i in range(n)]
    for a, b, length in roads:          # keep the shortest road
        if length < dist[a][b]:
            dist[a][b] = dist[b][a] = length

    for k in range(n):                  # k must be the OUTER loop
        dk = dist[k]
        for i in range(n):
            dik, row = dist[i][k], dist[i]
            for j in range(n):
                if dik + dk[j] < row[j]:
                    row[j] = dik + dk[j]

    best_city, best_count = -1, n
    for i in range(n):
        count = sum(1 for j in range(n)
                    if j != i and dist[i][j] <= threshold)
        if count <= best_count:         # <=: a later city wins ties
            best_city, best_count = i, count
    return best_city
