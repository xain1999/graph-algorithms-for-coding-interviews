import random
import time

import networkx as nx
import pytest

from solutions.p060_network import make_connected
from solutions.p060_network_brute import make_connected_brute

SOLVERS = [make_connected, make_connected_brute]

EXAMPLE_1 = [[0, 1], [1, 2], [4, 5], [2, 0], [2, 3], [3, 1]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, cables, expected",
    [
        (7, EXAMPLE_1, 2),                  # book example 1
        (7, EXAMPLE_1[:5], -1),             # book example 2
        (5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 0),  # a ring
        (1, [], 0),                         # smallest input
        (2, [], -1),
        (2, [[0, 1]], 0),
        (4, [[0, 1], [0, 1], [2, 3]], 1),   # duplicate cable
        (4, [[0, 1], [1, 2], [2, 0]], 1),
    ],
)
def test_examples(solve, n, cables, expected):
    assert solve(n, cables) == expected


def by_networkx(n, cables):
    if len(cables) < n - 1:
        return -1
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(map(tuple, cables))
    return nx.number_connected_components(g) - 1


def test_random_agree_with_networkx_and_brute():
    rng = random.Random(1319)
    for _ in range(300):
        n = rng.randint(1, 8)
        possible = [(a, b) for a in range(n) for b in range(a + 1, n)]
        cables = [list(c) for c in
                  rng.sample(possible, rng.randint(0, len(possible)))]
        expected = by_networkx(n, cables)
        assert make_connected(n, cables) == expected
        assert make_connected_brute(n, cables) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    cables = [c[:] for c in EXAMPLE_1]
    solve(7, cables)
    assert cables == EXAMPLE_1


def test_large_input_is_fast():
    rng = random.Random(5)
    n = 10**5
    cables = [[rng.randrange(n), rng.randrange(n)]
              for _ in range(2 * 10**5)]
    start = time.perf_counter()
    got = make_connected(n, cables)
    assert time.perf_counter() - start < 2.0
    assert got == by_networkx(n, cables)
