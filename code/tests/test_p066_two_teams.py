import random
import time

import networkx as nx
import pytest

from solutions.p066_two_teams import split_into_teams
from solutions.p066_two_teams_brute import split_into_teams_brute

SOLVERS = [split_into_teams, split_into_teams_brute]

EXAMPLE_1 = [[0, 1], [1, 2], [0, 3], [1, 4], [3, 4], [2, 5],
             [4, 5], [6, 7]]
EXAMPLE_2 = [[3, 0], [0, 1], [1, 4], [4, 3], [1, 2], [2, 4]]
GREEDY_TRAP = [[0, 2], [1, 3], [2, 3]]


def is_valid(n, rivals, team):
    return (len(team) == n and set(team) <= {0, 1}
            and all(team[a] != team[b] for a, b in rivals))


def test_book_outputs():
    assert split_into_teams(8, EXAMPLE_1) == [0, 1, 0, 1, 0, 1, 0, 1]
    assert split_into_teams(6, EXAMPLE_2) == []
    assert split_into_teams(3, []) == [0, 0, 0]
    assert split_into_teams(4, GREEDY_TRAP) == [0, 1, 1, 0]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, rivals, possible",
    [
        (8, EXAMPLE_1, True),               # book example 1
        (6, EXAMPLE_2, False),              # book example 2 (triangle)
        (3, [], True),                      # no rivalries
        (4, GREEDY_TRAP, True),             # label-order greedy fails
        (1, [], True),                      # smallest input
        (2, [[0, 1]], True),
        (3, [[0, 1], [1, 2], [2, 0]], False),           # triangle
        (5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], False),
        (6, [[0, 1], [2, 3], [3, 4], [4, 2]], False),   # 2nd group
        (4, [[0, 1], [1, 2], [2, 3], [3, 0]], True),    # even cycle
    ],
)
def test_examples(solve, n, rivals, possible):
    team = solve(n, rivals)
    if possible:
        assert is_valid(n, rivals, team)
    else:
        assert team == []


def test_does_not_mutate_input():
    rivals = [e[:] for e in EXAMPLE_1]
    split_into_teams(8, rivals)
    assert rivals == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(66)
    for _ in range(1500):
        n = rng.randint(1, 9)
        p = rng.choice((0.15, 0.3, 0.5))
        rivals = [[a, b] for a in range(n) for b in range(a + 1, n)
                  if rng.random() < p]
        rng.shuffle(rivals)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(rivals)
        possible = nx.is_bipartite(g)
        for solve in SOLVERS:
            team = solve(n, rivals)
            if possible:
                assert is_valid(n, rivals, team), (n, rivals)
            else:
                assert team == [], (n, rivals)


def test_large_input_is_fast():
    n = 50_000
    rng = random.Random(1)
    # A long path (deep for DFS) plus random even-gap rivalries.
    rivals = [[i, i + 1] for i in range(n - 1)]
    while len(rivals) < 100_000:
        a = rng.randrange(n)
        b = a + 2 * rng.randint(1, 50) + 1
        if b < n:
            rivals.append([a, b])
    start = time.perf_counter()
    team = split_into_teams(n, rivals)
    assert time.perf_counter() - start < 2.0
    assert is_valid(n, rivals, team)
    rivals.append([0, 2])                # creates a triangle 0-1-2
    assert split_into_teams(n, rivals) == []


def test_one_direction_edges_reject_valid_input():
    # Pitfall in the book: storing [1, 0] only at player 1 makes
    # players 0 and 1 start separate groups on team 0, then clash.
    from collections import deque
    graph = [[], [0]]
    team = [-1, -1]
    clash = False
    for start in range(2):
        if team[start] != -1:
            continue
        team[start] = 0
        queue = deque([start])
        while queue:
            player = queue.popleft()
            for rival in graph[player]:
                if team[rival] == -1:
                    team[rival] = 1 - team[player]
                    queue.append(rival)
                elif team[rival] == team[player]:
                    clash = True
    assert clash
    assert split_into_teams(2, [[1, 0]]) in ([0, 1], [1, 0])
