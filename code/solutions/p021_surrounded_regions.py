DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def capture_regions(board: list[list[str]]) -> list[list[str]]:
    """New board with every 'O' region off the border captured."""
    rows, cols = len(board), len(board[0])
    border = [(r, c) for r in range(rows) for c in range(cols)
              if r in (0, rows - 1) or c in (0, cols - 1)]

    # 1. Every 'O' on the border is a source; mark what they reach.
    safe = set()
    stack = []
    for r, c in border:
        if board[r][c] == "O":
            safe.add((r, c))
            stack.append((r, c))
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and board[nr][nc] == "O"
                    and (nr, nc) not in safe):
                safe.add((nr, nc))
                stack.append((nr, nc))

    # 2. Any 'O' the border could not reach is surrounded.
    return [["O" if (r, c) in safe else "X" for c in range(cols)]
            for r in range(rows)]
