import random
import time

import pytest

from solutions.p075_cheapest_flights import find_cheapest_price
from solutions.p075_cheapest_flights_alt import (
    find_cheapest_price_dijkstra,
)
from solutions.p075_cheapest_flights_brute import (
    find_cheapest_price_brute,
)

SOLVERS = [find_cheapest_price, find_cheapest_price_dijkstra,
           find_cheapest_price_brute]

FLIGHTS_1 = [[0, 1, 50], [1, 2, 40], [2, 4, 30], [0, 3, 100],
             [3, 4, 60], [0, 2, 120], [1, 4, 150]]
TRAP = [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 9]]
HOP = [[0, 1, 5], [1, 2, 5], [0, 2, 20]]   # review cases R04-R05


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, flights, src, dst, k, expected",
    [
        (5, FLIGHTS_1, 0, 4, 1, 150),       # book example 1
        (5, FLIGHTS_1, 0, 4, 2, 120),       # book example 2
        (3, [[1, 2, 4]], 0, 2, 2, -1),      # nothing leaves src
        (4, TRAP, 0, 3, 0, 9),              # the copy trap
        (4, TRAP, 0, 3, 2, 3),
        (5, FLIGHTS_1, 0, 4, 0, -1),        # no direct flight
        (5, FLIGHTS_1, 4, 0, 4, -1),        # flights are one-way
        (2, [[0, 1, 9], [0, 1, 4]], 0, 1, 0, 4),   # parallel flights
        (3, [[0, 1, 2], [1, 0, 1], [1, 2, 3]], 0, 2, 2, 5),  # cycle
        (3, HOP, 0, 2, 0, 20),              # R04: k = 0, one round
        (3, HOP, 0, 2, 1, 10),              # R05: k = 1, two rounds
    ],
)
def test_examples(solve, n, flights, src, dst, k, expected):
    assert solve(n, flights, src, dst, k) == expected


def in_place_relax(n, flights, src, dst, k):
    """The buggy version without the copy, kept to document it."""
    cost = [float("inf")] * n
    cost[src] = 0
    for _ in range(k + 1):
        for a, b, price in flights:
            if cost[a] + price < cost[b]:
                cost[b] = cost[a] + price
    return -1 if cost[dst] == float("inf") else cost[dst]


def test_without_copy_the_stop_limit_leaks():
    assert in_place_relax(4, TRAP, 0, 3, 0) == 3       # wrong
    assert find_cheapest_price(4, TRAP, 0, 3, 0) == 9  # right


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    flights = [f[:] for f in FLIGHTS_1]
    solve(5, flights, 0, 4, 2)
    assert flights == FLIGHTS_1


def test_random_agree():
    rng = random.Random(787)
    for _ in range(1500):
        n = rng.randint(2, 6)
        flights = []
        for _ in range(rng.randint(0, 12)):
            a, b = rng.sample(range(n), 2)
            flights.append([a, b, rng.randint(1, 20)])
        src, dst = rng.sample(range(n), 2)
        k = rng.randint(0, n - 1)
        expected = find_cheapest_price_brute(n, flights, src, dst, k)
        ans = find_cheapest_price(n, flights, src, dst, k)
        assert ans == expected
        assert find_cheapest_price_dijkstra(
            n, flights, src, dst, k) == expected


def test_large_input_is_fast():
    rng = random.Random(5)
    n = 150
    flights = [[a, b, rng.randint(1, 5000)]
               for a, b in (rng.sample(range(n), 2)
                            for _ in range(6000))]
    start = time.perf_counter()
    ans = find_cheapest_price(n, flights, 0, n - 1, n - 1)
    assert time.perf_counter() - start < 2.0
    assert ans == find_cheapest_price_dijkstra(n, flights, 0, n - 1,
                                               n - 1)
