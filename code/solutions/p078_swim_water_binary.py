from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def can_reach(grid: list[list[int]], t: int) -> bool:
    """BFS over cells of height <= t from the top-left corner."""
    n = len(grid)
    if grid[0][0] > t:
        return False
    seen = [[False] * n for _ in range(n)]
    seen[0][0] = True
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if r == n - 1 and c == n - 1:
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n and not seen[nr][nc]
                    and grid[nr][nc] <= t):
                seen[nr][nc] = True
                queue.append((nr, nc))
    return False


def swim_in_water_binary(grid: list[list[int]]) -> int:
    """Binary search on the time; BFS answers 'is t enough?'."""
    lo = max(grid[0][0], grid[-1][-1])  # never less than the ends
    hi = max(max(row) for row in grid)  # always enough
    while lo < hi:
        mid = (lo + hi) // 2
        if can_reach(grid, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
