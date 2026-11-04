import random
import time
from collections import deque

import pytest

from solutions.p084_nary_depth import Node, max_depth
from solutions.p084_nary_depth_dfs import max_depth_dfs
from solutions.p084_nary_depth_rec import max_depth_rec

SOLVERS = [max_depth, max_depth_dfs, max_depth_rec]
ITERATIVE = [max_depth, max_depth_dfs]

EXAMPLE_1 = [7, None, 2, 9, 4, None, None, 1, 8, None, 5,
             None, None, None, 6]
EXAMPLE_2 = [1, None, 2, None, 3, None, 4]


def build_tree(values):
    """Tree from level order: the root, then each node's children in
    queue order, every group of children ended by None."""
    if not values:
        return None
    root = Node(values[0])
    queue = deque([root])
    i = 2                               # values[1] ends the root group
    while queue and i < len(values):
        parent = queue.popleft()
        while i < len(values) and values[i] is not None:
            child = Node(values[i])
            parent.children.append(child)
            queue.append(child)
            i += 1
        i += 1                          # skip the None separator
    return root


def test_build_tree_reads_example_1():
    root = build_tree(EXAMPLE_1)
    assert [c.val for c in root.children] == [2, 9, 4]
    two, nine, four = root.children
    assert two.children == []
    assert [c.val for c in nine.children] == [1, 8]
    assert [c.val for c in four.children] == [5]
    assert [c.val for c in four.children[0].children] == [6]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "values, expected",
    [
        (EXAMPLE_1, 4),                     # book example 1
        (EXAMPLE_2, 4),                     # book example 2: a vine
        ([], 0),                            # book example 3: no tree
        ([5], 1),                           # a lone root
        ([1, None, 2, 3, 4, 5, 6], 2),      # a star
        ([1, None, 2, 3, None, None, 4, None, 5], 4),
    ],
)
def test_examples(solve, values, expected):
    assert solve(build_tree(values)) == expected


def random_tree(rng, n):
    """Random tree on n nodes; returns (root, true depth)."""
    nodes = [Node(0)]
    depth = [1]
    for v in range(1, n):
        p = rng.randrange(v)
        nodes.append(Node(v))
        nodes[p].children.append(nodes[v])
        depth.append(depth[p] + 1)
    return nodes[0], max(depth)


def test_random_trees_agree():
    rng = random.Random(559)
    for _ in range(500):
        root, expected = random_tree(rng, rng.randint(1, 40))
        for solve in SOLVERS:
            assert solve(root) == expected


@pytest.mark.parametrize("solve", ITERATIVE)
def test_deep_vine_needs_no_recursion(solve):
    root = node = Node(0)
    for v in range(1, 10**5):
        child = Node(v)
        node.children.append(child)
        node = child
    assert solve(root) == 10**5


def test_large_random_tree_is_fast():
    rng = random.Random(84)
    root, expected = random_tree(rng, 10**5)
    start = time.perf_counter()
    assert max_depth(root) == expected
    assert max_depth_dfs(root) == expected
    assert time.perf_counter() - start < 1.0
