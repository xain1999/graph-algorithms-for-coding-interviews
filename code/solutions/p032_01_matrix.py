from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    """Distance from every cell to its nearest 0 (side steps)."""
    rows, cols = len(mat), len(mat[0])
    dist = [[-1] * cols for _ in range(rows)]   # -1 = not reached
    queue: deque[tuple[int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0          # every zero is a source
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and dist[nr][nc] == -1):
                dist[nr][nc] = dist[r][c] + 1   # mark on enqueue
                queue.append((nr, nc))
    return dist
