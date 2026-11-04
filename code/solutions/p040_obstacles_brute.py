from collections import deque
from itertools import combinations

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def plain_bfs(grid: list[list[int]]) -> int:
    """Fewest steps corner to corner through empty cells, or -1."""
    rows, cols = len(grid), len(grid[0])
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return dist[(r, c)]
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 0 and (nr, nc) not in dist):
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))
    return -1


def shortest_path_brute(grid: list[list[int]], k: int) -> int:
    """Try every set of at most k walls to knock down."""
    walls = [(r, c) for r, row in enumerate(grid)
             for c, v in enumerate(row) if v == 1]
    best = -1
    for size in range(min(k, len(walls)) + 1):
        for chosen in combinations(walls, size):
            trial = [row[:] for row in grid]
            for r, c in chosen:
                trial[r][c] = 0
            steps = plain_bfs(trial)
            if steps != -1 and (best == -1 or steps < best):
                best = steps
    return best
