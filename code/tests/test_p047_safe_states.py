import random
import time

import networkx as nx
import pytest

from solutions.p047_safe_states import eventual_safe_nodes
from solutions.p047_safe_states_brute import eventual_safe_nodes_brute
from solutions.p047_safe_states_kahn import eventual_safe_nodes_kahn

SOLVERS = [eventual_safe_nodes, eventual_safe_nodes_kahn,
           eventual_safe_nodes_brute]

EXAMPLE_1 = [[1, 4], [2], [3], [6, 1], [5, 6], [], [5], [6, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "graph, expected",
    [
        (EXAMPLE_1, [4, 5, 6]),          # book example 1
        ([[1], [1, 2], []], [2]),           # book example 2 (self-loop)
        ([[2], [2, 3], [3], []], [0, 1, 2, 3]),  # a DAG (not in book)
        ([[]], [0]),                        # smallest input
        ([[0]], []),                        # lone self-loop
        ([[1], [2], [0]], []),              # everything on a cycle
        ([[1], [0], [3], []], [2, 3]),      # two pieces
        ([[1, 2], [], [0]], [1]),           # 1 is safe, 0 and 2 loop
    ],
)
def test_examples(solve, graph, expected):
    assert solve(graph) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    graph = [row[:] for row in EXAMPLE_1]
    solve(graph)
    assert graph == EXAMPLE_1


def safe_by_networkx(graph: list[list[int]]) -> list[int]:
    g = nx.DiGraph()
    g.add_nodes_from(range(len(graph)))
    g.add_edges_from((u, v) for u, row in enumerate(graph) for v in row)
    bad = set()
    for comp in nx.strongly_connected_components(g):
        v = next(iter(comp))
        if len(comp) > 1 or g.has_edge(v, v):
            bad |= comp
    return [v for v in range(len(graph))
            if v not in bad and not (nx.descendants(g, v) & bad)]


def test_random_graphs_agree_with_networkx():
    rng = random.Random(802)
    for _ in range(2000):
        n = rng.randint(1, 9)
        p = rng.choice((0.1, 0.2, 0.35))
        graph = [sorted(v for v in range(n) if rng.random() < p)
                 for _ in range(n)]
        expected = safe_by_networkx(graph)
        for solve in SOLVERS:
            assert solve(graph) == expected


def test_large_inputs_are_fast():
    n = 100_000
    chain = [[i + 1] for i in range(n - 1)] + [[]]   # deep DAG
    looped = [[i + 1] for i in range(n - 1)] + [[n // 2]]
    start = time.perf_counter()
    for solve in SOLVERS[:2]:
        assert solve(chain) == list(range(n))
        assert solve(looped) == []
    rng = random.Random(9)
    graph = [[rng.randrange(n) for _ in range(3)] for _ in range(n)]
    graph = [sorted(set(row)) for row in graph]
    assert eventual_safe_nodes(graph) == eventual_safe_nodes_kahn(graph)
    assert time.perf_counter() - start < 4.0
