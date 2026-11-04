DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def count_sub_islands_sink(grid1: list[list[int]],
                           grid2: list[list[int]]) -> int:
    """Sink grid2 islands that touch grid1 water, count the rest."""
    land = [row[:] for row in grid2]    # a copy we are free to erase
    rows, cols = len(land), len(land[0])

    def sink(sr: int, sc: int) -> None:
        land[sr][sc] = 0
        stack = [(sr, sc)]
        while stack:
            r, c = stack.pop()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and land[nr][nc] == 1):
                    land[nr][nc] = 0    # erasing is the marking
                    stack.append((nr, nc))

    for r in range(rows):               # pass 1: remove bad islands
        for c in range(cols):
            if land[r][c] == 1 and grid1[r][c] == 0:
                sink(r, c)
    count = 0
    for r in range(rows):               # pass 2: count survivors
        for c in range(cols):
            if land[r][c] == 1:
                count += 1
                sink(r, c)
    return count
