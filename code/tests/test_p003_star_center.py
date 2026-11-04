import random

import pytest

from solutions.p003_star_center import find_center
from solutions.p003_star_center_alt import find_center_by_degree

SOLVERS = [find_center, find_center_by_degree]

EXAMPLE_1 = [[3, 5], [5, 1], [4, 5], [5, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, expected",
    [
        (EXAMPLE_1, 5),                              # book example 1
        ([[2, 1], [1, 3]], 1),                       # smallest star
        ([[6, 4], [1, 6], [6, 2], [3, 6], [5, 6]], 6),  # book example 2
        ([[1, 2], [3, 1]], 1),                       # center in 1st slot
        ([[1, 2], [2, 3]], 2),                       # center in 2nd slot
        ([[2, 1], [3, 2]], 2),
    ],
)
def test_examples(solve, edges, expected):
    assert solve(edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(edges)
    assert edges == EXAMPLE_1


def random_star(rng: random.Random, n: int) -> tuple[list, int]:
    center = rng.randint(1, n)
    edges = [[center, v] if rng.random() < 0.5 else [v, center]
             for v in range(1, n + 1) if v != center]
    rng.shuffle(edges)
    return edges, center


def test_random_stars():
    rng = random.Random(1791)
    for _ in range(3000):
        edges, center = random_star(rng, rng.randint(3, 12))
        for solve in SOLVERS:
            assert solve(edges) == center


def test_degree_version_rejects_non_star():
    with pytest.raises(ValueError):
        find_center_by_degree([[1, 2], [2, 3], [3, 4]])


def test_large_star_is_fast():
    edges, center = random_star(random.Random(5), 100_000)
    assert find_center(edges) == center
    assert find_center_by_degree(edges) == center
