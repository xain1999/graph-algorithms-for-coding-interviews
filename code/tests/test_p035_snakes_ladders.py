import random
import time

import networkx as nx
import pytest

from solutions.p035_snakes_ladders import cell_of, snakes_and_ladders
from solutions.p035_snakes_ladders_alt import (
    flatten, snakes_and_ladders_flat,
)

SOLVERS = [snakes_and_ladders, snakes_and_ladders_flat]

EXAMPLE_1 = [
    [-1, -1, -1, -1, -1],
    [-1, -1, 15, -1, -1],
    [8, -1, -1, -1, -1],
    [-1, 19, -1, -1, -1],
    [-1, -1, -1, -1, 9],
]
EXAMPLE_2 = [
    [-1, 3, -1, -1],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
    [-1, 15, -1, -1],
]
EXAMPLE_3 = [
    [-1, -1, 8, 5],
    [3, 6, 2, 7],
    [-1, -1, -1, -1],
    [-1, -1, -1, -1],
]


def numbering(n):
    """Square number printed in each cell, built row by row."""
    labels = [[0] * n for _ in range(n)]
    square = 1
    for band in range(n):
        row = n - 1 - band
        cols = range(n) if band % 2 == 0 else range(n - 1, -1, -1)
        for c in cols:
            labels[row][c] = square
            square += 1
    return labels


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 7])
def test_cell_of_matches_the_drawn_numbering(n):
    labels = numbering(n)
    for r in range(n):
        for c in range(n):
            assert cell_of(labels[r][c], n) == (r, c)


def test_flatten_reads_squares_in_order():
    jump = flatten(EXAMPLE_1)
    assert [s for s in range(1, 26) if jump[s] != -1] == [5, 9, 11, 18]
    assert (jump[5], jump[9], jump[11], jump[18]) == (9, 19, 8, 15)


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "board, expected",
    [
        (EXAMPLE_1, 3),                 # book example 1
        (EXAMPLE_2, 2),                 # book example 2 (no chaining)
        (EXAMPLE_3, -1),                # all snakes, unreachable (edge case)
        ([[-1, -1], [-1, -1]], 1),      # smallest board
        ([[-1, -1], [-1, 4]], 1),       # ladder on square 2 to the goal
        ([[-1] * 3 for _ in range(3)], 2),
        ([[-1] * 6 for _ in range(6)], 6),
        ([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], 1),  # 4 -> 9
    ],
)
def test_examples(solve, board, expected):
    assert solve(board) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    board = [row[:] for row in EXAMPLE_1]
    solve(board)
    assert board == EXAMPLE_1


def networkx_answer(board):
    n = len(board)
    labels = numbering(n)
    jump = {labels[r][c]: board[r][c]
            for r in range(n) for c in range(n) if board[r][c] != -1}
    goal = n * n
    g = nx.DiGraph()
    g.add_nodes_from(range(1, goal + 1))
    for s in range(1, goal):
        for t in range(s + 1, min(s + 6, goal) + 1):
            g.add_edge(s, jump.get(t, t))
    try:
        return nx.shortest_path_length(g, 1, goal)
    except nx.NetworkXNoPath:
        return -1


def random_board(rng, n):
    board = [[-1] * n for _ in range(n)]
    goal = n * n
    for _ in range(rng.randint(0, 2 * n)):
        a = rng.randint(2, goal - 1)
        b = rng.randint(1, goal)
        if a != b:
            r, c = cell_of(a, n)
            board[r][c] = b
    return board


def test_random_boards_agree_with_networkx():
    rng = random.Random(909)
    for _ in range(1500):
        board = random_board(rng, rng.randint(2, 7))
        want = networkx_answer(board)
        assert snakes_and_ladders(board) == want
        assert snakes_and_ladders_flat(board) == want


def test_large_board_is_fast():
    n = 150
    rng = random.Random(1)
    board = random_board(rng, n)
    start = time.perf_counter()
    for solve in SOLVERS:
        solve(board)
    assert time.perf_counter() - start < 2.0
    plain = [[-1] * n for _ in range(n)]
    assert snakes_and_ladders(plain) == (n * n - 1 + 5) // 6
