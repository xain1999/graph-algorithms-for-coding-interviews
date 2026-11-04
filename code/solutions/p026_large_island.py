DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def largest_island(grid: list[list[int]]) -> int:
    """Largest island after turning at most one water cell to land."""
    rows, cols = len(grid), len(grid[0])
    label = [[0] * cols for _ in range(rows)]   # 0 = not labeled
    size = [0]                          # size[i] = area of island i

    # Pass 1: give every island an id and record its area.
    for sr in range(rows):
        for sc in range(cols):
            if grid[sr][sc] != 1 or label[sr][sc]:
                continue
            island = len(size)          # ids start at 1
            label[sr][sc] = island
            stack = [(sr, sc)]
            area = 0
            while stack:
                r, c = stack.pop()
                area += 1
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and not label[nr][nc]):
                        label[nr][nc] = island
                        stack.append((nr, nc))
            size.append(area)

    # Pass 2: try every water cell, using ids instead of floods.
    best = max(size)                    # flipping nothing (all land)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                continue
            touching = set()            # distinct neighbor islands
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and label[nr][nc]):
                    touching.add(label[nr][nc])
            best = max(best, 1 + sum(size[i] for i in touching))
    return best
