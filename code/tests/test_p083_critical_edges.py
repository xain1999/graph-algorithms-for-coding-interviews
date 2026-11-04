import random
import time

import pytest

from solutions.p083_critical_edges import critical_edges, mst_weight
from solutions.p083_critical_edges_brute import critical_edges_brute

SOLVERS = [critical_edges, critical_edges_brute]

EDGES_1 = [[2, 3, 1], [3, 5, 4], [0, 1, 2], [1, 3, 7], [3, 4, 3],
           [0, 2, 2], [4, 5, 4], [1, 2, 2]]
EDGES_2 = [[0, 1, 2], [1, 2, 5], [2, 3, 1], [3, 0, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (6, EDGES_1, [[0, 4], [1, 2, 5, 6, 7]]),    # book example 1
        (4, EDGES_2, [[0, 2], [1, 3]]),             # book example 2
        (2, [[0, 1, 9]], [[0], []]),                # smallest input
        (4, [[0, 1, 5], [1, 2, 3], [1, 3, 8]], [[0, 1, 2], []]),  # tree
        (3, [[0, 1, 1], [1, 2, 1], [0, 2, 1]], [[], [0, 1, 2]]),
        (3, [[0, 1, 1], [1, 2, 2], [0, 2, 3]], [[0, 1], []]),
        # a bridge plus a cycle with a unique heaviest edge
        (4, [[0, 1, 9], [1, 2, 1], [2, 3, 1], [1, 3, 4]],
         [[0, 1, 2], []]),
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


def test_mst_weight_skip_and_force():
    order = sorted(range(len(EDGES_1)), key=lambda i: EDGES_1[i][2])
    assert mst_weight(6, EDGES_1, order) == 12
    assert mst_weight(6, EDGES_1, order, skip=0) == 18   # critical
    assert mst_weight(6, EDGES_1, order, skip=7) == 12
    assert mst_weight(6, EDGES_1, order, force=7) == 12  # pseudo
    assert mst_weight(6, EDGES_1, order, force=3) == 17  # neither
    # removing a bridge disconnects the graph
    assert mst_weight(2, [[0, 1, 9]], [0], skip=0) == float("inf")


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EDGES_1]
    solve(6, edges)
    assert edges == EDGES_1


def random_connected(rng, n, extra, w_max):
    pairs = set()
    for v in range(1, n):                 # a random spanning tree
        pairs.add((rng.randrange(v), v))
    possible = [(a, b) for a in range(n) for b in range(a + 1, n)]
    for a, b in rng.sample(possible, min(extra, len(possible))):
        if (b, a) not in pairs:
            pairs.add((a, b))
    edges = [[a, b, rng.randint(1, w_max)] for a, b in pairs]
    rng.shuffle(edges)
    return edges


def test_random_agree_with_brute_force():
    rng = random.Random(1489)
    for _ in range(400):
        n = rng.randint(2, 6)
        edges = random_connected(rng, n, rng.randint(0, 6), 3)
        assert critical_edges(n, edges) == critical_edges_brute(n, edges)


def test_large_input_is_fast():
    rng = random.Random(83)
    n = 120
    edges = random_connected(rng, n, 181, 20)   # at most 300 edges
    assert len(edges) <= 300
    start = time.perf_counter()
    critical, pseudo = critical_edges(n, edges)
    assert time.perf_counter() - start < 2.0
    assert not set(critical) & set(pseudo)
    # every edge of one MST is critical or pseudo-critical
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for i in sorted(range(len(edges)), key=lambda i: edges[i][2]):
        ra, rb = find(edges[i][0]), find(edges[i][1])
        if ra != rb:
            parent[ra] = rb
            assert i in critical or i in pseudo
