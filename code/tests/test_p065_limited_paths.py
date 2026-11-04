import random
import time

import networkx as nx
import pytest

from solutions.p065_limited_paths import limited_paths
from solutions.p065_limited_paths_brute import limited_paths_brute

SOLVERS = [limited_paths, limited_paths_brute]

EDGES_1 = [[0, 1, 4], [1, 2, 2], [0, 2, 6], [2, 3, 5], [3, 4, 7],
           [4, 5, 3], [1, 5, 10]]
QUERIES_1 = [[0, 3, 6], [0, 4, 7], [5, 2, 8], [4, 5, 4], [1, 4, 3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, queries, expected",
    [
        # book example 1: the limit is strict (3-4 has length 7)
        (6, EDGES_1, QUERIES_1, [True, False, True, True, False]),
        # book example 2: parallel edges, the shorter one counts
        (3, [[0, 1, 9], [1, 2, 5], [0, 1, 3], [1, 2, 5]],
         [[0, 2, 6], [2, 0, 5], [1, 0, 4]], [True, False, True]),
        # an isolated node, u == v, a tight limit
        (4, [[0, 1, 1], [1, 2, 1]],
         [[2, 3, 100], [3, 3, 1], [0, 2, 1], [0, 2, 2]],
         [False, True, False, True]),
        (1, [], [[0, 0, 5]], [True]),            # smallest input
        (2, [[0, 1, 5]], [], []),                # no queries
        (2, [[0, 1, 5]], [[0, 1, 5], [0, 1, 6]], [False, True]),
        (3, [[0, 0, 1], [1, 2, 1]], [[0, 1, 9]], [False]),  # self-loop
        # equal limits in any order
        (3, [[0, 1, 2], [1, 2, 2]],
         [[0, 2, 3], [2, 0, 3], [0, 2, 2]], [True, True, False]),
    ],
)
def test_examples(solve, n, edges, queries, expected):
    assert solve(n, edges, queries) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EDGES_1]
    queries = [q[:] for q in QUERIES_1]
    solve(6, edges, queries)
    assert edges == EDGES_1
    assert queries == QUERIES_1


def random_case(rng: random.Random):
    n = rng.randint(1, 8)
    edges = [[rng.randrange(n), rng.randrange(n), rng.randint(1, 6)]
             for _ in range(rng.randint(0, 12))]
    queries = [[rng.randrange(n), rng.randrange(n), rng.randint(1, 7)]
               for _ in range(rng.randint(0, 10))]
    return n, edges, queries


def test_random_agree_with_brute_force():
    rng = random.Random(1697)
    for _ in range(800):
        n, edges, queries = random_case(rng)
        assert (limited_paths(n, edges, queries)
                == limited_paths_brute(n, edges, queries))


def test_random_agree_with_networkx():
    rng = random.Random(65)
    for _ in range(200):
        n, edges, queries = random_case(rng)
        expected = []
        for u, v, limit in queries:
            g = nx.Graph()
            g.add_nodes_from(range(n))
            g.add_edges_from((a, b) for a, b, w in edges if w < limit)
            expected.append(nx.has_path(g, u, v))
        assert limited_paths(n, edges, queries) == expected


def test_large_input_is_fast():
    rng = random.Random(7)
    n, m, q = 50_000, 200_000, 200_000
    edges = [[rng.randrange(n), rng.randrange(n),
              rng.randint(1, 10**8)] for _ in range(m)]
    queries = [[rng.randrange(n), rng.randrange(n),
                rng.randint(1, 10**8)] for _ in range(q)]
    start = time.perf_counter()
    answers = limited_paths(n, edges, queries)
    assert time.perf_counter() - start < 3.0
    assert len(answers) == q
    # a limit above every length connects whatever the edges connect
    top = limited_paths(n, edges, [[0, 1, 10**8 + 1]])[0]
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from((a, b) for a, b, _ in edges)
    assert top == nx.has_path(g, 0, 1)
