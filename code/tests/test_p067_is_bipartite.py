import random
import time

import networkx as nx
import pytest

from solutions.p067_is_bipartite import is_bipartite
from solutions.p067_is_bipartite_brute import is_bipartite_brute
from solutions.p067_is_bipartite_uf import is_bipartite_uf

SOLVERS = [is_bipartite, is_bipartite_uf, is_bipartite_brute]

EXAMPLE_1 = [[1], [0, 2], [1], [4, 7], [3, 5], [4, 6], [5, 7],
             [6, 3]]
EXAMPLE_2 = [[3, 4], [3, 4], [5], [0, 1], [1, 0], [2, 6], [5]]
EXAMPLE_3 = [[]]


def to_adjacency(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "graph, expected",
    [
        (EXAMPLE_1, False),                 # book example 1 (5-cycle)
        (EXAMPLE_2, True),                  # book example 2
        (EXAMPLE_3, True),                  # single isolated node
        ([[], []], True),                   # no edges at all
        ([[1], [0]], True),
        ([[1, 2], [0, 2], [0, 1]], False),  # triangle
        ([[], [2, 3], [1, 3], [1, 2]], False),  # 0 is isolated
        ([[1, 3], [0, 2], [1, 3], [2, 0]], True),   # square
    ],
)
def test_examples(solve, graph, expected):
    assert solve(graph) == expected


def test_node_zero_only_bug_is_caught():
    # Coloring only from node 0 would answer True here.
    from collections import deque
    color = [-1] * len(EXAMPLE_1)
    color[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in EXAMPLE_1[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                queue.append(v)
    assert all(color[u] != color[v] for u in range(3)
               for v in EXAMPLE_1[u])
    assert is_bipartite(EXAMPLE_1) is False


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    graph = [row[:] for row in EXAMPLE_1]
    solve(graph)
    assert graph == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(785)
    for _ in range(1500):
        n = rng.randint(1, 10)
        p = rng.choice((0.1, 0.2, 0.35, 0.5))
        edges = [(u, v) for u in range(n) for v in range(u + 1, n)
                 if rng.random() < p]
        graph = to_adjacency(n, edges)
        for row in graph:
            rng.shuffle(row)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.is_bipartite(g)
        assert is_bipartite(graph) == expected, graph
        assert is_bipartite_uf(graph) == expected, graph
        if n <= 8:
            assert is_bipartite_brute(graph) == expected, graph


@pytest.mark.parametrize("solve", [is_bipartite, is_bipartite_uf])
def test_large_graph_is_fast(solve):
    rng = random.Random(3)
    n = 2000
    # Random edges between even and odd labels: bipartite.
    edges = set()
    while len(edges) < 100_000:
        u = 2 * rng.randrange(n // 2)
        v = 2 * rng.randrange(n // 2) + 1
        edges.add((u, v))
    graph = to_adjacency(n, edges)
    start = time.perf_counter()
    assert solve(graph) is True
    graph[0].append(2)                  # one even-even edge breaks it
    graph[2].append(0)
    assert solve(graph) is False
    assert time.perf_counter() - start < 2.0
