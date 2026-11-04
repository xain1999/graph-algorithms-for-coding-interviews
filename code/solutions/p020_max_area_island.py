DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def max_area_of_island(grid: list[list[int]]) -> int:
    """Size of the largest 4-connected group of 1s (0 if none)."""
    grid = [row[:] for row in grid]     # we sink land in a copy
    rows, cols = len(grid), len(grid[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            grid[r][c] = 0              # sink when pushed
            stack = [(r, c)]
            area = 0
            while stack:
                cr, cc = stack.pop()
                area += 1               # count when popped
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1):
                        grid[nr][nc] = 0
                        stack.append((nr, nc))
            best = max(best, area)
    return best
