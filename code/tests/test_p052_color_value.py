import random
import time

import pytest

from solutions.p052_color_value import largest_path_value
from solutions.p052_color_value_alt import (
    largest_path_value_by_color,
)
from solutions.p052_color_value_brute import (
    largest_path_value_brute,
)

SOLVERS = [largest_path_value, largest_path_value_by_color,
           largest_path_value_brute]

EXAMPLE_1 = ("aabcbb", [[0, 1], [1, 3], [2, 3], [3, 4], [4, 5]])
EIGHT_NODES = ("baaabcbb", [[0, 1], [1, 2], [2, 3], [3, 5], [0, 4],
                            [1, 4], [4, 5], [5, 6], [6, 7]])
EXAMPLE_2 = ("xyzyx", [[0, 1], [1, 2], [2, 3], [3, 1], [3, 4]])
EXAMPLE_3 = ("kkkk", [[0, 1], [0, 2], [1, 3], [2, 3]])


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "colors, edges, expected",
    [
        (*EXAMPLE_1, 3),                     # book example 1
        (*EIGHT_NODES, 4),
        (*EXAMPLE_2, -1),                    # book example 2 (cycle)
        (*EXAMPLE_3, 3),                     # diamond (not in book)
        ("m", [], 1),                        # one node
        ("mn", [[0, 1], [1, 1]], -1),        # a self-loop is a cycle
        ("abc", [], 1),                      # no edges at all
        ("aba", [[0, 1], [1, 2]], 2),
        ("aa", [[0, 1], [1, 0]], -1),
        # a cycle far away from the best path still means -1
        ("aaaab", [[0, 1], [1, 2], [3, 4], [4, 3]], -1),
        # parallel edges are allowed
        ("zz", [[0, 1], [0, 1]], 2),
    ],
)
def test_examples(solve, colors, edges, expected):
    assert solve(colors, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    colors, edges = EXAMPLE_1
    copy = [e[:] for e in edges]
    solve(colors, edges)
    assert edges == copy


def single_best_path(colors, edges):
    """The tempting wrong shortcut: keep one tally per node."""
    n = len(colors)
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    tally = [[0] * 26 for _ in range(n)]
    order = [v for v in range(n) if indegree[v] == 0]
    for node in order:
        tally[node][ord(colors[node]) - 97] += 1
        for nxt in graph[node]:
            if max(tally[node]) > max(tally[nxt]):
                tally[nxt] = tally[node][:]
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                order.append(nxt)
    return max(max(row) for row in tally)


def test_one_tally_per_node_is_wrong_on_example_1():
    assert single_best_path(*EXAMPLE_1) == 2


def random_graph(rng: random.Random, n: int, acyclic: bool):
    colors = "".join(rng.choice("abc") for _ in range(n))
    edges = []
    for _ in range(rng.randint(0, 2 * n)):
        u, v = rng.randrange(n), rng.randrange(n)
        if acyclic and u >= v:
            continue
        edges.append([u, v])
    return colors, edges


def test_random_graphs_agree():
    rng = random.Random(1857)
    for _ in range(1500):
        n = rng.randint(1, 8)
        colors, edges = random_graph(rng, n, rng.random() < 0.7)
        expected = largest_path_value_brute(colors, edges)
        assert largest_path_value(colors, edges) == expected
        assert largest_path_value_by_color(colors, edges) == expected


def test_large_graph_is_fast():
    rng = random.Random(5)
    n, m = 50_000, 100_000
    colors = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz")
                     for _ in range(n))
    edges = []
    while len(edges) < m:
        u, v = rng.randrange(n), rng.randrange(n)
        if u < v:
            edges.append([u, v])
    start = time.perf_counter()
    expected = largest_path_value(colors, edges)
    assert largest_path_value_by_color(colors, edges) == expected
    assert time.perf_counter() - start < 4.0
    # one back edge closes a cycle
    edges.append([n - 1, 0])
    edges.append([0, n - 1])
    assert largest_path_value(colors, edges) == -1


def test_long_chain_is_fast():
    n = 50_000
    colors = "ab" * (n // 2)
    edges = [[i, i + 1] for i in range(n - 1)]
    assert largest_path_value(colors, edges) == n // 2
