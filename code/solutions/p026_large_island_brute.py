DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def max_area(grid: list[list[int]]) -> int:
    """Area of the largest island (one flood per island)."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    best = 0
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1 or seen[sr][sc]:
                continue
            seen[sr][sc] = True
            stack, area = [(sr, sc)], 0
            while stack:
                r, c = stack.pop()
                area += 1
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            best = max(best, area)
    return best


def largest_island_brute(grid: list[list[int]]) -> int:
    """Flip each water cell in turn and measure from scratch."""
    work = [row[:] for row in grid]
    best = max_area(work)               # in case there is no water
    for r, row in enumerate(work):
        for c, value in enumerate(row):
            if value == 0:
                work[r][c] = 1          # try it ...
                best = max(best, max_area(work))
                work[r][c] = 0          # ... and undo it
    return best
