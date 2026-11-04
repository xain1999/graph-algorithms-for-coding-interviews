DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def max_area_of_island_recursive(grid: list[list[int]]) -> int:
    """Recursive DFS; safe only while islands stay small."""
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> int:
        if not (0 <= r < rows and 0 <= c < cols):
            return 0
        if grid[r][c] != 1:
            return 0
        grid[r][c] = 0                  # sink before recursing
        area = 1
        for dr, dc in DIRECTIONS:
            area += sink(r + dr, c + dc)
        return area

    best = 0
    for r in range(rows):
        for c in range(cols):
            best = max(best, sink(r, c))
    return best
