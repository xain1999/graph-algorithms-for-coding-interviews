def num_islands_brute(grid: list[list[int]]) -> int:
    """Spread the smallest label until no label changes."""
    rows, cols = len(grid), len(grid[0])
    # Every land cell starts with its own label, its scan index.
    label = [[r * cols + c if grid[r][c] == 1 else -1
              for c in range(cols)] for r in range(rows)]
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if label[r][c] < 0:
                    continue
                for nr, nc in ((r + 1, c), (r - 1, c),
                               (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and 0 <= label[nr][nc] < label[r][c]):
                        label[r][c] = label[nr][nc]
                        changed = True
    return len({x for row in label for x in row if x >= 0})
