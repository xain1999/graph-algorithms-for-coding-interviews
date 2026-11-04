from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def shortest_path(grid: list[list[int]], k: int) -> int:
    """Fewest steps corner to corner, removing at most k walls."""
    rows, cols = len(grid), len(grid[0])
    if k >= rows + cols - 3:            # enough to clear any L path
        return rows + cols - 2
    # best[r][c]: most removals left on any arrival at (r, c) so far
    best = [[-1] * cols for _ in range(rows)]
    best[0][0] = k
    queue = deque([(0, 0, k)])          # state: (row, col, left)
    steps = 0
    while queue:
        for _ in range(len(queue)):     # one BFS layer = one step
            r, c, left = queue.popleft()
            if (r, c) == (rows - 1, cols - 1):
                return steps
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                rest = left - grid[nr][nc]  # a wall costs one
                if rest > best[nr][nc]:     # better than before
                    best[nr][nc] = rest
                    queue.append((nr, nc, rest))
        steps += 1
    return -1
