from solutions.p030_binary_matrix import DIRECTIONS


def shortest_path_brute(grid: list[list[int]]) -> int:
    """Backtracking DFS over every simple path; keep the shortest."""
    n = len(grid)
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1
    on_path = [[False] * n for _ in range(n)]
    best = -1

    def explore(r: int, c: int, length: int) -> None:
        nonlocal best
        if best != -1 and length >= best:
            return                      # cannot beat the best
        if r == n - 1 and c == n - 1:
            best = length
            return
        on_path[r][c] = True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < n and 0 <= nc < n
                    and grid[nr][nc] == 0 and not on_path[nr][nc]):
                explore(nr, nc, length + 1)
        on_path[r][c] = False           # undo: free the cell again

    explore(0, 0, 1)
    return best
