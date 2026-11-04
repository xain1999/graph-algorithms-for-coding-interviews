def is_solvable(board: list[list[int]]) -> bool:
    """True if the 2x3 board can reach 1 2 3 / 4 5 0 at all."""
    tiles = [v for row in board for v in row if v != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0      # moves never change the parity
