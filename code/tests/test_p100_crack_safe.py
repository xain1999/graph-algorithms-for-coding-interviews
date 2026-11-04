import itertools
import time

import pytest

from solutions.p100_crack_safe import crack_safe
from solutions.p100_crack_safe_brute import crack_safe_brute
from solutions.p100_crack_safe_greedy import crack_safe_greedy

SOLVERS = [crack_safe, crack_safe_brute]


def opens_safe(text, n, k):
    codes = {text[i:i + n] for i in range(len(text) - n + 1)}
    every = {"".join(p) for p in
             itertools.product(map(str, range(k)), repeat=n)}
    return len(text) == k ** n + n - 1 and codes == every


def test_book_examples():
    assert crack_safe(3, 2) == "0001011100"
    assert crack_safe(2, 3) == "0010211220"


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize("n, k", [
    (n, k) for n in range(1, 5) for k in range(1, 6) if k ** n <= 300
])
def test_small_cases_are_shortest_and_complete(solve, n, k):
    assert opens_safe(solve(n, k), n, k)


@pytest.mark.parametrize("n, k", [
    (n, k) for n in range(1, 6) for k in range(1, 11)
    if k ** n <= 20_000
])
def test_every_allowed_case(n, k):
    assert opens_safe(crack_safe(n, k), n, k)
    assert opens_safe(crack_safe_greedy(n, k), n, k)


def test_largest_case_is_fast():
    start = time.perf_counter()
    text = crack_safe(4, 10)
    assert len(text) == 10_003
    assert time.perf_counter() - start < 0.5
