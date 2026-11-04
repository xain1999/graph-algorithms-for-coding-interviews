import random
import time

import networkx as nx
import pytest

from solutions.p072_network_delay import network_delay_time
from solutions.p072_network_delay_brute import network_delay_time_brute

SOLVERS = [network_delay_time, network_delay_time_brute]

TIMES_1 = [[3, 1, 3], [3, 2, 9], [1, 2, 4], [2, 4, 2], [1, 5, 10],
           [4, 5, 1]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "times, n, k, expected",
    [
        (TIMES_1, 5, 3, 10),                         # book example 1
        ([[1, 2, 5], [2, 3, 1], [4, 3, 2]], 4, 1, -1),   # book example 2
        ([], 1, 1, 0),                               # smallest input
        ([], 2, 1, -1),                              # nothing links
        ([[1, 2, 0]], 2, 1, 0),                      # zero delay
        ([[2, 1, 4]], 2, 1, -1),                     # wrong direction
        ([[1, 2, 6], [1, 2, 2], [2, 3, 3]], 3, 1, 5),    # parallel links
        ([[1, 2, 1], [1, 3, 1], [1, 4, 1]], 4, 1, 1),    # star: parallel
    ],
)
def test_examples(solve, times, n, k, expected):
    assert solve(times, n, k) == expected


def test_does_not_mutate_input():
    times = [t[:] for t in TIMES_1]
    for solve in SOLVERS:
        solve(times, 5, 3)
    assert times == TIMES_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(743)
    for _ in range(600):
        n = rng.randint(1, 9)
        times = [[rng.randint(1, n), rng.randint(1, n),
                  rng.randint(0, 20)] for _ in range(rng.randint(0, 4 * n))]
        k = rng.randint(1, n)
        g = nx.DiGraph()
        g.add_nodes_from(range(1, n + 1))
        for u, v, w in times:
            if not g.has_edge(u, v) or g[u][v]["weight"] > w:
                g.add_edge(u, v, weight=w)
        lengths = nx.single_source_dijkstra_path_length(g, k)
        expected = max(lengths.values()) if len(lengths) == n else -1
        for solve in SOLVERS:
            assert solve(times, n, k) == expected


def test_large_input_is_fast():
    rng = random.Random(72)
    n = 500
    times = [[i, i + 1, 1000] for i in range(1, n)]
    times += [[rng.randint(1, n), rng.randint(1, n), rng.randint(0, 1000)]
              for _ in range(20_000 - (n - 1))]
    start = time.perf_counter()
    answer = network_delay_time(times, n, 1)
    assert time.perf_counter() - start < 1.0
    assert answer == network_delay_time_brute(times, n, 1)
