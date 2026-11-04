from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def shortest_path_states(grid: list[list[int]], k: int) -> int:
    """Plain BFS over every (row, col, removals_left) state."""
    rows, cols = len(grid), len(grid[0])
    start = (0, 0, k)
    seen = {start}
    queue = deque([start])
    steps = 0
    while queue:
        for _ in range(len(queue)):
            r, c, left = queue.popleft()
            if (r, c) == (rows - 1, cols - 1):
                return steps
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    state = (nr, nc, left - grid[nr][nc])
                    if state[2] >= 0 and state not in seen:
                        seen.add(state)
                        queue.append(state)
        steps += 1
    return -1
