DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def min_days(grid: list[list[int]]) -> int:
    """Fewest land cells to flood so the grid is not one island."""
    rows, cols = len(grid), len(grid[0])
    land = [(r, c) for r in range(rows) for c in range(cols)
            if grid[r][c] == 1]
    if not land:
        return 0                        # zero islands: disconnected

    def neighbors(r: int, c: int):
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                yield nr, nc

    root = land[0]
    disc = {root: 0}                    # cell -> discovery time
    low = {root: 0}                     # lowest time reachable
    root_children = 0
    has_cut = False
    stack: list[tuple] = [(root, None, neighbors(*root))]
    while stack:
        cell, parent, it = stack[-1]
        nxt = next(it, None)
        if nxt is None:                 # cell is finished
            stack.pop()
            if parent is not None:
                low[parent] = min(low[parent], low[cell])
                if parent != root and low[cell] >= disc[parent]:
                    has_cut = True      # subtree hangs on parent
        elif nxt == parent:
            continue
        elif nxt in disc:               # back edge to an ancestor
            low[cell] = min(low[cell], disc[nxt])
        else:                           # tree edge: go deeper
            disc[nxt] = low[nxt] = len(disc)
            if cell == root:
                root_children += 1
            stack.append((nxt, cell, neighbors(*nxt)))

    if len(disc) < len(land):
        return 0                        # already two or more islands
    one_day = len(land) == 1 or has_cut or root_children > 1
    return 1 if one_day else 2
