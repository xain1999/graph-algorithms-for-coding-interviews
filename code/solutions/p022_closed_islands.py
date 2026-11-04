DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def closed_island(grid: list[list[int]]) -> int:
    """Count islands of 1s that do not touch the grid's border."""
    grid = [row[:] for row in grid]     # we sink land in a copy
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        grid[r][c] = 0
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            for dr, dc in DIRECTIONS:
                nr, nc = cr + dr, cc + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == 1):
                    grid[nr][nc] = 0
                    stack.append((nr, nc))

    # 1. Sink every island that has a cell on the border.
    for r in range(rows):
        for c in range(cols):
            on_border = r in (0, rows - 1) or c in (0, cols - 1)
            if on_border and grid[r][c] == 1:
                sink(r, c)

    # 2. Whatever land is left is closed: count it as usual.
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                count += 1
                sink(r, c)
    return count
