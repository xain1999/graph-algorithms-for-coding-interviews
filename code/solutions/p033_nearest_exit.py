from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def nearest_exit(maze: list[str], entrance: list[int]) -> int:
    """Steps from the entrance to the closest exit, or -1."""
    rows, cols = len(maze), len(maze[0])
    r0, c0 = entrance
    seen = [[False] * cols for _ in range(rows)]
    seen[r0][c0] = True     # so the entrance is never an exit
    queue = deque([(r0, c0)])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):     # one layer = one more step
            r, c = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols
                        and maze[nr][nc] == "." and not seen[nr][nc]):
                    continue        # off the map, a wall, or seen
                if nr in (0, rows - 1) or nc in (0, cols - 1):
                    return steps    # first border cell reached
                seen[nr][nc] = True     # mark when enqueued
                queue.append((nr, nc))
    return -1
