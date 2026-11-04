NEIGHBORS = ((1, 3), (0, 2, 4), (1, 5), (0, 4), (1, 3, 5), (2, 4))
GOAL = "123450"


def sliding_puzzle_dfs(board: list[list[int]]) -> int:
    """DFS that re-explores a board when it finds a shorter way."""
    start = "".join(str(v) for row in board for v in row)
    best: dict[str, int] = {}       # board -> fewest moves so far

    def dfs(state: str, moves: int) -> None:
        if best.get(state, moves + 1) <= moves:
            return                  # reached before, at least as fast
        best[state] = moves
        if state == GOAL:
            return
        blank = state.index("0")
        for cell in NEIGHBORS[blank]:
            tiles = list(state)
            tiles[blank], tiles[cell] = tiles[cell], tiles[blank]
            dfs("".join(tiles), moves + 1)

    dfs(start, 0)
    return best.get(GOAL, -1)
