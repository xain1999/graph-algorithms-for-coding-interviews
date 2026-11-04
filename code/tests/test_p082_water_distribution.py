import random
import time

import pytest

from solutions.p082_water_distribution import min_cost_to_supply_water
from solutions.p082_water_distribution_alt import (
    min_cost_to_supply_water_prim,
)
from solutions.p082_water_distribution_brute import (
    min_cost_to_supply_water_brute,
)

SOLVERS = [min_cost_to_supply_water, min_cost_to_supply_water_prim,
           min_cost_to_supply_water_brute]

WELLS_1 = [5, 3, 10, 8, 7]
PIPES_1 = [[1, 2, 2], [2, 3, 4], [1, 3, 6], [4, 5, 1], [3, 4, 9]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, wells, pipes, expected",
    [
        (5, WELLS_1, PIPES_1, 17),                  # book example 1
        (3, [5, 1, 6], [[1, 2, 3], [2, 3, 8], [2, 3, 4]], 8),  # ex. 2
        (2, [3, 4], [], 7),                         # book example 3
        (1, [9], [], 9),                            # smallest input
        (2, [1, 1], [[1, 2, 5]], 2),                # wells beat pipe
        (3, [10, 10, 10], [[1, 2, 1], [2, 3, 1]], 12),  # one well
        (3, [0, 0, 0], [[1, 2, 1]], 0),             # free wells
        (4, [4, 9, 9, 9], [[1, 2, 0], [2, 3, 0], [3, 4, 0]], 4),
    ],
)
def test_examples(solve, n, wells, pipes, expected):
    assert solve(n, wells, pipes) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    wells, pipes = WELLS_1[:], [p[:] for p in PIPES_1]
    solve(5, wells, pipes)
    assert wells == WELLS_1 and pipes == PIPES_1


def random_case(rng, n_max, m_max):
    n = rng.randint(1, n_max)
    wells = [rng.randint(0, 9) for _ in range(n)]
    pipes = []
    if n > 1:
        for _ in range(rng.randint(0, m_max)):
            a, b = rng.sample(range(1, n + 1), 2)
            pipes.append([a, b, rng.randint(0, 9)])
    return n, wells, pipes


def test_random_agree_with_brute_force():
    rng = random.Random(1168)
    for _ in range(400):
        n, wells, pipes = random_case(rng, 5, 6)
        expected = min_cost_to_supply_water_brute(n, wells, pipes)
        assert min_cost_to_supply_water(n, wells, pipes) == expected
        assert min_cost_to_supply_water_prim(n, wells, pipes) == expected


def test_random_kruskal_agrees_with_prim():
    rng = random.Random(82)
    for _ in range(300):
        n, wells, pipes = random_case(rng, 30, 60)
        assert (min_cost_to_supply_water(n, wells, pipes)
                == min_cost_to_supply_water_prim(n, wells, pipes))


def test_large_input_is_fast():
    rng = random.Random(7)
    n, m = 20_000, 30_000
    wells = [rng.randint(0, 10**6) for _ in range(n)]
    pipes = []
    for _ in range(m):
        a, b = rng.sample(range(1, n + 1), 2)
        pipes.append([a, b, rng.randint(0, 10**6)])
    start = time.perf_counter()
    got = min_cost_to_supply_water(n, wells, pipes)
    assert time.perf_counter() - start < 2.0
    assert got == min_cost_to_supply_water_prim(n, wells, pipes)
