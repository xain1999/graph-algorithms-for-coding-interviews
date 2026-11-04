import random
import time

import networkx as nx
import pytest

from solutions.p080_wire_office import wire_office
from solutions.p080_wire_office_brute import wire_office_brute

SOLVERS = [wire_office, wire_office_brute]

EXAMPLE_1 = (6, [[0, 1, 4], [0, 2, 3], [1, 2, 5], [1, 3, 6], [2, 3, 7],
                 [2, 4, 9], [3, 4, 2], [3, 5, 8], [4, 5, 10]])
EXAMPLE_2 = (4, [[0, 1, 5], [1, 2, 1], [0, 2, 2]])


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, cables, expected",
    [
        (*EXAMPLE_1, 23),                    # book example 1
        (*EXAMPLE_2, -1),                    # book example 2 (isolated)
        (1, [], 0),                          # one computer, no cable
        (2, [], -1),                         # two computers, no cable
        (2, [[0, 1, 9], [1, 0, 4]], 4),      # parallel cables
        (3, [[0, 1, 1], [1, 2, 1], [0, 2, 1]], 2),   # equal costs
        (4, [[0, 1, 1], [2, 3, 1]], -1),     # two separate pairs
    ],
)
def test_examples(solve, n, cables, expected):
    assert solve(n, cables) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    n, cables = EXAMPLE_1
    copy = [c[:] for c in cables]
    solve(n, cables)
    assert cables == copy


def networkx_cost(n, cables):
    g = nx.MultiGraph()
    g.add_nodes_from(range(n))
    for u, v, c in cables:
        g.add_edge(u, v, weight=c)
    if not nx.is_connected(g):
        return -1
    tree = nx.minimum_spanning_tree(g)
    return int(tree.size(weight="weight"))


def random_cables(rng, n, m, top):
    cables = []
    for _ in range(m):
        u, v = rng.sample(range(n), 2)
        cables.append([u, v, rng.randint(1, top)])
    return cables


def test_random_small_agree_with_brute_force():
    rng = random.Random(80)
    for _ in range(400):
        n = rng.randint(1, 6)
        m = 0 if n == 1 else rng.randint(0, 10)
        cables = random_cables(rng, n, m, rng.choice((3, 20)))
        assert wire_office(n, cables) == wire_office_brute(n, cables)


def test_random_medium_agree_with_networkx():
    rng = random.Random(1080)
    for _ in range(300):
        n = rng.randint(2, 40)
        cables = random_cables(rng, n, rng.randint(0, 120), 50)
        assert wire_office(n, cables) == networkx_cost(n, cables)


def test_large_is_fast():
    rng = random.Random(5)
    n = 10**4
    cables = [[i, i + 1, rng.randint(1, 10**4)] for i in range(n - 1)]
    cables += random_cables(rng, n, 5 * 10**4 - (n - 1), 10**4)
    start = time.perf_counter()
    got = wire_office(n, cables)
    assert time.perf_counter() - start < 2.0
    assert got == networkx_cost(n, cables)
