DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def capture_regions_by_region(
        board: list[list[str]]) -> list[list[str]]:
    """Collect each 'O' region; flip it if it misses the border."""
    result = [row[:] for row in board]
    rows, cols = len(board), len(board[0])
    seen = set()
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != "O" or (r, c) in seen:
                continue
            seen.add((r, c))
            stack, region = [(r, c)], []
            touches_border = False
            while stack:                # explore the WHOLE region
                cr, cc = stack.pop()
                region.append((cr, cc))
                if cr in (0, rows - 1) or cc in (0, cols - 1):
                    touches_border = True   # note it, keep going
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and board[nr][nc] == "O"
                            and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            if not touches_border:
                for cr, cc in region:
                    result[cr][cc] = "X"
    return result
