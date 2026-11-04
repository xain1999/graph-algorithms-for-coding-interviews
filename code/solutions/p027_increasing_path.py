from collections.abc import Iterator

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def longest_increasing_path(matrix: list[list[int]]) -> int:
    """Cells on the longest strictly increasing path (iterative)."""
    rows, cols = len(matrix), len(matrix[0])
    best = [[0] * cols for _ in range(rows)]    # 0 = not known yet

    def uphill(r: int, c: int) -> Iterator[tuple[int, int]]:
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and matrix[nr][nc] > matrix[r][c]):
                yield nr, nc

    for sr in range(rows):
        for sc in range(cols):
            stack = [(sr, sc, False)]
            while stack:
                r, c, ready = stack.pop()
                if ready:               # every uphill cell is known
                    best[r][c] = 1 + max(
                        (best[nr][nc] for nr, nc in uphill(r, c)),
                        default=0)
                elif not best[r][c]:
                    stack.append((r, c, True))   # come back later
                    for nr, nc in uphill(r, c):
                        if not best[nr][nc]:
                            stack.append((nr, nc, False))
    return max(max(row) for row in best)
