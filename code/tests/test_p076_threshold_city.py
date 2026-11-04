import random
import time

import networkx as nx
import pytest

from solutions.p076_threshold_city import find_the_city
from solutions.p076_threshold_city_alt import find_the_city_dijkstra
from solutions.p076_threshold_city_brute import find_the_city_brute

SOLVERS = [find_the_city, find_the_city_dijkstra, find_the_city_brute]

ROADS_1 = [[0, 1, 3], [1, 2, 2], [2, 3, 4], [3, 4, 1], [0, 4, 8],
           [1, 3, 7]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, roads, threshold, expected",
    [
        (5, ROADS_1, 6, 4),                  # book example 1
        (4, [[0, 1, 5], [1, 2, 5], [2, 3, 5]], 4, 3),  # example 2
        (4, [[0, 1, 1], [1, 3, 1], [3, 2, 1]], 2, 2),  # loop trap
        (2, [], 10, 1),                      # nobody reachable: tie
        (2, [[0, 1, 3]], 3, 1),              # threshold is inclusive
        (3, [[0, 1, 1], [0, 1, 9], [1, 2, 1]], 1, 2),  # parallel
        (3, [[0, 1, 4], [1, 2, 4], [0, 2, 1]], 2, 1),
    ],
)
def test_examples(solve, n, roads, threshold, expected):
    assert solve(n, roads, threshold) == expected


def wrong_order_dist(n, roads):
    """k as the innermost loop: the classic Floyd-Warshall bug."""
    inf = float("inf")
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for a, b, w in roads:
        d[a][b] = d[b][a] = min(d[a][b], w)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def test_wrong_loop_order_misses_a_route():
    chain = [[0, 1, 1], [1, 3, 1], [3, 2, 1]]
    assert wrong_order_dist(4, chain)[0][2] == float("inf")


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    roads = [r[:] for r in ROADS_1]
    solve(5, roads, 6)
    assert roads == ROADS_1


def nx_answer(n, roads, threshold):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for a, b, w in roads:
        if not g.has_edge(a, b) or g[a][b]["weight"] > w:
            g.add_edge(a, b, weight=w)
    dist = dict(nx.all_pairs_dijkstra_path_length(g))
    counts = [sum(1 for j, d in dist[i].items()
                  if j != i and d <= threshold) for i in range(n)]
    low = min(counts)
    return max(i for i in range(n) if counts[i] == low)


def test_random_agree_with_networkx():
    rng = random.Random(1334)
    for _ in range(500):
        n = rng.randint(2, 8)
        roads = []
        for _ in range(rng.randint(0, 14)):
            a, b = rng.sample(range(n), 2)
            roads.append([a, b, rng.randint(1, 9)])
        threshold = rng.randint(1, 20)
        expected = nx_answer(n, roads, threshold)
        for solve in SOLVERS:
            assert solve(n, roads, threshold) == expected


def test_large_dense_input_is_fast():
    rng = random.Random(9)
    n = 120
    roads = [[a, b, rng.randint(1, 5000)]
             for a in range(n) for b in range(a + 1, n)][:7000]
    start = time.perf_counter()
    ans = find_the_city(n, roads, 3000)
    assert time.perf_counter() - start < 3.0
    assert ans == find_the_city_dijkstra(n, roads, 3000)
