import random

import networkx as nx
import pytest

from solutions.p023_pacific_atlantic import pacific_atlantic
from solutions.p023_pacific_atlantic_brute import (
    pacific_atlantic_brute,
)

SOLVERS = [pacific_atlantic, pacific_atlantic_brute]

EXAMPLE_1 = [
    [1, 3, 4, 6, 5, 4],
    [2, 4, 8, 7, 7, 3],
    [3, 8, 9, 4, 2, 2],
    [2, 8, 1, 3, 3, 1],
    [4, 6, 5, 2, 1, 2],
]
EXPECTED_1 = [(0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (2, 1),
              (2, 2), (3, 1), (4, 0), (4, 1)]


def nx_both(h):
    """Reference: directed water-flow graph plus two ocean nodes."""
    rows, cols = len(h), len(h[0])
    g = nx.DiGraph()
    for r in range(rows):
        for c in range(cols):
            g.add_node((r, c))
            for nr, nc in ((r + 1, c), (r - 1, c),
                           (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols \
                        and h[nr][nc] <= h[r][c]:
                    g.add_edge((r, c), (nr, nc))
            if r == 0 or c == 0:
                g.add_edge((r, c), "P")
            if r == rows - 1 or c == cols - 1:
                g.add_edge((r, c), "A")
    rev = g.reverse()
    return sorted(nx.descendants(rev, "P")
                  & nx.descendants(rev, "A"))


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "h, expected",
    [
        (EXAMPLE_1, EXPECTED_1),                       # example 1
        ([[9, 8, 7], [2, 1, 6], [3, 4, 5]],
         [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]),
        ([[3, 2, 1, 2, 3]],
         [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]),    # example 3
        ([[7]], [(0, 0)]),
        ([[1], [2], [3]], [(0, 0), (1, 0), (2, 0)]),  # one column
        ([[4, 4, 4], [4, 4, 4], [4, 4, 4]],
         [(r, c) for r in range(3) for c in range(3)]),       # flat
        ([[5, 5, 5], [5, 1, 5], [5, 5, 5]],
         [(r, c) for r in range(3) for c in range(3)
          if (r, c) != (1, 1)]),                              # pit
    ],
)
def test_examples(solve, h, expected):
    assert solve(h) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    h = [row[:] for row in EXAMPLE_1]
    solve(h)
    assert h == EXAMPLE_1


def test_random_grids_agree():
    rng = random.Random(417)
    for _ in range(600):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        top = rng.choice((2, 4, 9))       # few values = many plateaus
        h = [[rng.randint(0, top) for _ in range(cols)]
             for _ in range(rows)]
        want = nx_both(h)
        for solve in SOLVERS:
            assert solve(h) == want


def test_large_staircase_is_fast():
    # a snake of strictly increasing heights: very deep search
    n = 250
    h = [[0] * n for _ in range(n)]
    k = 0
    for r in range(n):
        cols = range(n) if r % 2 == 0 else range(n - 1, -1, -1)
        for c in cols:
            h[r][c] = k
            k += 1
    result = pacific_atlantic(h)
    assert (n - 1, 0) in result and (0, n - 1) in result


def test_large_flat_grid():
    n = 250
    h = [[10 ** 6] * n for _ in range(n)]
    assert len(pacific_atlantic(h)) == n * n
