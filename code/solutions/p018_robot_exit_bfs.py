from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def can_reach_exit_bfs(grid: list[str]) -> bool:
    """Same search with a queue and a matrix of booleans."""
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == "#" or grid[rows - 1][cols - 1] == "#":
        return False
    seen = [[False] * cols for _ in range(rows)]
    seen[0][0] = True
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == rows - 1 and c == cols - 1:
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == "." and not seen[nr][nc]):
                seen[nr][nc] = True
                queue.append((nr, nc))
    return False
