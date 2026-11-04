import itertools
import random
import time

import networkx as nx
import pytest

from solutions.p044_build_order import is_valid_order
from solutions.p044_build_order_brute import is_valid_order_brute

SOLVERS = [is_valid_order, is_valid_order_brute]

DEPS = [[0, 2], [1, 2], [1, 3], [2, 4], [3, 4], [4, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, deps, order, expected",
    [
        (6, DEPS, [1, 0, 3, 2, 4, 5], True),     # book example 1
        (6, DEPS, [0, 1, 2, 4, 3, 5], False),    # book example 2
        (4, [], [3, 1, 3, 0], False),            # book pitfall: repeat
        (1, [], [0], True),                      # smallest input
        (1, [], [], False),                      # task missing
        (2, [], [1, 0], True),                   # no rules: any order
        (2, [[0, 1]], [1, 0], False),            # single broken rule
        (3, [[0, 1]], [0, 1], False),            # task 2 missing
        (3, [[0, 1]], [2, 0, 1, 2], False),      # too long
        (3, [[0, 1], [1, 0]], [0, 1, 2], False),  # a cycle: never
        (5, [[0, 1], [0, 1]], [0, 2, 1, 4, 3], True),  # repeated pair
    ],
)
def test_examples(solve, n, deps, order, expected):
    assert solve(n, deps, order) is expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    deps = [d[:] for d in DEPS]
    order = [1, 0, 3, 2, 4, 5]
    solve(6, deps, order)
    assert deps == DEPS and order == [1, 0, 3, 2, 4, 5]


def test_every_permutation_against_networkx():
    # The valid orders are exactly networkx's topological sorts.
    rng = random.Random(44)
    for _ in range(300):
        n = rng.randint(1, 6)
        deps = [[a, b] for a in range(n) for b in range(n)
                if a != b and rng.random() < 0.25]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(deps)
        if nx.is_directed_acyclic_graph(g):
            valid = {tuple(o) for o in nx.all_topological_sorts(g)}
        else:
            valid = set()
        for perm in itertools.permutations(range(n)):
            expected = perm in valid
            for solve in SOLVERS:
                assert solve(n, deps, list(perm)) is expected


def test_random_lists_agree_with_brute_force():
    rng = random.Random(4400)
    for _ in range(2000):
        n = rng.randint(1, 7)
        deps = [[rng.randrange(n), rng.randrange(n)]
                for _ in range(rng.randint(0, 8))]
        deps = [d for d in deps if d[0] != d[1]]
        order = [rng.randrange(n) for _ in range(rng.randint(0, n + 1))]
        if rng.random() < 0.5:
            order = rng.sample(range(n), n)
        assert is_valid_order(n, deps, order) == \
            is_valid_order_brute(n, deps, order)


def test_large_input_is_fast():
    n = 100_000
    order = list(range(n))
    random.Random(1).shuffle(order)
    deps = [[order[i], order[i + 1]] for i in range(n - 1)]
    deps += [[order[i], order[-1]] for i in range(0, n - 1, 1000)]
    start = time.perf_counter()
    assert is_valid_order(n, deps, order)
    order[0], order[-1] = order[-1], order[0]
    assert not is_valid_order(n, deps, order)
    assert time.perf_counter() - start < 2.0
