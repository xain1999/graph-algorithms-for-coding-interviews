DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def count_distinct_islands(grid: list[list[int]]) -> int:
    """Number of island shapes, counting translated copies once."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    shapes: set[frozenset[tuple[int, int]]] = set()
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1 or seen[sr][sc]:
                continue
            # (sr, sc) is the island's first cell in scan order
            shape = []
            seen[sr][sc] = True
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                shape.append((r - sr, c - sc))  # offset from anchor
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            shapes.add(frozenset(shape))
    return len(shapes)
