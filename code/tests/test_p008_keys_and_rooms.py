import random

import networkx as nx
import pytest

from solutions.p008_keys_and_rooms import can_visit_all_rooms
from solutions.p008_keys_and_rooms_brute import (
    can_visit_all_rooms_brute,
)

SOLVERS = [can_visit_all_rooms, can_visit_all_rooms_brute]

EXAMPLE_1 = [[3], [5], [3], [1, 4], [0], [2]]
EXAMPLE_2 = [[1, 2], [2], [0], [4], [3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "rooms, expected",
    [
        (EXAMPLE_1, True),                  # book example 1
        (EXAMPLE_2, False),                 # book example 2
        ([[]], True),                       # a single room
        ([[], [0]], False),                 # key to 0 is useless
        ([[0, 0, 1], [1]], True),           # repeated / own keys
        ([[1], [2], [3], [4], []], True),   # a chain
        ([[1], [0], [3], [2]], False),      # two closed loops
    ],
)
def test_examples(solve, rooms, expected):
    assert solve(rooms) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    rooms = [keys[:] for keys in EXAMPLE_1]
    solve(rooms)
    assert rooms == EXAMPLE_1


def test_random_buildings_agree_with_networkx():
    rng = random.Random(841)
    for _ in range(2000):
        n = rng.randint(1, 9)
        rooms = [[rng.randrange(n) for _ in range(rng.randint(0, 3))]
                 for _ in range(n)]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from((r, k) for r, keys in enumerate(rooms)
                         for k in keys)
        expected = len(nx.descendants(g, 0)) + 1 == n
        assert can_visit_all_rooms(rooms) == expected
        assert can_visit_all_rooms_brute(rooms) == expected


def test_large_building_is_fast():
    n = 100_000
    rooms = [[i + 1] for i in range(n - 1)] + [[]]  # one long chain
    assert can_visit_all_rooms(rooms) is True
    rooms[n // 2] = []                              # break the chain
    assert can_visit_all_rooms(rooms) is False
