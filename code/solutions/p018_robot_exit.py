DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def can_reach_exit(grid: list[str]) -> bool:
    """True if open cells link the top-left to the bottom-right."""
    rows, cols = len(grid), len(grid[0])
    exit_cell = (rows - 1, cols - 1)
    if grid[0][0] == "#" or grid[rows - 1][cols - 1] == "#":
        return False
    seen = {(0, 0)}                 # strings cannot be overwritten
    stack = [(0, 0)]
    while stack:
        r, c = stack.pop()
        if (r, c) == exit_cell:
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == "." and (nr, nc) not in seen):
                seen.add((nr, nc))  # mark when pushed
                stack.append((nr, nc))
    return False
