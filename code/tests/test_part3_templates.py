import random

import networkx as nx

from templates.bipartite import two_color
from templates.topo_dfs import topo_order_dfs
from templates.topo_kahn import topo_order
from templates.union_find import UnionFind

# Graphs drawn in the chapter openers.
CH06_EDGES = [[0, 2], [1, 2], [1, 3], [2, 4], [3, 4], [4, 5]]
CH08_EVEN = [[1, 2], [0, 3], [0, 3], [1, 2]]          # 4-cycle
CH08_ODD = [[1, 2], [0, 2], [0, 1]]                   # triangle


def valid_order(n, edges, order):
    pos = {v: i for i, v in enumerate(order)}
    return len(order) == n and all(pos[u] < pos[v] for u, v in edges)


def test_ch06_example():
    assert topo_order(6, CH06_EDGES) == [0, 1, 2, 3, 4, 5]
    assert valid_order(6, CH06_EDGES, topo_order_dfs(6, CH06_EDGES))
    cyc = CH06_EDGES + [[5, 1]]
    assert topo_order(6, cyc) == [] and topo_order_dfs(6, cyc) == []


def test_topo_random_against_networkx():
    rng = random.Random(6)
    for _ in range(800):
        n = rng.randint(1, 9)
        edges = [[u, v] for u in range(n) for v in range(n)
                 if u != v and rng.random() < 0.18]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        acyclic = nx.is_directed_acyclic_graph(g)
        for solve in (topo_order, topo_order_dfs):
            order = solve(n, edges)
            if acyclic:
                assert valid_order(n, edges, order)
            else:
                assert order == []


def test_topo_deep_chain():
    n = 200_000
    edges = [[i, i + 1] for i in range(n - 1)]
    assert topo_order_dfs(n, edges) == list(range(n))
    assert topo_order(n, edges) == list(range(n))


def test_union_find_against_networkx():
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(1, 12)
        uf = UnionFind(n)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        for _ in range(rng.randint(0, 15)):
            a, b = rng.randrange(n), rng.randrange(n)
            merged = uf.union(a, b)
            assert merged == (not nx.has_path(g, a, b))
            g.add_edge(a, b)
            assert uf.count == nx.number_connected_components(g)
        for comp in nx.connected_components(g):
            roots = {uf.find(v) for v in comp}
            assert len(roots) == 1
            assert uf.size[roots.pop()] == len(comp)


def test_union_find_chain_is_fast():
    n = 300_000
    uf = UnionFind(n)
    for i in range(n - 1):
        uf.union(i, i + 1)
    assert uf.count == 1 and uf.find(0) == uf.find(n - 1)


def test_two_color():
    assert two_color(CH08_EVEN) == [0, 1, 1, 0]
    assert two_color(CH08_ODD) is None
    rng = random.Random(8)
    for _ in range(500):
        n = rng.randint(1, 10)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n)
                 if rng.random() < 0.25]
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        color = two_color(graph)
        assert (color is not None) == nx.is_bipartite(g)
        if color is not None:
            assert all(color[u] != color[v] for u, v in edges)
