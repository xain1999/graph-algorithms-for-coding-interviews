import random
import time

import networkx as nx
import pytest

from solutions.p081_connect_points import min_cost_connect_points
from solutions.p081_connect_points_alt import (
    min_cost_connect_points_kruskal,
)

SOLVERS = [min_cost_connect_points, min_cost_connect_points_kruskal]

EXAMPLE_1 = [[0, 0], [5, 6], [1, 3], [2, 0], [4, 3]]
EXAMPLE_2 = [[-2, 3], [2, -1], [5, 4], [0, 0]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "points, expected",
    [
        (EXAMPLE_1, 13),                    # book example 1
        (EXAMPLE_2, 16),                    # book example 2
        ([[7, -4]], 0),                     # book example 3: one point
        ([[0, 0], [3, 4]], 7),              # Manhattan, not Euclidean
        ([[0, 0], [0, 5], [0, 2], [0, 9]], 9),  # collinear
        ([[0, 0], [1, 1], [2, 2], [3, 3]], 6),
        ([[10**7, 10**7], [-10**7, -10**7]], 4 * 10**7),
    ],
)
def test_examples(solve, points, expected):
    assert solve(points) == expected


def by_networkx(points):
    g = nx.Graph()
    g.add_nodes_from(range(len(points)))
    for i, (x1, y1) in enumerate(points):
        for j in range(i + 1, len(points)):
            x2, y2 = points[j]
            g.add_edge(i, j, weight=abs(x1 - x2) + abs(y1 - y2))
    tree = nx.minimum_spanning_tree(g)
    return int(tree.size(weight="weight"))


def random_points(rng, n, span):
    cells = set()
    while len(cells) < n:
        cells.add((rng.randint(-span, span), rng.randint(-span, span)))
    return [list(c) for c in cells]


def test_random_agree_with_networkx():
    rng = random.Random(1584)
    for _ in range(300):
        points = random_points(rng, rng.randint(1, 12), 6)
        expected = by_networkx(points)
        for solve in SOLVERS:
            assert solve(points) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    points = [p[:] for p in EXAMPLE_1]
    solve(points)
    assert points == EXAMPLE_1


def test_large_input_is_fast():
    rng = random.Random(81)
    points = random_points(rng, 1500, 10**7)
    start = time.perf_counter()
    got = min_cost_connect_points(points)
    assert time.perf_counter() - start < 4.0
    assert got == min_cost_connect_points_kruskal(points)
