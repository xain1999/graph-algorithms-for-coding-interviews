import copy
import random
import time
from collections import Counter

import pytest

from solutions.p098_itinerary import find_itinerary
from solutions.p098_itinerary_brute import find_itinerary_brute

SOLVERS = [find_itinerary, find_itinerary_brute]

EXAMPLE_1 = [["KAP", "LUM"], ["JFK", "NOX"], ["MIR", "KAP"],
             ["JFK", "KAP"], ["LUM", "JFK"], ["KAP", "MIR"]]
EXAMPLE_2 = [["JFK", "AMS"], ["AMS", "RIO"], ["RIO", "JFK"],
             ["JFK", "RIO"], ["RIO", "ZAG"]]


def uses_every_ticket(tickets, route):
    legs = Counter(zip(route, route[1:]))
    return route[0] == "JFK" and legs == Counter(map(tuple, tickets))


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "tickets, expected",
    [
        (EXAMPLE_1, ["JFK", "KAP", "MIR", "KAP", "LUM", "JFK", "NOX"]),
        (EXAMPLE_2, ["JFK", "AMS", "RIO", "JFK", "RIO", "ZAG"]),
        ([["JFK", "QIB"]], ["JFK", "QIB"]),           # one ticket
        ([["JFK", "AAA"], ["JFK", "BBB"], ["BBB", "JFK"]],
         ["JFK", "BBB", "JFK", "AAA"]),               # greedy dead end
        ([["JFK", "JFK"], ["JFK", "ABC"]],
         ["JFK", "JFK", "ABC"]),                      # self-loop
        ([["JFK", "ZZZ"], ["ZZZ", "JFK"]] * 2,
         ["JFK", "ZZZ", "JFK", "ZZZ", "JFK"]),        # repeated tickets
    ],
)
def test_examples(solve, tickets, expected):
    assert solve(tickets) == expected


def test_plain_greedy_fails_on_example_1():
    graph = {}
    for src, dst in EXAMPLE_1:
        graph.setdefault(src, []).append(dst)
    route = ["JFK"]
    while graph.get(route[-1]):
        dests = graph[route[-1]]
        dests.sort()
        route.append(dests.pop(0))
    assert route == ["JFK", "KAP", "LUM", "JFK", "NOX"]  # stuck


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    tickets = copy.deepcopy(EXAMPLE_1)
    solve(tickets)
    assert tickets == EXAMPLE_1


def random_trip(rng, airports, length):
    route = ["JFK"]
    for _ in range(length):
        route.append(rng.choice(airports))
    tickets = [list(leg) for leg in zip(route, route[1:])]
    rng.shuffle(tickets)
    return tickets


def test_random_trips_agree_with_backtracking():
    rng = random.Random(332)
    for _ in range(500):
        k = rng.randint(1, 5)
        airports = ["JFK"] + [f"A{i}X" for i in range(k)]
        tickets = random_trip(rng, airports, rng.randint(1, 12))
        got = find_itinerary(tickets)
        assert uses_every_ticket(tickets, got)
        assert got == find_itinerary_brute(tickets)


def test_large_input_is_fast():
    rng = random.Random(98)
    airports = ["JFK"] + [f"B{i:02d}" for i in range(30)]
    tickets = random_trip(rng, airports, 2000)
    start = time.perf_counter()
    route = find_itinerary(tickets)
    assert time.perf_counter() - start < 0.5
    assert uses_every_ticket(tickets, route)
