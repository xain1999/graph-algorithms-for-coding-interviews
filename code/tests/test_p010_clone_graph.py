import random
import sys
from collections import deque

import networkx as nx
import pytest

from solutions.p010_clone_graph import Node, clone_graph
from solutions.p010_clone_graph_alt import clone_graph_bfs

SOLVERS = [clone_graph, clone_graph_bfs]

# Book examples as adjacency lists: adj[i] = neighbors of node i + 1.
EXAMPLE_1 = [[2, 5], [1, 3, 5], [2, 4], [3, 5], [1, 2, 4]]
EXAMPLE_2 = [[2, 3], [1, 3], [1, 2, 4], [3]]
EXAMPLE_3 = [[2], [1, 3], [2]]


def build(adj: list[list[int]]) -> Node | None:
    """Make Node objects from an adjacency list; return node 1."""
    if not adj:
        return None
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nbrs in enumerate(adj):
        nodes[i].neighbors = [nodes[v - 1] for v in nbrs]
    return nodes[0]


def collect(start: Node | None) -> list[Node]:
    """Every node reachable from start, in BFS order."""
    if start is None:
        return []
    seen = {id(start)}
    order = [start]
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in node.neighbors:
            if id(nxt) not in seen:
                seen.add(id(nxt))
                order.append(nxt)
                queue.append(nxt)
    return order


def to_adj(start: Node | None) -> list[list[int]]:
    """Read an adjacency list back from a graph of Node objects."""
    nodes = collect(start)
    if not nodes:
        return []
    adj = [[] for _ in nodes]
    for node in nodes:
        adj[node.val - 1] = [nxt.val for nxt in node.neighbors]
    return adj


def assert_is_deep_copy(original: Node | None, copy: Node | None):
    if original is None:
        assert copy is None
        return
    old_nodes = collect(original)
    new_nodes = collect(copy)
    # No original object may appear anywhere in the copy.
    assert not {id(n) for n in old_nodes} & {id(n) for n in new_nodes}
    assert len(old_nodes) == len(new_nodes)
    # Walk both graphs in lockstep: the pairing must be a bijection
    # that preserves values and neighbor lists, in order.
    pair = {id(original): copy}
    queue = deque([original])
    while queue:
        old = queue.popleft()
        new = pair[id(old)]
        assert new.val == old.val
        assert len(new.neighbors) == len(old.neighbors)
        for o, n in zip(old.neighbors, new.neighbors):
            if id(o) in pair:
                assert pair[id(o)] is n     # same node, same copy
            else:
                pair[id(o)] = n
                queue.append(o)
    assert len({id(n) for n in pair.values()}) == len(old_nodes)


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "adj",
    [
        EXAMPLE_1,                  # book example 1 (several cycles)
        EXAMPLE_2,                  # book example 2 (triangle + tail)
        EXAMPLE_3,                  # path, no cycle
        [],                         # no graph at all
        [[]],                       # one node, no edges
        [[2], [1]],                 # one edge
        [[2, 3], [1, 3], [1, 2]],   # triangle
        [[1]],                      # self-loop
        [[2, 3, 4], [1], [1], [1]],                 # star
        [[2], [1, 3], [2, 4], [3, 5], [4]],         # path
        [[2, 3, 4], [1, 3, 4], [1, 2, 4], [1, 2, 3]],  # complete
    ],
)
def test_examples(solve, adj):
    original = build(adj)
    copy = solve(original)
    assert to_adj(copy) == adj
    assert_is_deep_copy(original, copy)


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    original = build(EXAMPLE_1)
    nodes = collect(original)
    before = [(n, n.val, list(n.neighbors)) for n in nodes]
    solve(original)
    after = [(n, n.val, list(n.neighbors)) for n in collect(original)]
    assert len(before) == len(after)
    for (a, va, na), (b, vb, nb) in zip(before, after):
        assert a is b and va == vb
        assert all(x is y for x, y in zip(na, nb))
        assert len(na) == len(nb)


@pytest.mark.parametrize("solve", SOLVERS)
def test_clone_is_independent(solve):
    original = build(EXAMPLE_2)
    copy = solve(original)
    copy.neighbors.pop()
    copy.neighbors[0].val = 99
    assert to_adj(original) == EXAMPLE_2


def random_connected_adj(rng: random.Random) -> list[list[int]]:
    n = rng.randint(1, 9)
    edges = set()
    for v in range(2, n + 1):           # random spanning tree first
        edges.add((rng.randint(1, v - 1), v))
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < 0.3:
                edges.add((u, v))
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u - 1].append(v)
        adj[v - 1].append(u)
    for nbrs in adj:
        rng.shuffle(nbrs)
    return adj


def test_random_graphs_are_isomorphic_copies():
    rng = random.Random(133)
    for _ in range(500):
        adj = random_connected_adj(rng)
        original = build(adj)
        for solve in SOLVERS:
            copy = solve(original)
            assert to_adj(copy) == adj
            assert_is_deep_copy(original, copy)
            g_old, g_new = nx.Graph(), nx.Graph()
            for g, start in ((g_old, original), (g_new, copy)):
                for node in collect(start):
                    g.add_node(node.val)
                    for nxt in node.neighbors:
                        g.add_edge(node.val, nxt.val)
            assert nx.utils.graphs_equal(g_old, g_new)


def test_large_graph_is_fast():
    n = 2000                            # long path plus chords
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        adj[v - 1].append(v + 1)
        adj[v].append(v)
    for v in range(1, n - 10, 7):
        adj[v - 1].append(v + 10)
        adj[v + 9].append(v)
    original = build(adj)
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(10_000)       # the recursive DFS goes deep
    try:
        for solve in SOLVERS:
            copy = solve(original)
            assert to_adj(copy) == adj
            assert_is_deep_copy(original, copy)
    finally:
        sys.setrecursionlimit(limit)
