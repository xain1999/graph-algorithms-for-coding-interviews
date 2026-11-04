import itertools
import random
import time

import pytest

from solutions.p093_one_stroke import can_draw_in_one_stroke
from solutions.p093_one_stroke_brute import (
    can_draw_in_one_stroke_brute,
)

SOLVERS = [can_draw_in_one_stroke, can_draw_in_one_stroke_brute]

HOUSE = [[0, 1], [1, 3], [3, 4], [4, 2], [2, 0], [0, 3], [1, 2],
         [2, 3]]
TRIANGLES = [[0, 1], [1, 2], [2, 0], [4, 5], [5, 6], [6, 4]]
K4 = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, segments, expected",
    [
        (6, HOUSE, True),           # book example 1 (point 5 unused)
        (7, TRIANGLES, False),      # book example 2 (two pieces)
        (4, K4, False),             # four odd corners (follow-up)
        (1, [], True),              # empty drawing
        (5, [], True),
        (2, [[0, 1]], True),        # one segment
        (4, [[0, 1], [2, 3]], False),   # two separate segments
        (4, [[0, 1], [1, 2], [2, 3], [3, 0]], True),   # a loop
        (4, [[0, 1], [0, 2], [0, 3]], False),          # a star
        (5, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]], True),
        # Review cases R12-R14.
        (4, [[0, 1], [1, 2], [2, 0]], True),    # R12 stray point 3
        (6, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]],
         False),                                # R13 two triangles
        (3, [], True),                          # R14 empty drawing
    ],
)
def test_examples(solve, n, segments, expected):
    assert solve(n, segments) is expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    segments = [pair[:] for pair in HOUSE]
    solve(6, segments)
    assert segments == HOUSE


def test_random_drawings_agree_with_brute_force():
    rng = random.Random(93)
    for _ in range(1500):
        n = rng.randint(1, 6)
        pairs = list(itertools.combinations(range(n), 2))
        segments = [list(p) for p in pairs if rng.random() < 0.45]
        rng.shuffle(segments)
        segments = segments[:9]
        assert (can_draw_in_one_stroke(n, segments)
                == can_draw_in_one_stroke_brute(n, segments))


def test_large_drawing_is_fast():
    n = 100_000
    ring = [[i, (i + 1) % n] for i in range(n)]
    chords = [[0, 2], [4, 6]]
    start = time.perf_counter()
    assert can_draw_in_one_stroke(n, ring) is True
    assert can_draw_in_one_stroke(n, ring + chords[:1]) is True
    assert can_draw_in_one_stroke(n, ring + chords[:2]) is False
    assert can_draw_in_one_stroke(n, ring[:-1]) is True   # a path
    assert time.perf_counter() - start < 2.0
