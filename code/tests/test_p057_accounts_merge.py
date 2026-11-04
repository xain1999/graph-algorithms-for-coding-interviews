import random
import time

import pytest

from solutions.p057_accounts_merge import accounts_merge
from solutions.p057_accounts_merge_brute import accounts_merge_brute
from solutions.p057_accounts_merge_dfs import accounts_merge_dfs

SOLVERS = [accounts_merge, accounts_merge_brute, accounts_merge_dfs]

EXAMPLE_1 = [
    ["Noor", "noor@home.net", "n.k@work.org"],
    ["Tariq", "tariq@mail.io"],
    ["Noor", "noorx@club.net"],
    ["Tariq", "tariq.s@band.org", "tariq@mail.io"],
    ["Noor", "noor99@mail.io"],
    ["Noor", "noor.k@uni.edu", "noorx@club.net", "n.k@work.org"],
    ["Tariq", "tariq@mail.io", "tariq.s@band.org"],
]
EXPECTED_1 = [
    ["Noor", "n.k@work.org", "noor.k@uni.edu", "noor@home.net",
     "noorx@club.net"],
    ["Noor", "noor99@mail.io"],
    ["Tariq", "tariq.s@band.org", "tariq@mail.io"],
]
EXAMPLE_2 = [
    ["Ivo", "ivo@a.org"],
    ["Ivo", "ivo@b.org"],
    ["Ivo", "ivo@c.org", "ivo@b.org"],
]
EXPECTED_2 = [
    ["Ivo", "ivo@a.org"],
    ["Ivo", "ivo@b.org", "ivo@c.org"],
]
EXAMPLE_3 = [
    ["Ada", "a1@x.io", "a2@x.io"],
    ["Ada", "a3@x.io", "a4@x.io"],
    ["Ada", "a5@x.io", "a6@x.io"],
    ["Ada", "a6@x.io", "a3@x.io", "a1@x.io"],
]
EXPECTED_3 = [["Ada"] + [f"a{k}@x.io" for k in range(1, 7)]]


def canon(result):
    return sorted(result)


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "accounts, expected",
    [
        (EXAMPLE_1, EXPECTED_1),            # book example 1
        (EXAMPLE_2, EXPECTED_2),            # book example 2
        (EXAMPLE_3, EXPECTED_3),            # a bridging account
        ([["Zoe", "z@q.io"]], [["Zoe", "z@q.io"]]),     # smallest
        ([["Bo", "b@1", "b@1"]], [["Bo", "b@1"]]),      # repeat
        ([["Bo", "b@2", "b@1"], ["Bo", "b@1"]],
         [["Bo", "b@1", "b@2"]]),
    ],
)
def test_examples(solve, accounts, expected):
    assert canon(solve(accounts)) == canon(expected)


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    accounts = [row[:] for row in EXAMPLE_1]
    solve(accounts)
    assert accounts == EXAMPLE_1


def random_accounts(rng, people, pool):
    """Each person owns a disjoint block of emails."""
    accounts = []
    for p in range(people):
        emails = [f"u{p}e{k}@m.io" for k in range(pool)]
        for _ in range(rng.randint(1, 3)):
            size = rng.randint(1, min(4, pool))
            accounts.append([f"P{p % 3}"] + rng.sample(emails, size))
    rng.shuffle(accounts)
    return accounts


def test_random_agree_with_brute_force():
    rng = random.Random(721)
    for _ in range(400):
        accounts = random_accounts(rng, rng.randint(1, 4),
                                   rng.randint(1, 5))
        expected = canon(accounts_merge_brute(accounts))
        assert canon(accounts_merge(accounts)) == expected
        assert canon(accounts_merge_dfs(accounts)) == expected


def test_large_input_is_fast():
    # 3000 accounts of 8 emails in one long chain: all one person.
    accounts = [["Max"] + [f"m{i + k}@big.io" for k in range(8)]
                for i in range(0, 3000 * 7, 7)]
    start = time.perf_counter()
    result = accounts_merge(accounts)
    assert time.perf_counter() - start < 1.0
    assert len(result) == 1 and len(result[0]) == 1 + 3000 * 7 + 1
    assert len(accounts_merge_dfs(accounts)) == 1
