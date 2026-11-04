DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def flood(grid: list[list[int]], r: int, c: int,
          seen: list[list[bool]]) -> int:
    """Mark the region of equal cells at (r, c); return its size."""
    rows, cols = len(grid), len(grid[0])
    value = grid[r][c]
    seen[r][c] = True
    stack = [(r, c)]
    size = 0
    while stack:
        r, c = stack.pop()
        size += 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and not seen[nr][nc] and grid[nr][nc] == value):
                seen[nr][nc] = True     # mark when pushed
                stack.append((nr, nc))
    return size
