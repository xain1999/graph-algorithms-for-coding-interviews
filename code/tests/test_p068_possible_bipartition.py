import random
import time

import networkx as nx
import pytest

from solutions.p068_possible_bipartition import possible_bipartition
from solutions.p068_possible_bipartition_brute import (
    possible_bipartition_brute,
)
from solutions.p068_possible_bipartition_cycle import find_odd_cycle

SOLVERS = [possible_bipartition, possible_bipartition_brute]

EXAMPLE_1 = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 1], [1, 4]]
EXAMPLE_2 = [[1, 5], [5, 2], [2, 6], [6, 3], [3, 7], [7, 1], [2, 4],
             [4, 7]]


def check_odd_cycle(n, dislikes, cycle):
    """The cycle is odd, simple and uses only real dislikes."""
    pairs = {frozenset(p) for p in dislikes}
    assert len(cycle) % 2 == 1 and len(cycle) >= 3
    assert len(set(cycle)) == len(cycle)
    assert all(1 <= p <= n for p in cycle)
    for i, p in enumerate(cycle):
        q = cycle[(i + 1) % len(cycle)]
        assert frozenset((p, q)) in pairs


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, dislikes, expected",
    [
        (6, EXAMPLE_1, True),               # book example 1
        (7, EXAMPLE_2, False),              # book example 2
        (4, [], True),                      # no dislikes
        (1, [], True),                      # smallest input
        (2, [[2, 1]], True),
        (4, [[2, 3], [3, 4], [4, 2]], False),   # triangle, 1 alone
        (5, [[4, 5], [5, 3], [3, 4]], False),   # 1 and 2 unused
        (6, [[1, 2], [3, 4], [5, 6]], True),
    ],
)
def test_examples(solve, n, dislikes, expected):
    assert solve(n, dislikes) == expected


def test_book_odd_cycle():
    assert find_odd_cycle(7, EXAMPLE_2) == [2, 5, 1, 7, 4]
    check_odd_cycle(7, EXAMPLE_2, find_odd_cycle(7, EXAMPLE_2))
    assert find_odd_cycle(6, EXAMPLE_1) == []


def test_does_not_mutate_input():
    dislikes = [p[:] for p in EXAMPLE_2]
    possible_bipartition(7, dislikes)
    find_odd_cycle(7, dislikes)
    assert dislikes == EXAMPLE_2


def test_random_graphs_agree_with_networkx():
    rng = random.Random(886)
    for _ in range(1500):
        n = rng.randint(1, 10)
        p = rng.choice((0.1, 0.2, 0.35, 0.5))
        dislikes = [[a, b] for a in range(1, n + 1)
                    for b in range(a + 1, n + 1) if rng.random() < p]
        rng.shuffle(dislikes)
        g = nx.Graph()
        g.add_nodes_from(range(1, n + 1))
        g.add_edges_from(dislikes)
        expected = nx.is_bipartite(g)
        for solve in SOLVERS:
            assert solve(n, dislikes) == expected, (n, dislikes)
        cycle = find_odd_cycle(n, dislikes)
        if expected:
            assert cycle == []
        else:
            check_odd_cycle(n, dislikes, cycle)


def test_large_input_is_fast():
    n = 5000
    rng = random.Random(5)
    dislikes = [[i, i + 1] for i in range(1, n)]     # a long path
    while len(dislikes) < 30_000:
        a = rng.randint(1, n)
        b = a + 2 * rng.randint(1, 100) + 1
        if b <= n:
            dislikes.append([a, b])
    start = time.perf_counter()
    assert possible_bipartition(n, dislikes) is True
    assert find_odd_cycle(n, dislikes) == []
    dislikes.append([1, n - 1])         # closes a cycle of n - 1
    assert possible_bipartition(n, dislikes) is False
    check_odd_cycle(n, dislikes, find_odd_cycle(n, dislikes))
    assert time.perf_counter() - start < 2.0


def test_one_direction_edges_reject_valid_input():
    # Pitfall in the book: with [[2, 1]] stored only at person 2,
    # persons 1 and 2 each start a BFS in group 0 and then clash.
    from collections import deque
    graph = [[], [], [1]]
    group = [-1, -1, -1]
    clash = False
    for start in (1, 2):
        if group[start] != -1:
            continue
        group[start] = 0
        queue = deque([start])
        while queue:
            person = queue.popleft()
            for other in graph[person]:
                if group[other] == -1:
                    group[other] = 1 - group[person]
                    queue.append(other)
                elif group[other] == group[person]:
                    clash = True
    assert clash
    assert possible_bipartition(2, [[2, 1]]) is True
