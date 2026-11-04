import random
import time

import networkx as nx
import pytest

from solutions.p090_closest_node import closest_meeting_node
from solutions.p090_closest_node_brute import (
    closest_meeting_node_brute,
)

SOLVERS = [closest_meeting_node, closest_meeting_node_brute]

EXAMPLE_1 = [3, 6, 5, 2, 3, 6, 2, 1, 7]
EXAMPLE_2 = [1, -1, 3, 2, 3]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, node1, node2, expected",
    [
        (EXAMPLE_1, 0, 8, 2),               # book example 1 (tie 2 vs 6)
        (EXAMPLE_2, 0, 4, -1),              # book example 2
        (EXAMPLE_1, 4, 4, 4),               # same start: distance 0
        ([-1], 0, 0, 0),                    # smallest input
        ([-1, -1], 0, 1, -1),
        ([1, -1], 0, 1, 1),                 # 0 reaches 1 directly
        ([1, 0], 0, 1, 0),                  # 2-cycle: tie, smaller id
        ([0, 0], 1, 1, 1),                  # self-loop allowed
        ([1, 2, 0], 0, 1, 1),               # 3-cycle
        ([1, 2, 3, -1], 0, 3, 3),           # chain ends at node2
    ],
)
def test_examples(solve, edges, node1, node2, expected):
    assert solve(edges, node1, node2) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = EXAMPLE_1[:]
    solve(edges, 0, 8)
    assert edges == EXAMPLE_1


def networkx_answer(edges, node1, node2):
    g = nx.DiGraph()
    g.add_nodes_from(range(len(edges)))
    g.add_edges_from((u, v) for u, v in enumerate(edges) if v != -1)
    d1 = nx.single_source_shortest_path_length(g, node1)
    d2 = nx.single_source_shortest_path_length(g, node2)
    common = [(max(d1[v], d2[v]), v) for v in d1 if v in d2]
    return min(common)[1] if common else -1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(2359)
    for _ in range(2000):
        n = rng.randint(1, 12)
        edges = [rng.choice([-1] + list(range(n))) for _ in range(n)]
        node1, node2 = rng.randrange(n), rng.randrange(n)
        expected = networkx_answer(edges, node1, node2)
        for solve in SOLVERS:
            assert solve(edges, node1, node2) == expected, edges


def test_large_graph_is_fast():
    n = 3 * 10**5
    edges = list(range(1, n)) + [n // 2]      # long tail, big cycle
    start = time.perf_counter()
    # node1 = 0 enters the cycle at n // 2; node2 = n - 1 is on it.
    assert closest_meeting_node(edges, 0, n - 1) == n // 2
    assert time.perf_counter() - start < 5.0
