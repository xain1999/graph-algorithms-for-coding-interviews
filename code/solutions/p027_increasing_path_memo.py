DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def longest_increasing_path_memo(matrix: list[list[int]]) -> int:
    """Recursive DFS that remembers each cell's answer."""
    rows, cols = len(matrix), len(matrix[0])
    best = [[0] * cols for _ in range(rows)]    # 0 = not known yet

    def longest_from(r: int, c: int) -> int:
        if best[r][c]:
            return best[r][c]           # computed before: reuse
        length = 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and matrix[nr][nc] > matrix[r][c]):
                length = max(length, 1 + longest_from(nr, nc))
        best[r][c] = length
        return length

    return max(longest_from(r, c)
               for r in range(rows) for c in range(cols))
