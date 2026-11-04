from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def can_cross(heights: list[list[int]], limit: int) -> bool:
    """BFS using only steps of height difference <= limit."""
    rows, cols = len(heights), len(heights[0])
    seen = {(0, 0)}
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in seen
                    and abs(heights[nr][nc] - heights[r][c])
                    <= limit):
                seen.add((nr, nc))
                queue.append((nr, nc))
    return False


def minimum_effort_brute(heights: list[list[int]]) -> int:
    """Try every step size as a limit, smallest first."""
    rows, cols = len(heights), len(heights[0])
    steps = {0}
    for r in range(rows):
        for c in range(cols):
            if r + 1 < rows:
                steps.add(abs(heights[r + 1][c] - heights[r][c]))
            if c + 1 < cols:
                steps.add(abs(heights[r][c + 1] - heights[r][c]))
    for limit in sorted(steps):
        if can_cross(heights, limit):
            return limit
    return 0
