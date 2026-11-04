import random
import time

import pytest

from solutions.p070_max_groups import bfs_layers, max_groups
from solutions.p070_max_groups_brute import max_groups_brute

SOLVERS = [max_groups, max_groups_brute]

EXAMPLE_1 = [[1, 2], [2, 3], [3, 4], [4, 1], [3, 5], [5, 6], [2, 7],
             [8, 9]]
EXAMPLE_2 = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1], [5, 6]]


@pytest.mark.parametrize("solve", [max_groups])
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (9, EXAMPLE_1, 7),        # book example 1: 5 + 2 groups
        (6, EXAMPLE_2, -1),       # book example 2: a 5-cycle
        (5, [[2, 4]], 5),         # isolated nodes: 1 + 2 + 1 + 1
    ],
)
def test_book_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (1, [], 1),                               # smallest input
        (3, [], 3),                               # no edges at all
        (4, [[1, 2], [2, 3], [3, 1], [3, 4]], -1),  # triangle
        (4, [[1, 2], [2, 3], [3, 4]], 4),         # a path
        (4, [[1, 2], [2, 3], [3, 4], [4, 1]], 3),  # a square
        (5, [[1, 2], [1, 3], [1, 4], [1, 5]], 3),  # a star
        (6, [[1, 2], [2, 3], [4, 5], [5, 6], [6, 4]], -1),
        (5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 2]], 5),  # repeat
        (3, [[1, 2], [2, 2]], -1),                # self-loop
    ],
)
def test_small_cases(solve, n, edges, expected):
    assert solve(n, edges) == expected


def test_layers_from_each_start():
    graph = [[] for _ in range(10)]
    for a, b in EXAMPLE_1:
        graph[a].append(b)
        graph[b].append(a)
    layers = [bfs_layers(graph, s) for s in range(1, 8)]
    assert layers == [5, 4, 3, 4, 4, 5, 5]


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_2]
    solve(6, edges)
    assert edges == EXAMPLE_2


def test_random_agree_with_brute_force():
    rng = random.Random(2493)
    for _ in range(400):
        n = rng.randint(1, 6)
        pairs = [[a, b] for a in range(1, n + 1)
                 for b in range(a + 1, n + 1)]
        edges = rng.sample(pairs, rng.randint(0, len(pairs)))
        assert max_groups(n, edges) == max_groups_brute(n, edges)


def test_large_input_is_fast():
    rng = random.Random(70)
    n = 400
    # odd-even edges keep the graph bipartite, so every BFS runs
    edges = []
    while len(edges) < 8000:
        a, b = rng.randrange(1, n + 1, 2), rng.randrange(2, n + 1, 2)
        edges.append([a, b])
    start = time.perf_counter()
    assert max_groups(n, edges) >= 1
    path = [[i, i + 1] for i in range(1, n)]
    assert max_groups(n, path) == n
    assert time.perf_counter() - start < 3.0


def test_two_pass_shortcut_can_fail():
    # Square 1-2-5-3 plus node 4 on node 2 (the pitfall in the book).
    n, edges = 5, [[1, 2], [1, 3], [2, 4], [2, 5], [3, 5]]
    assert max_groups(n, edges) == 4
    graph = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def layers_from(s: int) -> dict[int, int]:
        dist, frontier = {s: 0}, [s]
        while frontier:
            nxt = []
            for u in frontier:
                for v in graph[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        nxt.append(v)
            frontier = nxt
        return dist

    first = layers_from(1)
    assert first[5] == first[4] == 2           # 5 is a farthest node
    assert max(layers_from(5).values()) + 1 == 3
