import math
import random
import time

import pytest

from solutions.p073_max_probability import max_probability
from solutions.p073_max_probability_brute import max_probability_brute
from solutions.p073_max_probability_log import max_probability_log

SOLVERS = [max_probability, max_probability_brute, max_probability_log]

EDGES_1 = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [2, 4]]
PROBS_1 = [0.9, 0.5, 0.8, 0.4, 0.9, 0.5, 0.3]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, probs, start, end, expected",
    [
        (5, EDGES_1, PROBS_1, 0, 4, 0.324),             # book example 1
        (4, [[0, 1], [1, 3], [0, 2]], [0.6, 0.0, 1.0], 0, 3,
         0.0),                                         # book example 2
        (2, [], [], 0, 1, 0.0),                        # no edges
        (3, [[0, 1]], [0.7], 2, 2, 1.0),               # start == end
        (2, [[0, 1], [1, 0]], [0.2, 0.6], 1, 0, 0.6),  # parallel edges
        (3, [[0, 1], [1, 2]], [1.0, 1.0], 0, 2, 1.0),  # certain edges
        (4, [[3, 2], [2, 1], [1, 0]], [0.5, 0.5, 0.5], 0, 3,
         0.125),                                       # reverse order
    ],
)
def test_examples(solve, n, edges, probs, start, end, expected):
    assert solve(n, edges, probs, start, end) == pytest.approx(expected)


def test_does_not_mutate_input():
    edges = [e[:] for e in EDGES_1]
    probs = PROBS_1[:]
    for solve in SOLVERS:
        solve(5, edges, probs, 0, 4)
    assert edges == EDGES_1 and probs == PROBS_1


def best_by_enumeration(n, edges, probs, start, end):
    """Try every simple path (tiny graphs only)."""
    graph = [[] for _ in range(n)]
    for (a, b), p in zip(edges, probs):
        graph[a].append((b, p))
        graph[b].append((a, p))
    best = 0.0
    stack = [(start, 1.0, {start})]
    while stack:
        node, prob, seen = stack.pop()
        if node == end:
            best = max(best, prob)
            continue
        for nxt, p in graph[node]:
            if nxt not in seen:
                stack.append((nxt, prob * p, seen | {nxt}))
    return best


def test_random_graphs_agree():
    rng = random.Random(1514)
    for _ in range(500):
        n = rng.randint(2, 7)
        m = rng.randint(0, 2 * n)
        edges = [[rng.randrange(n), rng.randrange(n)] for _ in range(m)]
        edges = [e for e in edges if e[0] != e[1]]
        probs = [rng.choice((0.0, 1.0, round(rng.random(), 2)))
                 for _ in edges]
        start, end = rng.randrange(n), rng.randrange(n)
        expected = best_by_enumeration(n, edges, probs, start, end)
        for solve in SOLVERS:
            got = solve(n, edges, probs, start, end)
            assert got == pytest.approx(expected, abs=1e-9)


def test_large_input_is_fast():
    rng = random.Random(73)
    n, m = 30_000, 50_000
    edges = [[i, i + 1] for i in range(n - 1)]
    edges += [[rng.randrange(n), rng.randrange(n)]
              for _ in range(m - (n - 1))]
    probs = [0.9999] * (n - 1) + [rng.random() for _ in range(m - n + 1)]
    start = time.perf_counter()
    got = max_probability(n, edges, probs, 0, n - 1)
    assert time.perf_counter() - start < 2.0
    assert got == pytest.approx(max_probability_log(n, edges, probs,
                                                    0, n - 1))
    assert got >= 0.9999 ** (n - 1) * (1 - 1e-9)
    assert not math.isnan(got)
