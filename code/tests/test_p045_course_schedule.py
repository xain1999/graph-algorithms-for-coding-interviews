import random
import time

import networkx as nx
import pytest

from solutions.p045_course_schedule import can_finish
from solutions.p045_course_schedule_brute import can_finish_brute
from solutions.p045_course_schedule_dfs import can_finish_dfs

SOLVERS = [can_finish, can_finish_dfs, can_finish_brute]

EXAMPLE_1 = [[2, 0], [2, 1], [3, 2], [5, 1], [4, 3], [4, 5], [6, 4]]
EXAMPLE_2 = EXAMPLE_1 + [[2, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, prereqs, expected",
    [
        (7, EXAMPLE_1, True),           # book example 1
        (7, EXAMPLE_2, False),          # book example 2 (cycle 2-3-4)
        (4, [[3, 1]], True),            # free courses (not in book)
        (1, [], True),                  # smallest input
        (3, [[0, 2], [2, 0]], False),   # two-course cycle
        (3, [[0, 2]], True),
        (3, [[1, 0], [2, 1]], True),    # a chain
        (3, [[1, 0], [1, 0], [2, 1]], True),    # repeated pair
        (3, [[0, 1], [1, 2], [2, 0]], False),
        # a cycle in one piece, a fine chain in another
        (6, [[1, 0], [2, 1], [4, 3], [5, 4], [3, 5]], False),
    ],
)
def test_examples(solve, n, prereqs, expected):
    assert solve(n, prereqs) is expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    prereqs = [p[:] for p in EXAMPLE_2]
    solve(7, prereqs)
    assert prereqs == EXAMPLE_2


def random_case(rng: random.Random):
    n = rng.randint(1, 9)
    pairs = {(rng.randrange(n), rng.randrange(n))
             for _ in range(rng.randint(0, 2 * n))}
    return n, [[a, b] for a, b in pairs if a != b]


def test_random_graphs_agree_with_networkx():
    rng = random.Random(207)
    for _ in range(2000):
        n, prereqs = random_case(rng)
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from((b, a) for a, b in prereqs)
        expected = nx.is_directed_acyclic_graph(g)
        for solve in SOLVERS[:2]:
            assert solve(n, prereqs) is expected
        assert can_finish_brute(n, prereqs) is expected


def test_large_inputs_are_fast():
    n = 100_000
    chain = [[i + 1, i] for i in range(n - 1)]      # deep: 0 -> ... n-1
    rng = random.Random(3)
    extra = []
    for _ in range(100_000):
        a, b = sorted(rng.sample(range(n), 2))
        extra.append([b, a])                        # still acyclic
    start = time.perf_counter()
    for solve in SOLVERS[:2]:
        assert solve(n, chain + extra) is True
        assert solve(n, chain + [[0, n - 1]]) is False   # closes it
    assert time.perf_counter() - start < 4.0
