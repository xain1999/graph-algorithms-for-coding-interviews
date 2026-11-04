import random
import time
from collections import deque

import networkx as nx
import pytest

from solutions.p087_distance_k import TreeNode, distance_k
from solutions.p087_distance_k_rec import distance_k_rec

SOLVERS = [distance_k, distance_k_rec]


def build_tree(values):
    """Tree from a level-order list; None marks a missing child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def all_nodes(root):
    out, stack = [], [root]
    while stack:
        node = stack.pop()
        out.append(node)
        stack += [c for c in (node.left, node.right) if c]
    return out


def find(root, val):
    return next(n for n in all_nodes(root) if n.val == val)


def shape(root):
    """Nested tuples, to check the tree is left untouched."""
    if root is None:
        return None
    return (root.val, shape(root.left), shape(root.right))


EXAMPLE_1 = [7, 3, 12, 1, 5, 9, 15, None, 2, 4, 6]
EXAMPLE_2 = [10, 20, None, 30, None, 40]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "values, target, k, expected",
    [
        (EXAMPLE_1, 5, 3, [2, 12]),          # book example 1
        (EXAMPLE_2, 30, 1, [20, 40]),        # book example 2
        (EXAMPLE_1, 5, 0, [5]),              # k = 0: the target
        (EXAMPLE_1, 5, 2, [1, 7]),
        (EXAMPLE_1, 5, 4, [9, 15]),
        (EXAMPLE_1, 5, 5, []),               # beyond the farthest
        (EXAMPLE_1, 7, 2, [1, 5, 9, 15]),    # target is the root
        ([8], 8, 0, [8]),
        ([8], 8, 2, []),
    ],
)
def test_examples(solve, values, target, k, expected):
    root = build_tree(values)
    assert sorted(solve(root, find(root, target), k)) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_tree(solve):
    root = build_tree(EXAMPLE_1)
    before = shape(root)
    solve(root, find(root, 5), 3)
    assert shape(root) == before


def random_tree(n, rng):
    values = rng.sample(range(1000), n)
    nodes = [TreeNode(v) for v in values]
    for i in range(1, n):
        while True:
            par = nodes[rng.randrange(i)]
            side = rng.choice(("left", "right"))
            if getattr(par, side) is None:
                setattr(par, side, nodes[i])
                break
    return nodes[0], nodes


def test_random_trees_agree_with_networkx():
    rng = random.Random(863)
    for _ in range(400):
        root, nodes = random_tree(rng.randint(1, 30), rng)
        graph = nx.Graph()
        graph.add_nodes_from(n.val for n in nodes)
        for n in nodes:
            for c in (n.left, n.right):
                if c:
                    graph.add_edge(n.val, c.val)
        target = rng.choice(nodes)
        dist = nx.single_source_shortest_path_length(graph, target.val)
        for k in range(0, 8):
            want = sorted(v for v, d in dist.items() if d == k)
            assert sorted(distance_k(root, target, k)) == want
            assert sorted(distance_k_rec(root, target, k)) == want


def test_long_vine_is_fast():
    n = 100_000
    nodes = [TreeNode(i) for i in range(n)]
    for i in range(n - 1):
        nodes[i].right = nodes[i + 1]
    start = time.perf_counter()
    got = distance_k(nodes[0], nodes[n // 2], 50_000)
    assert got == [0]
    assert time.perf_counter() - start < 2.0
