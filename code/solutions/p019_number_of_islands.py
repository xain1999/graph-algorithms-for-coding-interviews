DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def num_islands(grid: list[list[int]]) -> int:
    """Count groups of side-connected land cells (1 = land)."""
    grid = [row[:] for row in grid]     # we sink land: use a copy
    rows, cols = len(grid), len(grid[0])
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            islands += 1                # land no flood has reached
            grid[r][c] = 0              # sink it: marks it as seen
            stack = [(r, c)]
            while stack:
                cr, cc = stack.pop()
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1):
                        grid[nr][nc] = 0    # sink when pushed
                        stack.append((nr, nc))
    return islands
