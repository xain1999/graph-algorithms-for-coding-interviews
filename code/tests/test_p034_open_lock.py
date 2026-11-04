import itertools
import random
import time

import networkx as nx
import pytest

from solutions.p034_open_lock import neighbors, open_lock
from solutions.p034_open_lock_alt import open_lock_bidirectional

SOLVERS = [open_lock, open_lock_bidirectional]

EXAMPLE_1 = ["0001", "0011", "0021", "0009", "0019"]
RING = ["1000", "9000", "0100", "0900", "0010", "0090", "0001", "0009"]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "deadends, target, expected",
    [
        (EXAMPLE_1, "0018", 5),          # book example 1
        (RING, "5555", -1),              # book example 2 (start walled in)
        (["0000", "2468"], "1357", -1),  # start is dead (edge case)
        ([], "0000", 0),
        (["1234"], "0000", 0),
        (["0000"], "0000", -1),          # jammed beats "already there"
        ([], "0009", 1),                 # wraparound: one turn down
        ([], "5555", 20),                # the farthest position
        ([], "1919", 4),
        (["0018"], "0018", -1),          # target itself is dead
        (RING[:6], "0005", 5),           # only the last dial can move
    ],
)
def test_examples(solve, deadends, target, expected):
    assert solve(deadends, target) == expected


def test_neighbors_of_start_match_chapter_1():
    assert sorted(neighbors("0000")) == sorted(RING)
    assert sorted(neighbors("9090")) == sorted(
        ["0090", "8090", "9190", "9990", "9000", "9080", "9091",
         "9099"])


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    dead = list(EXAMPLE_1)
    solve(dead, "0018")
    assert dead == EXAMPLE_1


ALL = ["".join(p) for p in itertools.product("0123456789", repeat=4)]
FULL = nx.Graph()
for s in ALL:
    for t in neighbors(s):
        FULL.add_edge(s, t)


def networkx_answer(deadends, target):
    dead = set(deadends)
    if "0000" in dead or target in dead:
        return -1
    g = FULL.subgraph(s for s in ALL if s not in dead)
    try:
        return nx.shortest_path_length(g, "0000", target)
    except nx.NetworkXNoPath:
        return -1


def test_random_locks_agree_with_networkx():
    rng = random.Random(752)
    for trial in range(120):
        # Dense dead ends near the start make blocked and long cases.
        k = rng.choice((0, 20, 200, 2000, 5000))
        pool = ALL if trial % 2 else [s for s in ALL
                                      if s[0] in "019" and s[1] in "019"]
        dead = rng.sample(pool, min(k, len(pool)))
        target = rng.choice(ALL)
        want = networkx_answer(dead, target)
        assert open_lock(dead, target) == want
        assert open_lock_bidirectional(dead, target) == want


def test_worst_case_is_fast():
    # Unreachable target: the BFS must exhaust all reachable states.
    dead = [s for s in neighbors("7777")] + ["0123"] * 5000
    for solve in SOLVERS:
        start = time.perf_counter()
        assert solve(dead, "7777") == -1
        assert time.perf_counter() - start < 2.0
