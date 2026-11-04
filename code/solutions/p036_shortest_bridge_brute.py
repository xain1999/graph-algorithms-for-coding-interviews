from solutions.p036_shortest_bridge import DIRECTIONS


def shortest_bridge_brute(grid: list[list[int]]) -> int:
    """Try every pair of cells, one from each island."""
    rows, cols = len(grid), len(grid[0])
    label = [[0] * cols for _ in range(rows)]
    islands: list[list[tuple[int, int]]] = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and label[r][c] == 0:
                islands.append([])
                label[r][c] = len(islands)
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    islands[-1].append((cr, cc))
                    for dr, dc in DIRECTIONS:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == 1
                                and label[nr][nc] == 0):
                            label[nr][nc] = len(islands)
                            stack.append((nr, nc))
    first, second = islands
    # A bridge between a and b needs |dr| + |dc| - 1 new cells.
    return min(abs(ar - br) + abs(ac - bc) - 1
               for ar, ac in first for br, bc in second)
