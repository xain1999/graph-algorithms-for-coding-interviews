import random
import sys

import pytest

from solutions.p016_flood_fill import flood_fill
from solutions.p016_flood_fill_recursive import flood_fill_recursive

SOLVERS = [flood_fill, flood_fill_recursive]

EXAMPLE_1 = [
    [2, 2, 1, 1, 0],
    [2, 1, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [0, 1, 2, 1, 1],
]
ANSWER_1 = [
    [2, 2, 3, 3, 0],
    [2, 3, 3, 0, 1],
    [3, 3, 0, 0, 1],
    [0, 3, 2, 1, 1],
]
EXAMPLE_2 = [
    [5, 5, 0],
    [0, 5, 5],
]
EXAMPLE_3 = [
    [7, 0, 7],
    [0, 7, 0],
    [7, 0, 7],
]
ANSWER_3 = [
    [7, 0, 7],
    [0, 9, 0],
    [7, 0, 7],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "image, sr, sc, color, expected",
    [
        (EXAMPLE_1, 1, 2, 3, ANSWER_1),        # book example 1
        (EXAMPLE_2, 0, 1, 5, EXAMPLE_2),       # book example 2 (same color)
        (EXAMPLE_3, 1, 1, 9, ANSWER_3),        # former example 3: diagonals
        ([[0]], 0, 0, 4, [[4]]),               # single pixel
        ([[4]], 0, 0, 4, [[4]]),               # single pixel, same color
        ([[1, 1, 1]], 0, 2, 0, [[0, 0, 0]]),   # whole image is one region
        ([[1], [0], [1]], 2, 0, 6, [[1], [0], [6]]),
        (EXAMPLE_1, 1, 4, 3,                   # the other region of 1s
         [[2, 2, 1, 1, 0],
          [2, 1, 1, 0, 3],
          [1, 1, 0, 0, 3],
          [0, 1, 2, 3, 3]]),
    ],
)
def test_examples(solve, image, sr, sc, color, expected):
    assert solve(image, sr, sc, color) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    image = [row[:] for row in EXAMPLE_1]
    solve(image, 1, 2, 3)
    assert image == EXAMPLE_1


@pytest.mark.parametrize("solve", SOLVERS)
def test_same_color_returns_a_copy(solve):
    image = [row[:] for row in EXAMPLE_2]
    out = solve(image, 0, 0, 5)
    assert out == image and out is not image


def repaint_by_definition(image, sr, sc, color):
    """Reference: grow the region by repeated full scans."""
    rows, cols = len(image), len(image[0])
    old = image[sr][sc]
    region = {(sr, sc)}
    grew = True
    while grew:
        grew = False
        for r in range(rows):
            for c in range(cols):
                if (r, c) in region or image[r][c] != old:
                    continue
                if any((r + dr, c + dc) in region
                       for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    region.add((r, c))
                    grew = True
    return [[color if (r, c) in region else image[r][c]
             for c in range(cols)] for r in range(rows)]


def test_random_images_agree_with_definition():
    rng = random.Random(733)
    for _ in range(1500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        image = [[rng.randint(0, 2) for _ in range(cols)]
                 for _ in range(rows)]
        sr, sc = rng.randrange(rows), rng.randrange(cols)
        color = rng.randint(0, 3)
        expected = repaint_by_definition(image, sr, sc, color)
        for solve in SOLVERS:
            assert solve(image, sr, sc, color) == expected


def test_large_single_color_image_is_fast():
    # 400 x 400 = 160,000 pixels in one region: far too deep for the
    # recursive version, easy for the explicit stack.
    image = [[0] * 400 for _ in range(400)]
    out = flood_fill(image, 123, 45, 9)
    assert all(v == 9 for row in out for v in row)


def test_recursive_version_fails_on_deep_regions():
    image = [[0] * 400 for _ in range(400)]
    assert sys.getrecursionlimit() < 160_000
    with pytest.raises(RecursionError):
        flood_fill_recursive(image, 0, 0, 9)
