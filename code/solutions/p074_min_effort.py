import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def minimum_effort(heights: list[list[int]]) -> int:
    """Least effort (hardest single step) from corner to corner."""
    rows, cols = len(heights), len(heights[0])
    INF = float("inf")
    effort = [[INF] * cols for _ in range(rows)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]                  # (effort so far, row, col)
    while heap:
        e, r, c = heapq.heappop(heap)
        if e > effort[r][c]:
            continue                    # stale entry
        if (r, c) == (rows - 1, cols - 1):
            return e                    # popped = final
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                step = abs(heights[nr][nc] - heights[r][c])
                ne = max(e, step)       # max, not sum
                if ne < effort[nr][nc]:
                    effort[nr][nc] = ne
                    heapq.heappush(heap, (ne, nr, nc))
    return 0                            # never reached
