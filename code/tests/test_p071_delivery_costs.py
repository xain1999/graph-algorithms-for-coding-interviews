import random
import time

import networkx as nx
import pytest

from solutions.p071_delivery_costs import cheapest_costs
from solutions.p071_delivery_costs_brute import cheapest_costs_brute

SOLVERS = [cheapest_costs, cheapest_costs_brute]

ROADS_1 = [[0, 1, 7], [0, 2, 2], [2, 1, 3], [1, 3, 1], [2, 3, 8],
           [3, 4, 2], [4, 2, 1], [5, 0, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, roads, source, expected",
    [
        (6, ROADS_1, 0, [0, 5, 2, 6, 8, -1]),          # book example 1
        (4, [[1, 2, 0], [2, 3, 4], [3, 1, 1], [0, 3, 2]], 1,
         [-1, 0, 0, 4]),                             # book example 2
        (1, [], 0, [0]),                             # smallest input
        (3, [], 1, [-1, 0, -1]),                     # no roads
        (2, [[0, 1, 5], [0, 1, 3], [0, 1, 9]], 0, [0, 3]),  # parallel
        (2, [[0, 0, 4], [0, 1, 1]], 0, [0, 1]),      # self-loop
        (3, [[0, 1, 0], [1, 2, 0]], 0, [0, 0, 0]),   # free roads
        (2, [[1, 0, 1]], 0, [0, -1]),                # one-way only
    ],
)
def test_examples(solve, n, roads, source, expected):
    assert solve(n, roads, source) == expected


def test_does_not_mutate_input():
    roads = [r[:] for r in ROADS_1]
    for solve in SOLVERS:
        solve(6, roads, 0)
    assert roads == ROADS_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(71)
    for _ in range(600):
        n = rng.randint(1, 9)
        m = rng.randint(0, 3 * n)
        roads = [[rng.randrange(n), rng.randrange(n), rng.randint(0, 9)]
                 for _ in range(m)]
        source = rng.randrange(n)
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        for u, v, w in roads:           # keep the cheapest parallel road
            if not g.has_edge(u, v) or g[u][v]["weight"] > w:
                g.add_edge(u, v, weight=w)
        lengths = nx.single_source_dijkstra_path_length(g, source)
        expected = [lengths.get(v, -1) for v in range(n)]
        for solve in SOLVERS:
            assert solve(n, roads, source) == expected


def test_large_input_is_fast():
    rng = random.Random(7)
    n, m = 30_000, 100_000
    roads = [[i, i + 1, 1] for i in range(n - 1)]
    roads += [[rng.randrange(n), rng.randrange(n),
               rng.randint(0, 50_000)] for _ in range(m - (n - 1))]
    start = time.perf_counter()
    costs = cheapest_costs(n, roads, 0)
    assert time.perf_counter() - start < 2.0
    assert costs[0] == 0 and all(0 <= c <= n for c in costs)
