import random
import time

import networkx as nx
import pytest

from solutions.p042_bus_routes import num_buses_to_destination
from solutions.p042_bus_routes_brute import num_buses_brute

SOLVERS = [num_buses_to_destination, num_buses_brute]

EXAMPLE_1 = [[3, 8, 12], [12, 5, 20], [20, 16, 40], [8, 33],
             [33, 41, 16]]
EXAMPLE_2 = [[1, 4, 9], [9, 6], [2, 7, 11]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "routes, source, target, expected",
    [
        (EXAMPLE_1, 3, 40, 3),               # book example 1
        (EXAMPLE_2, 1, 11, -1),              # book example 2
        ([[5, 6]], 8, 8, 0),                 # book example 3
        (EXAMPLE_1, 8, 33, 1),               # one bus, not bus 0
        (EXAMPLE_1, 40, 3, 3),               # same trip backwards
        (EXAMPLE_1, 3, 99, -1),              # target on no route
        (EXAMPLE_1, 99, 3, -1),              # source on no route
        ([[1, 2, 3, 4, 5, 6]], 6, 1, 1),     # long single route
        ([[1, 2], [2, 3], [3, 4], [4, 5]], 1, 5, 4),
    ],
)
def test_examples(solve, routes, source, target, expected):
    assert solve(routes, source, target) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    routes = [r[:] for r in EXAMPLE_1]
    solve(routes, 3, 40)
    assert routes == EXAMPLE_1


def networkx_answer(routes, source, target):
    """Stop-route graph: every bus taken is two edges."""
    graph = nx.Graph()
    for bus, stops in enumerate(routes):
        for stop in stops:
            graph.add_edge(("stop", stop), ("bus", bus))
    if source == target:
        return 0
    try:
        hops = nx.shortest_path_length(graph, ("stop", source),
                                       ("stop", target))
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return -1
    return hops // 2


def test_random_networks_agree():
    rng = random.Random(815)
    for _ in range(600):
        stops = rng.randint(1, 15)
        routes = [rng.sample(range(stops), rng.randint(1, min(5, stops)))
                  for _ in range(rng.randint(1, 8))]
        source = rng.randrange(stops + 1)    # may be on no route
        target = rng.randrange(stops + 1)
        expected = networkx_answer(routes, source, target)
        assert num_buses_to_destination(routes, source, target) == expected
        assert num_buses_brute(routes, source, target) == expected


def test_large_network_is_fast():
    # One huge loop plus a chain of 1000 buses, 3 * 10^5 stops in all.
    routes = [list(range(100_000, 200_000))]
    for bus in range(1000):
        routes.append([bus, bus + 1] + list(range(
            1_000_000 + 198 * bus, 1_000_000 + 198 * (bus + 1))))
    routes.append([1000, 150_000])
    assert sum(map(len, routes)) <= 300_002
    start = time.perf_counter()
    assert num_buses_to_destination(routes, 0, 100_000) == 1002
    assert time.perf_counter() - start < 2.0
