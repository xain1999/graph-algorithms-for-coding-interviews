from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def can_reach(grid: list[list[int]], t: int) -> bool:
    """BFS over cells of height <= t from the top-left corner."""
    n = len(grid)
    if grid[0][0] > t:
        return False
    seen = {(0, 0)}
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == n - 1 and c == n - 1:
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n
                    and (nr, nc) not in seen and grid[nr][nc] <= t):
                seen.add((nr, nc))
                queue.append((nr, nc))
    return False


def swim_in_water_brute(grid: list[list[int]]) -> int:
    """Try every height as the time, smallest first."""
    for t in sorted({h for row in grid for h in row}):
        if can_reach(grid, t):
            return t
    raise ValueError("unreachable: the largest height always works")
