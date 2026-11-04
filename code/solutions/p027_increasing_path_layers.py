from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def longest_increasing_path_layers(matrix: list[list[int]]) -> int:
    """Peel cells with no smaller neighbor, one layer at a time."""
    rows, cols = len(matrix), len(matrix[0])
    smaller = [[0] * cols for _ in range(rows)]  # the in-degrees
    for r in range(rows):
        for c in range(cols):
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and matrix[nr][nc] < matrix[r][c]):
                    smaller[r][c] += 1
    queue = deque((r, c) for r in range(rows) for c in range(cols)
                  if smaller[r][c] == 0)        # local minima
    layers = 0
    while queue:
        layers += 1
        for _ in range(len(queue)):     # one layer per path cell
            r, c = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and matrix[nr][nc] > matrix[r][c]):
                    smaller[nr][nc] -= 1
                    if smaller[nr][nc] == 0:
                        queue.append((nr, nc))
    return layers
