import random

import networkx as nx
import pytest

from solutions.p001_path_exists import valid_path
from solutions.p001_path_exists_alt import valid_path_bfs

SOLVERS = [valid_path, valid_path_bfs]

# Book examples 1 and 2 share this graph: {0,1,2,3,4} and {5,6,7}.
EDGES = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [5, 6], [6, 7]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, source, destination, expected",
    [
        (8, EDGES, 0, 4, True),            # book example 1
        (8, EDGES, 1, 7, False),           # book example 2
        (3, [[0, 1]], 2, 2, True),         # source == destination
        (1, [], 0, 0, True),               # smallest graph
        (2, [], 0, 1, False),              # no edges at all
        (2, [[1, 0]], 0, 1, True),         # edge listed backwards
        (2, [[0, 1], [0, 1]], 1, 0, True),  # duplicate edge
        (8, EDGES, 7, 5, True),            # other component
        (8, EDGES, 4, 0, True),            # reversed query
    ],
)
def test_examples(solve, n, edges, source, destination, expected):
    assert solve(n, edges, source, destination) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EDGES]
    solve(8, edges, 0, 4)
    assert edges == EDGES


def test_random_graphs_agree_with_networkx():
    rng = random.Random(1971)
    for _ in range(1500):
        n = rng.randint(1, 9)
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        chosen = rng.sample(pairs, rng.randint(0, len(pairs) // 2))
        edges = [list(p) if rng.random() < 0.5 else [p[1], p[0]]
                 for p in chosen]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(chosen)
        s, d = rng.randrange(n), rng.randrange(n)
        expected = nx.has_path(g, s, d)
        for solve in SOLVERS:
            assert solve(n, edges, s, d) == expected


def test_long_path_is_fast():
    n = 200_000
    edges = [[i, i + 1] for i in range(n - 1)]
    rng = random.Random(7)
    rng.shuffle(edges)
    assert valid_path(n, edges, 0, n - 1)
    assert valid_path_bfs(n, edges, n - 1, 0)
    edges.remove([n // 2, n // 2 + 1])      # cut the path in two
    assert not valid_path(n, edges, 0, n - 1)
