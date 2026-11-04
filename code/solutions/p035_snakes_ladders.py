from collections import deque


def cell_of(square: int, n: int) -> tuple[int, int]:
    """(row, col) of a square; row 0 is the top row of the board."""
    band, offset = divmod(square - 1, n)    # band 0 = bottom row
    row = n - 1 - band
    if band % 2 == 0:
        return row, offset                  # left to right
    return row, n - 1 - offset              # right to left


def snakes_and_ladders(board: list[list[int]]) -> int:
    """Fewest dice rolls from square 1 to square n*n, or -1."""
    n = len(board)
    goal = n * n
    seen = [False] * (goal + 1)
    seen[1] = True
    queue = deque([1])
    rolls = 0
    while queue:
        rolls += 1
        for _ in range(len(queue)):     # one layer = one more roll
            square = queue.popleft()
            for face in range(1, 7):
                nxt = square + face
                if nxt > goal:
                    break
                r, c = cell_of(nxt, n)
                if board[r][c] != -1:
                    nxt = board[r][c]   # follow it once, never chain
                if nxt == goal:
                    return rolls
                if not seen[nxt]:
                    seen[nxt] = True    # mark when enqueued
                    queue.append(nxt)
    return -1
