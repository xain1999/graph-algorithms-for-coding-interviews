DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def longest_increasing_path_brute(matrix: list[list[int]]) -> int:
    """Explore every increasing path from every cell."""
    rows, cols = len(matrix), len(matrix[0])

    def longest_from(r: int, c: int) -> int:
        length = 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and matrix[nr][nc] > matrix[r][c]):
                length = max(length, 1 + longest_from(nr, nc))
        return length

    return max(longest_from(r, c)
               for r in range(rows) for c in range(cols))
