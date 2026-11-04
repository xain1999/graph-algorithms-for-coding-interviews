from collections import deque

# Eight neighbors: four sides and four corners.
DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))


def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """Cells on the shortest clear corner-to-corner path, or -1."""
    n = len(grid)
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    dist = [[0] * n for _ in range(n)]  # 0 = not reached yet
    dist[0][0] = 1                      # a path counts its cells
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist[r][c]
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n
                    and grid[nr][nc] == 0 and dist[nr][nc] == 0):
                dist[nr][nc] = dist[r][c] + 1   # mark on enqueue
                queue.append((nr, nc))
    return -1
