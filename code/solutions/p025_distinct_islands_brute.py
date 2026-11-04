DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def islands_of(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """The cells of every island, each list sorted."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    islands = []
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1 or seen[sr][sc]:
                continue
            cells = []
            seen[sr][sc] = True
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                cells.append((r, c))
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            islands.append(sorted(cells))
    return islands


def same_shape(a: list[tuple[int, int]],
               b: list[tuple[int, int]]) -> bool:
    """Is sorted island b a translated copy of sorted island a?"""
    if len(a) != len(b):
        return False
    dr, dc = b[0][0] - a[0][0], b[0][1] - a[0][1]
    return all((r + dr, c + dc) == cell
               for (r, c), cell in zip(a, b))


def count_distinct_islands_brute(grid: list[list[int]]) -> int:
    """Compare each island with every distinct shape kept so far."""
    distinct: list[list[tuple[int, int]]] = []
    for island in islands_of(grid):
        if not any(same_shape(island, kept) for kept in distinct):
            distinct.append(island)
    return len(distinct)
