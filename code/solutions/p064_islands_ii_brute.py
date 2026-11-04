from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def count_islands(grid: list[list[int]]) -> int:
    """Number of islands, one BFS per island (Problem 19)."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1 or seen[sr][sc]:
                continue
            islands += 1
            seen[sr][sc] = True
            queue = deque([(sr, sc)])
            while queue:
                r, c = queue.popleft()
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        queue.append((nr, nc))
    return islands


def islands_after_each_brute(rows: int, cols: int,
                             added: list[list[int]]) -> list[int]:
    """Add each cell, then recount every island from scratch."""
    grid = [[0] * cols for _ in range(rows)]
    counts = []
    for r, c in added:
        grid[r][c] = 1
        counts.append(count_islands(grid))
    return counts
