import random
import time

import pytest

from solutions.p043_visit_all_nodes import shortest_path_length
from solutions.p043_visit_all_nodes_brute import (
    shortest_path_length_brute,
)

SOLVERS = [shortest_path_length, shortest_path_length_brute]


def from_edges(n, edges):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return graph


EXAMPLE_1 = [[2], [2, 3], [0, 1, 3, 4], [1, 2], [2]]
EXAMPLE_2 = [[1], [0, 2, 3], [1], [1, 4, 5], [3], [3, 6], [5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "graph, expected",
    [
        (EXAMPLE_1, 5),                      # book example 1
        (EXAMPLE_2, 8),                      # book example 2
        ([[]], 0),                           # book example 3
        ([[1], [0]], 1),
        (from_edges(6, [(i, i + 1) for i in range(5)]), 5),
        (from_edges(5, [(0, i) for i in range(1, 5)]), 6),   # star
        (from_edges(6, [(i, (i + 1) % 6) for i in range(6)]), 5),
        (from_edges(4, [(a, b) for a in range(4)
                        for b in range(a + 1, 4)]), 3),     # complete
    ],
)
def test_examples(solve, graph, expected):
    assert solve(graph) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    graph = [nbrs[:] for nbrs in EXAMPLE_2]
    solve(graph)
    assert graph == EXAMPLE_2


def random_connected(rng, n):
    edges = {(rng.randrange(i), i) for i in range(1, n)}   # a tree
    for _ in range(rng.randint(0, n)):
        a, b = rng.sample(range(n), 2) if n > 1 else (0, 0)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    return from_edges(n, sorted(edges))


def test_random_graphs_agree_with_brute_force():
    rng = random.Random(847)
    for _ in range(400):
        graph = random_connected(rng, rng.randint(1, 7))
        assert (shortest_path_length(graph)
                == shortest_path_length_brute(graph))


def test_tree_answer_formula():
    # On a tree every edge is walked twice, except along one path,
    # which is best chosen as a longest path: 2(n-1) - diameter.
    rng = random.Random(12)
    for _ in range(200):
        n = rng.randint(2, 9)
        graph = from_edges(n, [(rng.randrange(i), i)
                               for i in range(1, n)])
        diameter = 0
        for s in range(n):
            dist, frontier = {s: 0}, [s]
            for node in frontier:
                for nxt in graph[node]:
                    if nxt not in dist:
                        dist[nxt] = dist[node] + 1
                        frontier.append(nxt)
            diameter = max(diameter, max(dist.values()))
        assert shortest_path_length(graph) == 2 * (n - 1) - diameter


def test_largest_graphs_are_fast():
    n = 13
    complete = from_edges(n, [(a, b) for a in range(n)
                              for b in range(a + 1, n)])
    star = from_edges(n, [(0, i) for i in range(1, n)])
    start = time.perf_counter()
    assert shortest_path_length(complete) == n - 1
    assert shortest_path_length(star) == 2 * (n - 1) - 2
    assert time.perf_counter() - start < 2.0
