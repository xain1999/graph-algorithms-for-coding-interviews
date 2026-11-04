DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def oranges_rotting_brute(grid: list[list[int]]) -> int:
    """Simulate minute by minute, rescanning the grid each time."""
    grid = [row[:] for row in grid]
    rows, cols = len(grid), len(grid[0])

    def touches_rotten(r: int, c: int) -> bool:
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 2):
                return True
        return False

    minutes = 0
    while True:
        # Snapshot first: oranges rotting now must not spread yet.
        to_rot = [(r, c) for r in range(rows) for c in range(cols)
                  if grid[r][c] == 1 and touches_rotten(r, c)]
        if not to_rot:
            break
        for r, c in to_rot:
            grid[r][c] = 2
        minutes += 1

    return -1 if any(1 in row for row in grid) else minutes
