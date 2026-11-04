import heapq

MOVES = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}


def min_cost_dijkstra(grid: list[list[int]]) -> int:
    """Dijkstra with a heap: weight 0 along the sign, else 1."""
    rows, cols = len(grid), len(grid[0])
    INF = rows * cols
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[r][c]:
            continue
        if r == rows - 1 and c == cols - 1:
            return d
        for sign, (dr, dc) in MOVES.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = d + (0 if grid[r][c] == sign else 1)
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    raise ValueError("unreachable: every cell can be reached")
