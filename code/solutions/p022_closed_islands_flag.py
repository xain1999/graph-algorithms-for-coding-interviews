DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def closed_island_flag(grid: list[list[int]]) -> int:
    """One search per island; count those that miss the edge."""
    rows, cols = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or (r, c) in seen:
                continue
            seen.add((r, c))
            stack = [(r, c)]
            closed = True
            while stack:                # finish the whole island
                cr, cc = stack.pop()
                if cr in (0, rows - 1) or cc in (0, cols - 1):
                    closed = False
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            if closed:
                count += 1
    return count
