import heapq
import random
import time

import networkx as nx
import pytest

from solutions.p077_ways_to_arrive import MOD, count_paths
from solutions.p077_ways_to_arrive_alt import count_paths_dag
from solutions.p077_ways_to_arrive_brute import count_paths_brute

SOLVERS = [count_paths, count_paths_dag, count_paths_brute]

ROADS_1 = [[0, 1, 2], [0, 2, 3], [1, 3, 3], [2, 3, 2], [1, 2, 1],
           [3, 5, 4], [2, 4, 4], [4, 5, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, roads, expected",
    [
        (6, ROADS_1, 5),                         # book example 1
        (3, [[0, 1, 4], [1, 2, 4], [0, 2, 8]], 2),   # book example 2
        (1, [], 1),                              # start is the goal
        (2, [[1, 0, 6]], 1),
        (4, [[0, 1, 1], [1, 3, 1], [0, 2, 1], [2, 3, 2]], 1),
        (4, [[0, 3, 10], [0, 1, 3], [1, 2, 3], [2, 3, 4]], 2),
    ],
)
def test_examples(solve, n, roads, expected):
    assert solve(n, roads) == expected


def count_without_stale_check(n, roads):
    """The bug from the text: no stale check, nd from dist[node]."""
    graph = [[] for _ in range(n)]
    for u, v, t in roads:
        graph[u].append((v, t))
        graph[v].append((u, t))
    dist, ways = [float("inf")] * n, [0] * n
    dist[0], ways[0] = 0, 1
    heap = [(0, 0)]
    while heap:
        _, node = heapq.heappop(heap)
        for nxt, t in graph[node]:
            nd = dist[node] + t
            if nd < dist[nxt]:
                dist[nxt], ways[nxt] = nd, ways[node]
                heapq.heappush(heap, (nd, nxt))
            elif nd == dist[nxt]:
                ways[nxt] += ways[node]
    return ways[n - 1]


def test_stale_entries_must_be_skipped():
    # Node 1 is pushed at time 9, then improved to 2 via node 2.
    roads = [[0, 1, 9], [0, 2, 1], [2, 1, 1], [1, 3, 1]]
    assert count_without_stale_check(4, roads) == 2     # wrong
    assert count_paths(4, roads) == 1


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    roads = [r[:] for r in ROADS_1]
    solve(6, roads)
    assert roads == ROADS_1


def diamonds(m):
    """m diamonds in a row: 2**m fastest routes."""
    roads = []
    for i in range(m):
        a = 3 * i
        roads += [[a, a + 1, 1], [a, a + 2, 1],
                  [a + 1, a + 3, 1], [a + 2, a + 3, 1]]
    return 3 * m + 1, roads


def test_count_is_reduced_modulo():
    n, roads = diamonds(100)
    assert count_paths(n, roads) == pow(2, 100, MOD)
    assert count_paths_dag(n, roads) == pow(2, 100, MOD)


def random_connected(rng):
    n = rng.randint(2, 8)
    pairs = {(rng.randrange(i), i) for i in range(1, n)}  # a tree
    for _ in range(rng.randint(0, 10)):
        a, b = sorted(rng.sample(range(n), 2))
        pairs.add((a, b))
    return n, [[a, b, rng.randint(1, 4)] for a, b in pairs]


def test_random_agree_with_networkx():
    rng = random.Random(1976)
    for _ in range(800):
        n, roads = random_connected(rng)
        g = nx.Graph()
        g.add_weighted_edges_from(roads)
        expected = sum(1 for _ in nx.all_shortest_paths(
            g, 0, n - 1, weight="weight"))
        for solve in SOLVERS:
            assert solve(n, roads) == expected


def test_large_input_is_fast():
    rng = random.Random(3)
    n = 500
    pairs = {(rng.randrange(i), i) for i in range(1, n)}
    while len(pairs) < 10_000:
        a, b = sorted(rng.sample(range(n), 2))
        pairs.add((a, b))
    roads = [[a, b, rng.randint(1, 3)] for a, b in pairs]
    start = time.perf_counter()
    ans = count_paths(n, roads)
    assert time.perf_counter() - start < 1.0
    assert ans == count_paths_dag(n, roads)
