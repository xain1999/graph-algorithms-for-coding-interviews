DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
MOVES = "DURL"                          # one letter per direction


def island_signature(grid: list[list[int]], seen: list[list[bool]],
                     sr: int, sc: int) -> str:
    """Moves of a DFS from (sr, sc), with 'b' for each step back."""
    rows, cols = len(grid), len(grid[0])
    moves = []
    seen[sr][sc] = True
    stack = [(sr, sc, 0)]               # cell, next direction to try
    while stack:
        r, c, d = stack.pop()
        if d == len(DIRECTIONS):
            moves.append("b")           # all tried: leave this cell
            continue
        stack.append((r, c, d + 1))     # resume here afterwards
        nr, nc = r + DIRECTIONS[d][0], c + DIRECTIONS[d][1]
        if (0 <= nr < rows and 0 <= nc < cols
                and grid[nr][nc] == 1 and not seen[nr][nc]):
            seen[nr][nc] = True
            moves.append(MOVES[d])
            stack.append((nr, nc, 0))   # go deeper first
    return "".join(moves)


def count_distinct_islands_path(grid: list[list[int]]) -> int:
    """Count island shapes by their DFS move signatures."""
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    signatures: set[str] = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                signatures.add(island_signature(grid, seen, r, c))
    return len(signatures)
