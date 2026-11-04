from collections import defaultdict

Cell = tuple[int, int]


def can_reach_exit_graph(grid: list[str]) -> bool:
    """Build an adjacency list of open cells, then search it."""
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == "#" or grid[rows - 1][cols - 1] == "#":
        return False
    graph: defaultdict[Cell, list[Cell]] = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != ".":
                continue
            # Look right and down only; store both directions.
            for nr, nc in ((r, c + 1), (r + 1, c)):
                if nr < rows and nc < cols and grid[nr][nc] == ".":
                    graph[(r, c)].append((nr, nc))
                    graph[(nr, nc)].append((r, c))

    goal = (rows - 1, cols - 1)
    seen = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        cell = stack.pop()
        if cell == goal:
            return True
        for nxt in graph[cell]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False
