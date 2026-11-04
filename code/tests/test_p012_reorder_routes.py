import random
import time

import networkx as nx
import pytest

from solutions.p012_reorder_routes import min_reorder
from solutions.p012_reorder_routes_alt import min_reorder_sets
from solutions.p012_reorder_routes_brute import min_reorder_brute

SOLVERS = [min_reorder, min_reorder_sets, min_reorder_brute]

EXAMPLE_1 = [[0, 1], [0, 2], [3, 1], [1, 4], [5, 2], [2, 6]]
EXAMPLE_2 = [[1, 0], [2, 0], [3, 2], [4, 2]]
EXAMPLE_3 = [[0, 1], [1, 2], [2, 3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, connections, expected",
    [
        (7, EXAMPLE_1, 4),          # book example 1 (mixed directions)
        (5, EXAMPLE_2, 0),          # book example 2 (already fine)
        (4, EXAMPLE_3, 3),          # former example 3: all point away
        (2, [[0, 1]], 1),           # smallest input, wrong way
        (2, [[1, 0]], 0),           # smallest input, right way
        (4, [[0, 1], [0, 2], [0, 3]], 3),   # star pointing out
        (4, [[3, 2], [2, 1], [1, 0]], 0),   # chain pointing in
        # 0 is a leaf at the end of a chain pointing away from it
        (4, [[0, 3], [3, 2], [2, 1]], 3),
    ],
)
def test_examples(solve, n, connections, expected):
    assert solve(n, connections) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    roads = [road[:] for road in EXAMPLE_1]
    solve(7, roads)
    assert roads == EXAMPLE_1


def random_tree(rng: random.Random) -> tuple[int, list[list[int]]]:
    n = rng.randint(2, 12)
    order = list(range(n))
    rng.shuffle(order)
    roads = []
    for i in range(1, n):
        a, b = order[i], order[rng.randrange(i)]
        roads.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(roads)
    return n, roads


def flips_by_networkx(n: int, roads: list[list[int]]) -> int:
    """Count roads whose head is farther from 0 than their tail."""
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(roads)
    depth = nx.single_source_shortest_path_length(g, 0)
    return sum(1 for a, b in roads if depth[b] > depth[a])


def test_random_trees_agree():
    rng = random.Random(1466)
    for _ in range(1000):
        n, roads = random_tree(rng)
        expected = flips_by_networkx(n, roads)
        for solve in SOLVERS:
            assert solve(n, roads) == expected


def test_answer_after_flipping_reaches_zero():
    # Flip exactly the roads the answer counts, then check with
    # networkx that every city has a directed path to 0.
    rng = random.Random(7)
    for _ in range(300):
        n, roads = random_tree(rng)
        g = nx.Graph(roads)
        depth = nx.single_source_shortest_path_length(g, 0)
        fixed = nx.DiGraph()
        fixed.add_nodes_from(range(n))
        for a, b in roads:
            fixed.add_edge(*((b, a) if depth[b] > depth[a] else (a, b)))
        assert len(nx.ancestors(fixed, 0)) == n - 1
        assert min_reorder(n, roads) == sum(
            1 for a, b in roads if depth[b] > depth[a])


def test_large_tree_is_fast():
    n = 100_000
    chain = [[i, i + 1] for i in range(n - 1)]  # deep: 0 -> ... -> n-1
    start = time.perf_counter()
    assert min_reorder(n, chain) == n - 1
    assert min_reorder_sets(n, chain) == n - 1
    rng = random.Random(5)
    roads = [[rng.randrange(i), i] if rng.random() < 0.5
             else [i, rng.randrange(i)] for i in range(1, n)]
    assert min_reorder(n, roads) == sum(1 for a, b in roads if a < b)
    assert time.perf_counter() - start < 3.0
