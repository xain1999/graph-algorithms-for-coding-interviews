def num_islands_union_find(grid: list[list[int]]) -> int:
    """Merge neighboring land cells; count the groups left."""
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))   # cell (r, c) is r * cols + c

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # shortcut as we climb
            x = parent[x]
        return x

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            islands += 1                # a new group of one cell
            for nr, nc in ((r - 1, c), (r, c - 1)):  # up and left
                if nr >= 0 and nc >= 0 and grid[nr][nc] == 1:
                    a, b = find(r * cols + c), find(nr * cols + nc)
                    if a != b:
                        parent[a] = b
                        islands -= 1    # two groups became one
    return islands
