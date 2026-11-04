import random
import time

import pytest

from solutions.p059_smallest_swaps import smallest_string_with_swaps
from solutions.p059_smallest_swaps_brute import smallest_swaps_brute

SOLVERS = [smallest_string_with_swaps, smallest_swaps_brute]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "s, pairs, expected",
    [
        ("pandemic", [[5, 0], [7, 5], [2, 6], [6, 4], [3, 1]],
         "caedimnp"),                       # book example 1
        ("tulip", [[0, 4], [4, 0], [1, 1]], "pulit"),   # example 2
        ("vector", [[0, 3], [3, 5]], "rectov"),         # not in book
        ("q", [], "q"),                     # smallest input
        ("zyx", [], "zyx"),                 # no swaps at all
        ("bbaa", [[0, 3]], "abab"),
        ("ccc", [[0, 1], [1, 2]], "ccc"),
    ],
)
def test_examples(solve, s, pairs, expected):
    assert solve(s, pairs) == expected


def test_random_agree_with_brute_force():
    rng = random.Random(1202)
    for _ in range(500):
        n = rng.randint(1, 7)
        s = "".join(rng.choice("abcd") for _ in range(n))
        pairs = [[rng.randrange(n), rng.randrange(n)]
                 for _ in range(rng.randint(0, 6))]
        assert (smallest_string_with_swaps(s, pairs)
                == smallest_swaps_brute(s, pairs))


def test_does_not_mutate_input():
    pairs = [[5, 0], [7, 5], [2, 6]]
    smallest_string_with_swaps("pandemic", pairs)
    assert pairs == [[5, 0], [7, 5], [2, 6]]


def test_large_input_is_fast():
    rng = random.Random(7)
    n = 2 * 10**5
    s = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz")
                for _ in range(n))
    pairs = [[rng.randrange(n), rng.randrange(n)] for _ in range(n)]
    start = time.perf_counter()
    out = smallest_string_with_swaps(s, pairs)
    assert time.perf_counter() - start < 2.0
    assert sorted(out) == sorted(s)
    # one long chain: everything sorts
    chain = [[i, i + 1] for i in range(n - 1)]
    assert smallest_string_with_swaps(s, chain) == "".join(sorted(s))


def test_greedy_trap_from_the_book():
    assert smallest_string_with_swaps("bac", [[0, 2], [2, 1]]) == "abc"
