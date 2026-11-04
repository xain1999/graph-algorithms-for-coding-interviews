import random

import pytest

from solutions.p004_destination_city import dest_city
from solutions.p004_destination_city_brute import dest_city_brute

SOLVERS = [dest_city, dest_city_brute]

EXAMPLE_1 = [["Oslo", "Lyon"], ["Kyiv", "Oslo"],
             ["Lyon", "Cairo"], ["Cairo", "Quito"]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "paths, expected",
    [
        (EXAMPLE_1, "Quito"),                       # book example 1
        ([["Tunis", "Seoul"]], "Seoul"),            # single trip
        ([["Lima", "Rome"], ["Pune", "Lima"]], "Rome"),  # book ex. 2
        ([["x", "y"], ["y", "z"]], "z"),            # already in order
        ([["Lyon", "lyon"]], "lyon"),               # case matters
    ],
)
def test_examples(solve, paths, expected):
    assert solve(paths) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    paths = [p[:] for p in EXAMPLE_1]
    solve(paths)
    assert paths == EXAMPLE_1


@pytest.mark.parametrize("solve", SOLVERS)
def test_cycle_is_rejected(solve):
    with pytest.raises(ValueError):
        solve([["a", "b"], ["b", "a"]])


def random_route(rng: random.Random, m: int) -> tuple[list, str]:
    cities = rng.sample([f"C{i}" for i in range(4 * m)], m + 1)
    paths = [[cities[i], cities[i + 1]] for i in range(m)]
    rng.shuffle(paths)
    return paths, cities[-1]


def test_random_routes():
    rng = random.Random(1436)
    for _ in range(2000):
        paths, last = random_route(rng, rng.randint(1, 12))
        assert dest_city(paths) == last
        assert dest_city_brute(paths) == last


def test_long_route_is_fast():
    paths, last = random_route(random.Random(3), 100_000)
    assert dest_city(paths) == last
