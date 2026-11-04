import random
import time

import networkx as nx
import pytest

from solutions.p046_course_schedule_ii import find_order
from solutions.p046_course_schedule_ii_brute import find_order_brute
from solutions.p046_course_schedule_ii_dfs import find_order_dfs

SOLVERS = [find_order, find_order_dfs, find_order_brute]

EXAMPLE_1 = [[1, 4], [2, 4], [0, 1], [0, 2], [3, 2], [3, 5]]
EXAMPLE_2 = [[1, 0], [2, 1], [3, 2], [1, 3]]


def is_valid(n: int, prereqs: list[list[int]], order: list[int]):
    """The check of Problem 44, with pairs read as [course, pre]."""
    if sorted(order) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[pre] < pos[course] for course, pre in prereqs)


def test_book_example_1_exact_kahn_order():
    assert find_order(6, EXAMPLE_1) == [4, 5, 1, 2, 0, 3]
    assert is_valid(6, EXAMPLE_1, [5, 4, 2, 3, 1, 0])  # also valid


def test_no_pairs_exact_kahn_order():
    assert find_order(3, []) == [0, 1, 2]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, prereqs, possible",
    [
        (6, EXAMPLE_1, True),           # book example 1
        (4, EXAMPLE_2, False),          # book example 2 (cycle 1-2-3)
        (3, [], True),                  # no pairs (not in book)
        (1, [], True),                  # smallest input
        (3, [[1, 2], [2, 1]], False),
        (3, [[2, 0]], True),
        (5, [[4, 3], [3, 2], [2, 1], [1, 0]], True),   # one order only
        (5, [[1, 0], [0, 1], [3, 2]], False),
    ],
)
def test_examples(solve, n, prereqs, possible):
    order = solve(n, prereqs)
    if possible:
        assert is_valid(n, prereqs, order)
    else:
        assert order == []


def test_unique_order_is_found():
    assert find_order(5, [[4, 3], [3, 2], [2, 1], [1, 0]]) == \
        [0, 1, 2, 3, 4]
    assert find_order_dfs(5, [[4, 3], [3, 2], [2, 1], [1, 0]]) == \
        [0, 1, 2, 3, 4]


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    prereqs = [p[:] for p in EXAMPLE_1]
    solve(6, prereqs)
    assert prereqs == EXAMPLE_1


def test_random_graphs():
    rng = random.Random(210)
    for _ in range(1500):
        n = rng.randint(1, 7)
        pairs = {(rng.randrange(n), rng.randrange(n))
                 for _ in range(rng.randint(0, 2 * n))}
        prereqs = [[a, b] for a, b in pairs if a != b]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from((b, a) for a, b in prereqs)
        acyclic = nx.is_directed_acyclic_graph(g)
        for solve in SOLVERS:
            order = solve(n, prereqs)
            if acyclic:
                assert is_valid(n, prereqs, order)
            else:
                assert order == []


def test_large_inputs_are_fast():
    n = 100_000
    rng = random.Random(46)
    label = list(range(n))
    rng.shuffle(label)                  # hidden order to recover
    prereqs = [[label[i + 1], label[i]] for i in range(n - 1)]
    for _ in range(100_000):
        i, j = sorted(rng.sample(range(n), 2))
        prereqs.append([label[j], label[i]])
    start = time.perf_counter()
    for solve in SOLVERS[:2]:
        assert solve(n, prereqs) == label   # the chain forces it
        assert solve(n, prereqs + [[label[0], label[-1]]]) == []
    assert time.perf_counter() - start < 4.0
