MOVES = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}


def min_cost_brute(grid: list[list[int]]) -> int:
    """Relax every move again and again until nothing improves."""
    rows, cols = len(grid), len(grid[0])
    INF = rows * cols
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    changed = True
    while changed:                      # Bellman-Ford style sweeps
        changed = False
        for r in range(rows):
            for c in range(cols):
                for sign, (dr, dc) in MOVES.items():
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        continue
                    w = 0 if grid[r][c] == sign else 1
                    if dist[r][c] + w < dist[nr][nc]:
                        dist[nr][nc] = dist[r][c] + w
                        changed = True
    return dist[rows - 1][cols - 1]
