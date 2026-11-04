DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def count_sub_islands(grid1: list[list[int]],
                      grid2: list[list[int]]) -> int:
    """Islands of grid2 whose every cell is land in grid1."""
    rows, cols = len(grid2), len(grid2[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for sr in range(rows):
        for sc in range(cols):
            if grid2[sr][sc] != 1 or seen[sr][sc]:
                continue
            is_sub = True           # until a cell proves otherwise
            seen[sr][sc] = True
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                if grid1[r][c] == 0:
                    is_sub = False      # but keep flooding
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid2[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            if is_sub:
                count += 1
    return count
