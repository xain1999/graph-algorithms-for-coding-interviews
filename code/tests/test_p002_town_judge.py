import random

import pytest

from solutions.p002_town_judge import find_judge
from solutions.p002_town_judge_brute import find_judge_brute

SOLVERS = [find_judge, find_judge_brute]

EXAMPLE_1 = [[1, 4], [2, 4], [3, 4], [5, 4], [2, 1], [5, 3]]
EXAMPLE_2 = [[1, 3], [2, 3], [4, 3], [3, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, trust, expected",
    [
        (5, EXAMPLE_1, 4),                 # book example 1
        (4, EXAMPLE_2, -1),                # book example 2
        (1, [], 1),                        # a town of one
        (2, [], -1),                       # nobody trusted
        (2, [[2, 1]], 1),
        (2, [[1, 2], [2, 1]], -1),         # mutual trust
        (3, [[1, 3]], -1),                 # 2 does not trust 3
        (4, [[1, 4], [2, 4], [3, 4], [1, 2], [3, 2]], 4),
    ],
)
def test_examples(solve, n, trust, expected):
    assert solve(n, trust) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    trust = [p[:] for p in EXAMPLE_1]
    solve(5, trust)
    assert trust == EXAMPLE_1


def test_random_agrees_with_brute_force():
    rng = random.Random(997)
    for _ in range(3000):
        n = rng.randint(1, 7)
        pairs = [[a, b] for a in range(1, n + 1)
                 for b in range(1, n + 1) if a != b]
        trust = rng.sample(pairs, rng.randint(0, len(pairs)))
        if rng.random() < 0.5 and n > 1:
            # Plant a judge, then maybe spoil it with one more edge.
            j = rng.randint(1, n)
            trust = [p for p in trust if p[0] != j]
            trust += [[a, j] for a in range(1, n + 1)
                      if a != j and [a, j] not in trust]
            rng.shuffle(trust)
        assert find_judge(n, trust) == find_judge_brute(n, trust)


def test_duplicate_pair_fools_the_score():
    # Documented limitation: pairs must be distinct (see pitfalls).
    assert find_judge(3, [[1, 3], [1, 3]]) == 3
    assert find_judge_brute(3, [[1, 3], [1, 3]]) == 3


def test_large_input_is_fast():
    n = 1000
    trust = [[a, b] for a in range(1, n + 1)
             for b in range(1, n + 1) if a != b and b != 500]
    trust = [p for p in trust if p[0] != 500]
    trust += [[a, 500] for a in range(1, n + 1) if a != 500]
    assert len(trust) > 990_000
    assert find_judge(n, trust) == 500
