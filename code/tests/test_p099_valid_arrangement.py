import copy
import itertools
import random
import time
from collections import Counter

import pytest

from solutions.p099_valid_arrangement import valid_arrangement
from solutions.p099_valid_arrangement_brute import (
    valid_arrangement_brute)
from solutions.p099_valid_arrangement_smallest import (
    smallest_valid_arrangement)

SOLVERS = [valid_arrangement, valid_arrangement_brute]

EXAMPLE_1 = [[2, 4], [7, 2], [4, 9], [7, 5], [9, 4], [4, 7]]
EXAMPLE_2 = [[5, 1], [1, 5], [5, 1]]


def is_valid(pairs, answer):
    same = Counter(map(tuple, pairs)) == Counter(map(tuple, answer))
    chained = all(answer[i][1] == answer[i + 1][0]
                  for i in range(len(answer) - 1))
    return same and chained


def test_book_example_outputs():
    assert valid_arrangement(EXAMPLE_1) == [
        [7, 2], [2, 4], [4, 9], [9, 4], [4, 7], [7, 5]]
    assert valid_arrangement(EXAMPLE_2) == [[5, 1], [1, 5], [5, 1]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize("pairs", [
    EXAMPLE_1,
    EXAMPLE_2,
    [[8, 3]],                               # one pair
    [[6, 6], [6, 6]],                       # self-loops
    [[3, 8], [8, 6], [6, 8], [8, 3]],       # balanced: a circuit
    [[10**12, 0], [0, 10**12], [10**12, 1]],
])
def test_examples_are_valid(solve, pairs):
    assert is_valid(pairs, solve(pairs))


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    pairs = copy.deepcopy(EXAMPLE_1)
    solve(pairs)
    assert pairs == EXAMPLE_1


def random_pairs(rng, nodes, length):
    walk = [rng.randrange(nodes) for _ in range(length + 1)]
    pairs = [[a, b] for a, b in zip(walk, walk[1:])]
    rng.shuffle(pairs)
    return pairs


def test_random_inputs_are_valid():
    rng = random.Random(2097)
    for _ in range(600):
        pairs = random_pairs(rng, rng.randint(1, 6), rng.randint(1, 9))
        assert is_valid(pairs, valid_arrangement(pairs))
        assert is_valid(pairs, valid_arrangement_brute(pairs))


def test_large_input_is_fast():
    rng = random.Random(99)
    pairs = random_pairs(rng, 1000, 200_000)
    start = time.perf_counter()
    answer = valid_arrangement(pairs)
    assert time.perf_counter() - start < 2.0
    assert is_valid(pairs, answer)


def smallest_by_brute_force(pairs):
    """Try every order of the pairs; keep the smallest valid one."""
    best = None
    for order in set(itertools.permutations(map(tuple, pairs))):
        answer = [list(p) for p in order]
        if is_valid(pairs, answer) and (best is None or answer < best):
            best = answer
    return best


def test_smallest_needs_the_smallest_circuit_start():
    # Review case R18: pairs[0][0] = 2 would start the circuit at 2.
    assert valid_arrangement([[2, 1], [1, 2]]) == [[2, 1], [1, 2]]
    assert smallest_valid_arrangement([[2, 1], [1, 2]]) == [
        [1, 2], [2, 1]]


def test_smallest_matches_brute_force_on_small_multigraphs():
    edges = list(itertools.product(range(3), repeat=2))  # with loops
    checked = 0
    for size in range(1, 6):
        for combo in itertools.combinations_with_replacement(
                edges, size):
            pairs = [list(e) for e in combo]
            expected = smallest_by_brute_force(pairs)
            if expected is None:
                continue                # no valid arrangement
            assert smallest_valid_arrangement(pairs) == expected
            checked += 1
    assert checked == 596


@pytest.mark.parametrize("pairs", [EXAMPLE_1, EXAMPLE_2])
def test_smallest_on_book_examples(pairs):
    given = copy.deepcopy(pairs)
    answer = smallest_valid_arrangement(given)
    assert given == pairs               # input is not mutated
    assert is_valid(pairs, answer)
    assert answer == smallest_by_brute_force(pairs)
