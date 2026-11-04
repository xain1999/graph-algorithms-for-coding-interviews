import random
import time

import pytest

from solutions.p069_flower_planting import plant_flowers
from solutions.p069_flower_planting_brute import plant_flowers_brute

EXAMPLE_1 = [[1, 2], [1, 3], [1, 4], [2, 3], [3, 4], [2, 5]]
EXAMPLE_2 = [[2, 4], [2, 5], [2, 6], [4, 5], [4, 6], [5, 6], [1, 3]]
K4 = [[2, 3], [2, 4], [2, 5], [3, 4], [3, 5], [4, 5]]  # 1 alone


def is_valid(n, paths, flower, kinds=4):
    return (len(flower) == n
            and all(1 <= f <= kinds for f in flower)
            and all(flower[x - 1] != flower[y - 1] for x, y in paths))


def random_paths(rng, n, max_degree=3):
    """Random gardens where no garden has more than 3 paths."""
    degree = [0] * (n + 1)
    pairs = [(x, y) for x in range(1, n + 1)
             for y in range(x + 1, n + 1)]
    rng.shuffle(pairs)
    paths = []
    for x, y in pairs:
        if degree[x] < max_degree and degree[y] < max_degree:
            if rng.random() < 0.6:
                paths.append([x, y] if rng.random() < 0.5 else [y, x])
                degree[x] += 1
                degree[y] += 1
    return paths


def test_book_outputs():
    assert plant_flowers(5, EXAMPLE_1) == [1, 2, 3, 2, 1]
    assert plant_flowers(6, EXAMPLE_2) == [1, 1, 2, 2, 3, 4]
    assert plant_flowers(3, []) == [1, 1, 1]


@pytest.mark.parametrize("solve", [plant_flowers, plant_flowers_brute])
@pytest.mark.parametrize(
    "n, paths",
    [
        (5, EXAMPLE_1), (6, EXAMPLE_2), (3, []),    # examples, no paths
        (1, []),                                    # smallest input
        (5, K4),                                    # needs all four
        (2, [[2, 1]]),
        (8, [[1, 2], [2, 3], [3, 4], [4, 1], [5, 6], [6, 7], [7, 5]]),
    ],
)
def test_examples(solve, n, paths):
    assert is_valid(n, paths, solve(n, paths))


def test_does_not_mutate_input():
    paths = [p[:] for p in EXAMPLE_1]
    plant_flowers(5, paths)
    assert paths == EXAMPLE_1


def test_three_kinds_are_not_always_enough():
    assert plant_flowers_brute(5, K4, kinds=3) == []
    assert plant_flowers_brute(5, K4, kinds=4) == [1, 1, 2, 3, 4]
    assert plant_flowers_brute(6, EXAMPLE_2, kinds=3) == []


def test_random_gardens_are_valid():
    rng = random.Random(1042)
    for _ in range(1500):
        n = rng.randint(1, 12)
        paths = random_paths(rng, n)
        assert is_valid(n, paths, plant_flowers(n, paths)), paths
        if n <= 8:
            three = plant_flowers_brute(n, paths, kinds=3)
            assert three == [] or is_valid(n, paths, three, 3)


def test_large_input_is_fast():
    rng = random.Random(9)
    n = 50_000
    # A ring of gardens plus a random perfect matching: degree 3.
    order = list(range(1, n + 1))
    rng.shuffle(order)
    paths = [[i, i % n + 1] for i in range(1, n + 1)]
    pairs = {frozenset(p) for p in paths}
    for i in range(0, n, 2):
        x, y = order[i], order[i + 1]
        if frozenset((x, y)) not in pairs:
            paths.append([x, y])
    start = time.perf_counter()
    flower = plant_flowers(n, paths)
    assert time.perf_counter() - start < 2.0
    assert is_valid(n, paths, flower)
