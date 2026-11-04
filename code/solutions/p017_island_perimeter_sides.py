DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def island_perimeter_sides(grid: list[list[int]]) -> int:
    """Count the land sides that face water or the edge of the map."""
    rows, cols = len(grid), len(grid[0])
    perimeter = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    perimeter += 1      # side on the map's edge
                elif grid[nr][nc] == 0:
                    perimeter += 1      # side facing water
    return perimeter
