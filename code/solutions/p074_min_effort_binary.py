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


def minimum_effort_binary(heights: list[list[int]]) -> int:
    """Binary search the smallest limit that lets BFS get across."""
    lo, hi = 0, max(map(max, heights)) - min(map(min, heights))
    while lo < hi:                      # answer is in [lo, hi]
        mid = (lo + hi) // 2
        if can_cross(heights, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
