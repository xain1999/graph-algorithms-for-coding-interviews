DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def max_area_of_island_brute(grid: list[list[int]]) -> int:
    """Measure the island of every land cell from scratch."""
    rows, cols = len(grid), len(grid[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            seen = {(r, c)}             # fresh set for every start
            stack = [(r, c)]
            while stack:
                cr, cc = stack.pop()
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            best = max(best, len(seen))
    return best
