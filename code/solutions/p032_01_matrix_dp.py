def update_matrix_dp(mat: list[list[int]]) -> list[list[int]]:
    """Two sweeps: from the top-left, then from the bottom-right."""
    rows, cols = len(mat), len(mat[0])
    far = rows + cols                   # more than any distance
    dist = [[0 if v == 0 else far for v in row] for row in mat]

    for r in range(rows):               # zeros above or to the left
        for c in range(cols):
            if r > 0:
                dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1)
            if c > 0:
                dist[r][c] = min(dist[r][c], dist[r][c - 1] + 1)

    for r in range(rows - 1, -1, -1):   # ... below or to the right
        for c in range(cols - 1, -1, -1):
            if r < rows - 1:
                dist[r][c] = min(dist[r][c], dist[r + 1][c] + 1)
            if c < cols - 1:
                dist[r][c] = min(dist[r][c], dist[r][c + 1] + 1)
    return dist
