import random

import networkx as nx
import pytest

from solutions.p029_fewest_hops import fewest_hops
from solutions.p029_fewest_hops_path import shortest_route

# Book examples 1-3 share this graph; node 8 has no edges.
EDGES = [[0, 1], [0, 4], [1, 2], [1, 5], [4, 5], [2, 3], [3, 6],
         [5, 6], [6, 7]]


@pytest.mark.parametrize(
    "n, edges, source, target, expected",
    [
        (9, EDGES, 0, 7, 4),            # book example 1
        (9, EDGES, 0, 8, -1),           # book example 2
        (9, EDGES, 5, 5, 0),            # book example 3
        (1, [], 0, 0, 0),               # smallest graph
        (2, [], 0, 1, -1),              # no edges
        (2, [[1, 0]], 0, 1, 1),         # edge listed backwards
        (3, [[0, 1], [0, 1], [1, 2]], 2, 0, 2),  # duplicate edge
        (9, EDGES, 7, 0, 4),            # reversed query
        (9, EDGES, 2, 4, 3),
    ],
)
def test_examples(n, edges, source, target, expected):
    assert fewest_hops(n, edges, source, target) == expected
    route = shortest_route(n, edges, source, target)
    assert len(route) - 1 == expected


def test_example_route():
    assert shortest_route(9, EDGES, 0, 7) == [0, 1, 5, 6, 7]
    assert shortest_route(9, EDGES, 0, 8) == []
    assert shortest_route(9, EDGES, 5, 5) == [5]


def test_does_not_mutate_input():
    edges = [e[:] for e in EDGES]
    fewest_hops(9, edges, 0, 7)
    shortest_route(9, edges, 0, 7)
    assert edges == EDGES


def test_random_graphs_agree_with_networkx():
    rng = random.Random(29)
    for _ in range(1500):
        n = rng.randint(1, 10)
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        chosen = rng.sample(pairs, rng.randint(0, len(pairs) // 3))
        edges = [list(p) if rng.random() < 0.5 else [p[1], p[0]]
                 for p in chosen]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(chosen)
        s, t = rng.randrange(n), rng.randrange(n)
        try:
            expected = nx.shortest_path_length(g, s, t)
        except nx.NetworkXNoPath:
            expected = -1
        assert fewest_hops(n, edges, s, t) == expected
        route = shortest_route(n, edges, s, t)
        if expected == -1:
            assert route == []
        else:
            assert len(route) == expected + 1
            assert route[0] == s and route[-1] == t
            assert all(g.has_edge(a, b)
                       for a, b in zip(route, route[1:]))


def test_large_graph_is_fast():
    n = 100_000
    edges = [[i, i + 1] for i in range(n - 1)]
    edges += [[i, i + 1000] for i in range(0, n - 1000, 1000)]
    rng = random.Random(5)
    rng.shuffle(edges)
    # Express lane: 99 jumps of 1000, then 999 single steps.
    assert fewest_hops(n, edges, 0, n - 1) == 99 + 999
    assert len(shortest_route(n, edges, 0, n - 1)) == 99 + 999 + 1
