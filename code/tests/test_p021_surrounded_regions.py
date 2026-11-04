import random

import networkx as nx
import pytest

from solutions.p021_surrounded_regions import capture_regions
from solutions.p021_surrounded_regions_regions import (
    capture_regions_by_region,
)

SOLVERS = [capture_regions, capture_regions_by_region]


def board(*rows):
    return [list(row) for row in rows]


EXAMPLE_1 = board("XXXXOXX", "XOOXOXX", "XXOXOOX", "XXXXXOX",
                  "OOXXOXX", "XXXXXXX")
EXPECTED_1 = board("XXXXOXX", "XXXXOXX", "XXXXOOX", "XXXXXOX",
                   "OOXXXXX", "XXXXXXX")


def nx_capture(b):
    """Reference: capture components with no border cell."""
    rows, cols = len(b), len(b[0])
    g = nx.Graph()
    for r in range(rows):
        for c in range(cols):
            if b[r][c] == "O":
                g.add_node((r, c))
                if r + 1 < rows and b[r + 1][c] == "O":
                    g.add_edge((r, c), (r + 1, c))
                if c + 1 < cols and b[r][c + 1] == "O":
                    g.add_edge((r, c), (r, c + 1))
    out = [row[:] for row in b]
    for comp in nx.connected_components(g):
        if not any(r in (0, rows - 1) or c in (0, cols - 1)
                   for r, c in comp):
            for r, c in comp:
                out[r][c] = "X"
    return out


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "b, expected",
    [
        (EXAMPLE_1, EXPECTED_1),                       # example 1
        (board("XXXXX", "XOXOX", "XXOXX", "XOXOX", "XXXXX"),
         board("XXXXX", "XXXXX", "XXXXX", "XXXXX", "XXXXX")),  # ex. 2
        (board("XOX", "OOO", "XOX"),
         board("XOX", "OOO", "XOX")),                  # example 3
        (board("X"), board("X")),
        (board("O"), board("O")),
        (board("OXO"), board("OXO")),                        # one row
        (board("O", "O", "X"), board("O", "O", "X")),  # one column
        (board("XXX", "XOX", "XXX"), board("XXX", "XXX", "XXX")),
        (board("OOOO", "OXXO", "OXOO", "OOOO"),
         board("OOOO", "OXXO", "OXOO", "OOOO")),       # ring of O
    ],
)
def test_examples(solve, b, expected):
    assert solve(b) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    b = [row[:] for row in EXAMPLE_1]
    solve(b)
    assert b == EXAMPLE_1


def test_random_boards_agree():
    rng = random.Random(130)
    for _ in range(1000):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        p = rng.random()
        b = [["O" if rng.random() < p else "X" for _ in range(cols)]
             for _ in range(rows)]
        want = nx_capture(b)
        for solve in SOLVERS:
            assert solve(b) == want


def test_large_spiral_is_fast():
    # one long winding corridor of 'O' reaching the border: no capture
    n = 300
    b = [["X"] * n for _ in range(n)]
    for r in range(0, n, 2):
        b[r] = ["O"] * n
        if r + 1 < n:
            b[r + 1][n - 1 if r % 4 == 0 else 0] = "O"
    for solve in SOLVERS:
        assert solve(b) == b


def test_large_interior_block_captured():
    n = 300
    b = [["O" if 0 < r < n - 1 and 0 < c < n - 1 else "X"
          for c in range(n)] for r in range(n)]
    out = capture_regions(b)
    assert all(cell == "X" for row in out for cell in row)
