import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def swim_in_water(grid: list[list[int]]) -> int:
    """Earliest time to swim from the top-left to the bottom-right."""
    n = len(grid)
    INF = float("inf")
    best = [[INF] * n for _ in range(n)]  # best known path height
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if t > best[r][c]:
            continue                    # stale entry
        if r == n - 1 and c == n - 1:
            return t
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                nt = max(t, grid[nr][nc])  # path cost = its max
                if nt < best[nr][nc]:
                    best[nr][nc] = nt
                    heapq.heappush(heap, (nt, nr, nc))
    raise ValueError("unreachable: a grid is always connected")
