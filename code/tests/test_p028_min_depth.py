import random
from collections import deque

import pytest

from solutions.p028_min_depth import TreeNode, min_depth
from solutions.p028_min_depth_dfs import min_depth_dfs

SOLVERS = [min_depth, min_depth_dfs]


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


def to_level_order(root):
    """Inverse of build_tree (trailing Nones dropped)."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


EXAMPLE_1 = [8, 4, 12, 2, 6, None, 14, 1, 3, None, None, 13, 15]
EXAMPLE_2 = [5, 3, None, None, 9, 7]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "values, expected",
    [
        (EXAMPLE_1, 3),                 # book example 1
        (EXAMPLE_2, 4),                 # book example 2 (zigzag vine)
        ([], 0),                        # book example 3 (no tree)
        ([42], 1),                      # a lone root is a leaf
        ([1, 2], 2),                    # one child: not a leaf
        ([1, None, 2], 2),
        ([1, 2, 3], 2),
        ([1, 2, 3, 4, 5, None, None, 6], 2),   # leaf 3 at depth 2
        ([1, 2, 3, None, 4, None, 5, 6, None, None, 7], 4),
    ],
)
def test_examples(solve, values, expected):
    assert solve(build_tree(values)) == expected


def test_helper_round_trip():
    assert to_level_order(build_tree(EXAMPLE_1)) == EXAMPLE_1
    assert to_level_order(build_tree(EXAMPLE_2)) == EXAMPLE_2


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_tree(solve):
    root = build_tree(EXAMPLE_1)
    solve(root)
    assert to_level_order(root) == EXAMPLE_1


def random_tree(rng, size):
    root = TreeNode(0)
    free = [(root, "left"), (root, "right")]
    for val in range(1, size):
        i = rng.randrange(len(free))
        parent, side = free.pop(i)
        child = TreeNode(val)
        setattr(parent, side, child)
        free += [(child, "left"), (child, "right")]
    return root


def leaf_depths(root):
    """Depth of every leaf, by an explicit-stack DFS."""
    depths, stack = [], [(root, 1)]
    while stack:
        node, d = stack.pop()
        kids = [k for k in (node.left, node.right) if k]
        if not kids:
            depths.append(d)
        stack += [(k, d + 1) for k in kids]
    return depths


def test_random_trees_agree():
    rng = random.Random(111)
    for _ in range(1500):
        root = random_tree(rng, rng.randint(1, 40))
        expected = min(leaf_depths(root))
        assert min_depth(root) == expected
        assert min_depth_dfs(root) == expected


def test_long_chain_is_fast_and_iterative():
    n = 200_000
    root = node = TreeNode(0)
    for val in range(1, n):             # a vine, alternating sides
        child = TreeNode(val)
        if val % 2:
            node.left = child
        else:
            node.right = child
        node = child
    assert min_depth(root) == n


def test_bfs_stops_early_on_huge_tree():
    # A leaf at depth 2 next to a 200k-node chain: BFS stops at once.
    root = TreeNode(0, TreeNode(1), TreeNode(2))
    node = root.right
    for val in range(3, 200_000):
        node.right = TreeNode(val)
        node = node.right
    assert min_depth(root) == 2


def test_naive_min_formula_is_wrong_as_the_book_says():
    def naive(node):
        if node is None:
            return 0
        return 1 + min(naive(node.left), naive(node.right))

    assert naive(build_tree(EXAMPLE_1)) == 2    # true answer 3
    assert naive(build_tree(EXAMPLE_2)) == 1    # true answer 4
