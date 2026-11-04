import random

import pytest

from solutions.p005_find_champion import find_champion
from solutions.p005_find_champion_rows import find_champion_rows

SOLVERS = [find_champion, find_champion_rows]


def tournament(order: list[int]) -> list[list[int]]:
    """Matrix in which order[0] beats everyone, order[1] the rest..."""
    n = len(order)
    rank = {team: i for i, team in enumerate(order)}
    return [[1 if rank[i] < rank[j] else 0 for j in range(n)]
            for i in range(n)]


EXAMPLE_1 = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0],
]
EXAMPLE_2 = [
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
]


def test_book_matrices_are_tournaments():
    assert EXAMPLE_1 == tournament([3, 1, 4, 0, 2])
    assert EXAMPLE_2 == tournament([2, 0, 1, 3])


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 3),                    # book example 1
        (EXAMPLE_2, 2),                    # book example 2
        ([[0]], 0),                        # one team
        ([[0, 0], [1, 0]], 1),
        (tournament([0, 1, 2, 3]), 0),     # champion first
        (tournament([1, 2, 3, 0]), 1),
        (tournament([2, 3, 1, 0]), 2),
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_tournaments():
    rng = random.Random(2923)
    for _ in range(2000):
        order = list(range(rng.randint(1, 10)))
        rng.shuffle(order)
        grid = tournament(order)
        assert find_champion(grid) == order[0]
        assert find_champion_rows(grid) == order[0]


def test_large_tournament_is_fast():
    rng = random.Random(4)
    order = list(range(1000))
    rng.shuffle(order)
    grid = tournament(order)
    assert find_champion(grid) == order[0]
    assert find_champion_rows(grid) == order[0]
