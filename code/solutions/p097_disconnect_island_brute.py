from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def count_islands(grid: list[list[int]]) -> int:
    """Number of 4-connected groups of land cells (BFS)."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                islands += 1
                seen[r][c] = True
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in DIRECTIONS:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == 1
                                and not seen[nr][nc]):
                            seen[nr][nc] = True
                            queue.append((nr, nc))
    return islands


def min_days_brute(grid: list[list[int]]) -> int:
    """Try flooding each land cell and recount the islands."""
    if count_islands(grid) != 1:
        return 0
    grid = [row[:] for row in grid]
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 1:
                grid[r][c] = 0
                split = count_islands(grid) != 1
                grid[r][c] = 1
                if split:
                    return 1
    return 2                            # a corner cell: two cuts
