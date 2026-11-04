from collections import deque

# Cells are numbered 0 1 2 / 3 4 5. NEIGHBORS[i] lists the cells
# that share a side with cell i: where the blank can move from i.
NEIGHBORS = ((1, 3), (0, 2, 4), (1, 5), (0, 4), (1, 3, 5), (2, 4))
GOAL = "123450"


def sliding_puzzle(board: list[list[int]]) -> int:
    """Fewest moves that solve the 2x3 board, or -1 if impossible."""
    start = "".join(str(v) for row in board for v in row)
    if start == GOAL:
        return 0

    seen = {start}
    queue = deque([start])
    moves = 0
    while queue:
        moves += 1
        for _ in range(len(queue)):     # one layer = one more move
            state = queue.popleft()
            blank = state.index("0")
            for cell in NEIGHBORS[blank]:
                tiles = list(state)
                tiles[blank], tiles[cell] = tiles[cell], tiles[blank]
                nxt = "".join(tiles)
                if nxt == GOAL:
                    return moves
                if nxt not in seen:     # mark when enqueued
                    seen.add(nxt)
                    queue.append(nxt)
    return -1                           # all reachable boards tried
