import random

import networkx as nx

from templates.bellman_ford import bellman_ford
from templates.bridges import bridges
from templates.dijkstra import dijkstra
from templates.floyd_warshall import floyd_warshall
from templates.hierholzer import euler_path
from templates.kosaraju import kosaraju
from templates.kruskal import kruskal
from templates.prim import prim
from templates.root_tree import root_tree
from templates.zero_one_bfs import zero_one_bfs

INF = float("inf")


def rand_digraph(rng, n, p, lo=0, hi=9):
    return [[u, v, rng.randint(lo, hi)] for u in range(n)
            for v in range(n) if u != v and rng.random() < p]


def nx_dist(n, edges, s):
    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    for u, v, w in edges:
        if not g.has_edge(u, v) or g[u][v]["weight"] > w:
            g.add_edge(u, v, weight=w)
    d = nx.single_source_bellman_ford_path_length(g, s)
    return [d.get(v, INF) for v in range(n)]


def test_shortest_path_templates():
    rng = random.Random(9)
    for _ in range(400):
        n = rng.randint(1, 8)
        edges = rand_digraph(rng, n, 0.3)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
        want = nx_dist(n, edges, 0)
        assert dijkstra(adj, 0) == want
        assert bellman_ford(n, edges, 0) == want
        assert floyd_warshall(n, edges)[0] == want
        bin_edges = [[u, v, w % 2] for u, v, w in edges]
        badj = [[] for _ in range(n)]
        for u, v, w in bin_edges:
            badj[u].append((v, w))
        assert zero_one_bfs(badj, 0) == nx_dist(n, bin_edges, 0)


def test_bellman_ford_rounds_and_negative_edges():
    edges = [[0, 1, 4], [0, 2, 1], [2, 1, -2], [1, 3, 1]]
    assert bellman_ford(4, edges, 0) == [0, -1, 1, 0]
    assert bellman_ford(4, edges, 0, rounds=1) == [0, 4, 1, INF]


def test_mst_templates():
    rng = random.Random(10)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = [[u, v, rng.randint(1, 9)] for u in range(n)
                 for v in range(u + 1, n) if rng.random() < 0.5]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        for u, v, w in edges:
            if not g.has_edge(u, v) or g[u][v]["weight"] > w:
                g.add_edge(u, v, weight=w)
        if nx.is_connected(g):
            want = int(nx.minimum_spanning_tree(g).size(weight="weight"))
        else:
            want = -1
        assert kruskal(n, edges) == want
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        assert prim(adj) == want


def test_root_tree():
    parent, order = root_tree(5, [[0, 1], [1, 2], [1, 3], [3, 4]], 1)
    assert parent == [1, -1, 1, 1, 3]
    pos = {v: i for i, v in enumerate(order)}
    assert all(parent[v] == -1 or pos[parent[v]] < pos[v]
               for v in range(5))


def test_kosaraju_against_networkx():
    rng = random.Random(11)
    for _ in range(400):
        n = rng.randint(1, 9)
        edges = [e[:2] for e in rand_digraph(rng, n, 0.25)]
        comp = kosaraju(n, edges)
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        groups = {frozenset(c) for c in nx.strongly_connected_components(g)}
        mine = {}
        for v, c in enumerate(comp):
            mine.setdefault(c, set()).add(v)
        assert {frozenset(s) for s in mine.values()} == groups
        for u, v in edges:              # ids in topological order
            assert comp[u] <= comp[v]


def test_bridges_against_networkx():
    rng = random.Random(12)
    for _ in range(400):
        n = rng.randint(1, 9)
        edges = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if rng.random() < 0.3]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        want = {frozenset(e) for e in nx.bridges(g)}
        assert {frozenset(e) for e in bridges(n, edges)} == want


def test_deep_graphs_do_not_recurse():
    n = 200_000
    chain = [[i, i + 1] for i in range(n - 1)]
    assert len(bridges(n, chain)) == n - 1
    assert len(set(kosaraju(n, chain))) == n


def test_euler_path():
    edges = [[0, 1], [1, 2], [2, 0], [0, 3]]
    path = euler_path(edges, 0)
    assert len(path) == 5 and path[0] == 0
    used = sorted([path[i], path[i + 1]] for i in range(4))
    assert used == sorted(edges)
