from collections import deque

# sign -> move: 1 right, 2 left, 3 down, 4 up
MOVES = {1: (0, 1), 2: (0, -1), 3: (1, 0), 4: (-1, 0)}


def min_cost(grid: list[list[int]]) -> int:
    """Fewest sign changes that open a path to the bottom-right."""
    rows, cols = len(grid), len(grid[0])
    INF = rows * cols                   # more than any answer
    dist = [[INF] * cols for _ in range(rows)]
    dist[0][0] = 0
    dq = deque([(0, 0, 0)])             # (cost, row, col)
    while dq:
        d, r, c = dq.popleft()
        if d > dist[r][c]:
            continue                    # stale entry
        if r == rows - 1 and c == cols - 1:
            return d
        for sign, (dr, dc) in MOVES.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            w = 0 if grid[r][c] == sign else 1
            if d + w < dist[nr][nc]:
                dist[nr][nc] = d + w
                if w == 0:
                    dq.appendleft((d, nr, nc))      # free: go first
                else:
                    dq.append((d + 1, nr, nc))      # paid: go last
    raise ValueError("unreachable: every cell can be reached")
