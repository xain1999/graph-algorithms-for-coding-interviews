import itertools
import random
from collections import deque

import pytest

from solutions.p041_sliding_puzzle import sliding_puzzle
from solutions.p041_sliding_puzzle_alt import is_solvable
from solutions.p041_sliding_puzzle_brute import sliding_puzzle_dfs

SOLVERS = [sliding_puzzle, sliding_puzzle_dfs]
ALL_BOARDS = [[list(p[:3]), list(p[3:])]
              for p in itertools.permutations(range(6))]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "board, expected",
    [
        ([[1, 3, 0], [4, 2, 5]], 3),         # book example 1
        ([[4, 5, 0], [1, 2, 3]], 21),        # hardest solvable board
        ([[3, 1, 2], [0, 5, 4]], -1),        # book example 2 (odd)
        ([[1, 2, 3], [4, 5, 0]], 0),         # already solved
        ([[1, 2, 0], [4, 5, 3]], 1),
        ([[2, 1, 3], [4, 5, 0]], -1),        # one swapped pair
        ([[0, 1, 2], [4, 5, 3]], 3),
    ],
)
def test_examples(solve, board, expected):
    assert solve(board) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    board = [[4, 5, 0], [1, 2, 3]]
    solve(board)
    assert board == [[4, 5, 0], [1, 2, 3]]


def test_every_board_agrees_with_parity():
    for board in ALL_BOARDS:
        assert (sliding_puzzle(board) != -1) == is_solvable(board)


def test_random_boards_agree_with_dfs():
    rng = random.Random(41)
    for board in rng.sample(ALL_BOARDS, 120):
        assert sliding_puzzle(board) == sliding_puzzle_dfs(board)


def test_exactly_half_the_boards_are_solvable():
    solvable = [b for b in ALL_BOARDS if sliding_puzzle(b) != -1]
    assert len(solvable) == 360
    assert max(sliding_puzzle(b) for b in solvable) == 21


def test_answer_matches_a_backward_bfs_from_the_goal():
    # One BFS from the goal labels every solvable board at once.
    nbrs = ((1, 3), (0, 2, 4), (1, 5), (0, 4), (1, 3, 5), (2, 4))
    dist = {"123450": 0}
    queue = deque(dist)
    while queue:
        s = queue.popleft()
        b = s.index("0")
        for c in nbrs[b]:
            t = list(s)
            t[b], t[c] = t[c], t[b]
            t = "".join(t)
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    rng = random.Random(773)
    for board in rng.sample(ALL_BOARDS, 200):
        key = "".join(str(v) for row in board for v in row)
        assert sliding_puzzle(board) == dist.get(key, -1)


def test_all_boards_are_fast():
    for board in ALL_BOARDS:     # 720 searches of at most 360 boards
        sliding_puzzle(board)
