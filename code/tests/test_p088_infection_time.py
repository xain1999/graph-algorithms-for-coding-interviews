import random
import time
from collections import deque

import networkx as nx
import pytest

from solutions.p088_infection_time import TreeNode, amount_of_time
from solutions.p088_infection_time_brute import amount_of_time_brute

SOLVERS = [amount_of_time, amount_of_time_brute]


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


def shape(root):
    if root is None:
        return None
    return (root.val, shape(root.left), shape(root.right))


EXAMPLE_1 = [3, 6, 8, 2, 4, 1, None, 5, None, None, None, None, 9]
EXAMPLE_2 = [4, 9, 6]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "values, start, expected",
    [
        (EXAMPLE_1, 1, 5),                   # book example 1
        (EXAMPLE_2, 9, 2),                   # book example 2
        (EXAMPLE_1, 3, 3),                   # start at the root: height
        (EXAMPLE_1, 5, 6),                   # start at a deep leaf
        (EXAMPLE_1, 6, 4),
        ([11], 11, 0),                       # a lone node
        ([1, None, 2, None, 3, None, 4], 3, 2),
    ],
)
def test_examples(solve, values, start, expected):
    assert solve(build_tree(values), start) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_tree(solve):
    root = build_tree(EXAMPLE_1)
    before = shape(root)
    solve(root, 1)
    assert shape(root) == before


def random_tree(n, rng):
    values = rng.sample(range(10 * n), n)
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
    rng = random.Random(2385)
    for _ in range(500):
        root, nodes = random_tree(rng.randint(1, 40), rng)
        graph = nx.Graph()
        graph.add_nodes_from(n.val for n in nodes)
        for n in nodes:
            for c in (n.left, n.right):
                if c:
                    graph.add_edge(n.val, c.val)
        start = rng.choice(nodes).val
        want = nx.eccentricity(graph, v=start)
        assert amount_of_time(root, start) == want
        assert amount_of_time_brute(root, start) == want


def test_large_trees_are_fast():
    n = 100_000
    vine = [TreeNode(i) for i in range(n)]
    for i in range(n - 1):              # a vine: the deepest shape
        vine[i].left = vine[i + 1]
    full = [TreeNode(i) for i in range(n)]
    for i in range(1, n):               # a complete binary tree
        if i % 2:
            full[(i - 1) // 2].left = full[i]
        else:
            full[(i - 1) // 2].right = full[i]
    start = time.perf_counter()
    assert amount_of_time(vine[0], 40_000) == 59_999
    assert amount_of_time(full[0], n - 1) == 32   # leaf to leaf
    assert time.perf_counter() - start < 2.0
