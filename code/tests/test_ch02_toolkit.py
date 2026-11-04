import random
import runpy
from pathlib import Path

import networkx as nx

from templates.bfs import bfs_order
from templates.bfs_levels import bfs_levels
from templates.build_graph import build_graph, build_graph_dict
from templates.components import count_components
from templates.dfs_iterative import dfs_iterative
from templates.dfs_recursive import dfs_recursive
from templates.grid import grid_neighbors

SNIPPETS = Path(__file__).resolve().parents[1] / "snippets"

# The example graph drawn in Chapter 2.
EXAMPLE_EDGES = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [5, 6]]


def random_graph(rng, directed=False):
    n = rng.randint(1, 10)
    edges = [[u, v] for u in range(n) for v in range(n)
             if u != v and rng.random() < 0.2]
    if not directed:
        edges = [e for e in edges if e[0] < e[1]]
    return n, edges


def test_build_graph_example():
    g = build_graph(7, EXAMPLE_EDGES)
    assert g == [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3], [6], [5]]
    d = build_graph(3, [[0, 1], [1, 2]], directed=True)
    assert d == [[1], [2], []]


def test_build_graph_dict():
    g = build_graph_dict([("a", "b"), ("b", "c")])
    assert g == {"a": ["b"], "b": ["a", "c"], "c": ["b"]}
    assert build_graph_dict([("a", "b")], directed=True)["b"] == []


def test_example_orders():
    g = build_graph(7, EXAMPLE_EDGES)
    assert dfs_recursive(g, 0) == [0, 1, 3, 2, 4]
    assert dfs_iterative(g, 0) == [0, 1, 3, 2, 4]
    assert bfs_order(g, 0) == [0, 1, 2, 3, 4]
    assert bfs_levels(g, 0) == [[0], [1, 2], [3], [4]]
    assert count_components(g) == 2


def test_iterative_matches_recursive_and_networkx():
    rng = random.Random(2)
    for _ in range(500):
        directed = rng.random() < 0.5
        n, edges = random_graph(rng, directed)
        g = build_graph(n, edges, directed)
        rec = dfs_recursive(g, 0)
        assert dfs_iterative(g, 0) == rec
        G = nx.DiGraph() if directed else nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        if directed:
            assert set(rec) == {0} | nx.descendants(G, 0)
        else:
            assert set(rec) == nx.node_connected_component(G, 0)
        assert set(bfs_order(g, 0)) == set(rec)
        dist = nx.single_source_shortest_path_length(G, 0)
        for d, level in enumerate(bfs_levels(g, 0)):
            assert all(dist[v] == d for v in level)
        if not directed:
            assert count_components(g) == nx.number_connected_components(G)


def test_deep_graph_iterative_only():
    n = 200_000
    g = build_graph(n, [[i, i + 1] for i in range(n - 1)])
    assert len(dfs_iterative(g, 0)) == n
    assert count_components(g) == 1


def test_grid_neighbors():
    grid = [[0] * 3 for _ in range(2)]
    assert sorted(grid_neighbors(grid, 0, 0)) == [(0, 1), (1, 0)]
    assert sorted(grid_neighbors(grid, 1, 1)) == [(0, 1), (1, 0), (1, 2)]


def test_snippets():
    ns = runpy.run_path(str(SNIPPETS / "ch02_deque.py"))
    assert ns["first"] == 1 and ns["last"] == 3
    assert list(ns["queue"]) == [0, 2]
    ns = runpy.run_path(str(SNIPPETS / "ch02_heapq.py"))
    assert ns["smallest"] == (1, "a") and ns["peek"] == (3, "c")
    assert ns["largest"] == 9
    ns = runpy.run_path(str(SNIPPETS / "ch02_counting.py"))
    assert ns["indegree"] == {1: 2, 2: 1}
    assert ns["outdegree"] == {0: 2, 2: 1} and ns["zero"] == 0
    assert dict(ns["graph"]) == {0: [1, 2], 2: [1]}
