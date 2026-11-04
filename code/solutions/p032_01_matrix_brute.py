from collections import deque

from solutions.p032_01_matrix import DIRECTIONS


def update_matrix_brute(mat: list[list[int]]) -> list[list[int]]:
    """A separate BFS from every 1, stopping at the first 0."""
    rows, cols = len(mat), len(mat[0])

    def nearest_zero(sr: int, sc: int) -> int:
        seen = {(sr, sc)}
        queue = deque([(sr, sc, 0)])
        while queue:
            r, c, d = queue.popleft()
            if mat[r][c] == 0:
                return d
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in seen):
                    seen.add((nr, nc))
                    queue.append((nr, nc, d + 1))
        return -1                       # the grid has no 0 at all

    return [[nearest_zero(r, c) if mat[r][c] else 0
             for c in range(cols)] for r in range(rows)]
