def island_perimeter(grid: list[list[int]]) -> int:
    """Island perimeter: 4 per land cell, minus 2 per shared side."""
    rows, cols = len(grid), len(grid[0])
    land = shared = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            land += 1
            # Look right and down only, so each pair is seen once.
            if c + 1 < cols and grid[r][c + 1] == 1:
                shared += 1
            if r + 1 < rows and grid[r + 1][c] == 1:
                shared += 1
    return 4 * land - 2 * shared
