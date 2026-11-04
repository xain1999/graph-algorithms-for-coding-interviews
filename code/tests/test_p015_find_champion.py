import random

import networkx as nx
import pytest

from solutions.p015_find_champion import find_champion
from solutions.p015_find_champion_brute import find_champion_brute

SOLVERS = [find_champion, find_champion_brute]

EXAMPLE_1 = [[4, 0], [0, 2], [4, 1], [1, 5], [2, 3], [5, 3], [1, 2]]
EXAMPLE_2 = [[4, 0], [0, 2], [1, 5], [2, 3], [5, 3], [1, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (6, EXAMPLE_1, 4),                  # book example 1
        (6, EXAMPLE_2, -1),                 # book example 2: 1 and 4
        (4, [[2, 0], [0, 1]], -1),          # book example 3: 3 idle
        (3, [], -1),                        # no games at all
        (1, [], 0),                         # a single team wins
        (2, [[1, 0]], 1),
        (4, [[3, 2], [2, 1], [1, 0]], 3),   # a chain of wins
        (4, [[0, 1], [0, 2], [0, 3]], 0),   # beats everyone directly
        (4, [[0, 1], [2, 3]], -1),          # two separate leagues
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [row[:] for row in EXAMPLE_1]
    solve(6, edges)
    assert edges == EXAMPLE_1


def random_dag(rng: random.Random, n: int, p: float):
    order = list(range(n))
    rng.shuffle(order)                  # edges go left to right
    return [[order[i], order[j]]
            for i in range(n) for j in range(i + 1, n)
            if rng.random() < p]


def test_random_dags_agree():
    rng = random.Random(2924)
    for _ in range(2000):
        n = rng.randint(1, 8)
        edges = random_dag(rng, n, rng.choice([0.1, 0.3, 0.6]))
        expected = find_champion_brute(n, edges)
        assert find_champion(n, edges) == expected
        # networkx: the champion is the one node that reaches all
        graph = nx.DiGraph()
        graph.add_nodes_from(range(n))
        graph.add_edges_from(edges)
        tops = [v for v in graph
                if len(nx.descendants(graph, v)) == n - 1]
        assert expected == (tops[0] if len(tops) == 1 else -1)


def test_large_input_is_fast():
    n = 100_000
    edges = [[i, i + 1] for i in range(n - 1)]
    edges += [[0, i] for i in range(2, n)]
    assert find_champion(n, edges) == 0
    assert find_champion(n + 1, edges) == -1   # team n never played
