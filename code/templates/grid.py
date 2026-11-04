from collections.abc import Iterator

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def grid_neighbors(grid: list[list[int]], r: int,
                   c: int) -> Iterator[tuple[int, int]]:
    """In-bounds cells sharing a side with (r, c)."""
    rows, cols = len(grid), len(grid[0])
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc
