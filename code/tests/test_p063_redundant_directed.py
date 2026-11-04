import random
import time

import pytest

from solutions.p063_redundant_directed import find_redundant_directed
from solutions.p063_redundant_directed_brute import (
    find_redundant_directed_brute, is_rooted_tree)

SOLVERS = [find_redundant_directed, find_redundant_directed_brute]

# Book examples, one per case.
CASE_A = [[4, 2], [4, 6], [2, 1], [6, 3], [2, 5], [6, 1]]
CASE_B = [[2, 5], [3, 1], [5, 3], [3, 2], [1, 4]]
CASE_C = [[1, 3], [2, 4], [5, 2], [3, 6], [1, 2], [4, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, expected",
    [
        (CASE_A, [6, 1]),        # two parents, no cycle: the later
        (CASE_B, [3, 2]),        # a cycle, no two parents
        (CASE_C, [5, 2]),        # both: the parent edge on the cycle
        ([[1, 2], [2, 1]], [2, 1]),              # smallest input
        ([[2, 1], [1, 2]], [1, 2]),
        ([[3, 2], [1, 3], [1, 2]], [1, 2]),
        ([[2, 3], [3, 1], [1, 2]], [1, 2]),      # a pure cycle
        ([[1, 2], [2, 3], [3, 2]], [3, 2]),      # 2 <-> 3 + double
    ],
)
def test_examples(solve, edges, expected):
    assert solve(edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in CASE_C]
    solve(edges)
    assert edges == CASE_C


def random_instance(rng: random.Random, n: int) -> list[list[int]]:
    """A random rooted tree on 1..n plus one new directed edge."""
    labels = list(range(1, n + 1))
    rng.shuffle(labels)                 # labels[0] is the root
    edges = [[labels[rng.randrange(i)], labels[i]]
             for i in range(1, n)]
    existing = {tuple(e) for e in edges}
    while True:
        u, v = rng.sample(labels, 2)
        if (u, v) not in existing:
            break
    edges.insert(rng.randrange(n), [u, v])
    rng.shuffle(edges)
    return edges


def test_random_instances_agree_with_brute_force():
    rng = random.Random(685)
    for _ in range(2000):
        edges = random_instance(rng, rng.randint(2, 9))
        answer = find_redundant_directed(edges)
        assert answer == find_redundant_directed_brute(edges)
        rest = [e for e in edges if e != answer]
        assert is_rooted_tree(len(edges), rest)


def test_long_chain_is_fast():
    # A chain 1 -> 2 -> ... -> n with an edge back into the middle,
    # listed first or last: only the back edge leaves a tree.
    n = 100_000
    chain = [[i, i + 1] for i in range(1, n)]
    back = [n, n // 2]
    start = time.perf_counter()
    assert find_redundant_directed(chain + [back]) == back
    assert find_redundant_directed([back] + chain) == back
    assert time.perf_counter() - start < 1.0


def test_undirected_answer_is_wrong_in_case_a():
    # Pitfall in the book: node 1 has two parents and there is no
    # directed cycle; the undirected method would answer [4, 3].
    from solutions.p056_redundant_connection import (
        find_redundant_connection)
    edges = [[2, 1], [3, 1], [4, 2], [4, 3]]
    assert find_redundant_connection(edges) == [4, 3]
    assert find_redundant_directed(edges) == [3, 1]
