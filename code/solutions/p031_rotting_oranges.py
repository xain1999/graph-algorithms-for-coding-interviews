from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def oranges_rotting(grid: list[list[int]]) -> int:
    """Minutes until nothing is fresh, or -1 if that never happens."""
    grid = [row[:] for row in grid]     # leave the input untouched
    rows, cols = len(grid), len(grid[0])

    queue: deque[tuple[int, int]] = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))    # each rotten one is a source
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh > 0:
        minutes += 1
        for _ in range(len(queue)):     # one BFS layer = one minute
            r, c = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == 1):
                    grid[nr][nc] = 2    # mark when enqueued
                    fresh -= 1
                    queue.append((nr, nc))

    return minutes if fresh == 0 else -1
