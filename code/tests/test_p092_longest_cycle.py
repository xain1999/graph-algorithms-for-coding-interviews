import random
import time

import networkx as nx
import pytest

from solutions.p092_longest_cycle import longest_cycle
from solutions.p092_longest_cycle_brute import longest_cycle_brute
from solutions.p092_longest_cycle_kahn import longest_cycle_kahn

SOLVERS = [longest_cycle, longest_cycle_brute, longest_cycle_kahn]

EXAMPLE_1 = [4, 7, 0, 9, 8, 3, 1, 2, 2, 5]
EXAMPLE_2 = [2, 2, -1, 4, 2]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, expected",
    [
        (EXAMPLE_1, 4),                     # book example 1
        (EXAMPLE_2, -1),                    # book example 2
        ([-1], -1),                         # smallest input
        ([0], 1),                           # a self-loop is a cycle
        ([1, 0], 2),
        ([1, 2, 0, 0], 3),                  # tail 3 -> 0 into a cycle
        ([1, 1, 1], 1),                     # self-loop with tails
        ([1, 2, 3, 4, 0, 6, 5], 5),         # two cycles: 5 and 2
    ],
)
def test_examples(solve, edges, expected):
    assert solve(edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = EXAMPLE_1[:]
    solve(edges)
    assert edges == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(2360)
    for _ in range(2000):
        n = rng.randint(1, 12)
        edges = [rng.choice([-1] + list(range(n))) for _ in range(n)]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from((u, v) for u, v in enumerate(edges) if v != -1)
        cycles = [len(c) for c in nx.simple_cycles(g)]
        expected = max(cycles, default=-1)
        for solve in SOLVERS:
            assert solve(edges) == expected, edges


@pytest.mark.parametrize("solve", [longest_cycle, longest_cycle_kahn])
def test_large_graphs_are_fast(solve):
    n = 2 * 10**5
    one_cycle = list(range(1, n)) + [0]
    tail = list(range(1, n)) + [n // 2]         # long tail, then cycle
    rng = random.Random(9)
    random_graph = [rng.randrange(n) for _ in range(n)]
    start = time.perf_counter()
    assert solve(one_cycle) == n
    assert solve(tail) == n - n // 2
    assert solve(random_graph) == longest_cycle(random_graph)
    assert time.perf_counter() - start < 5.0
