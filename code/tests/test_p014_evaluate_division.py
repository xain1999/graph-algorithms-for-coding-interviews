import math
import random

import networkx as nx
import pytest
from pytest import approx

from solutions.p014_evaluate_division import calc_equation
from solutions.p014_evaluate_division_brute import calc_equation_brute
from solutions.p014_evaluate_division_wide import calc_equation_wide

SOLVERS = [calc_equation, calc_equation_brute, calc_equation_wide]

KITCHEN = [["cup", "tbsp"], ["tbsp", "tsp"], ["pint", "cup"],
           ["quart", "pint"], ["cup", "floz"]]
KITCHEN_VALUES = [16.0, 3.0, 2.0, 2.0, 8.0]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "equations, values, queries, expected",
    [
        # book example 1: kitchen measures
        (KITCHEN, KITCHEN_VALUES,
         [["pint", "tsp"], ["floz", "tbsp"], ["tbsp", "quart"],
          ["tsp", "tsp"], ["cup", "liter"]],
         [96.0, 2.0, 0.015625, 1.0, -1.0]),
        # book example 2: two separate groups of variables
        ([["a", "b"], ["c", "d"]], [2.5, 4.0],
         [["b", "a"], ["d", "c"], ["a", "c"], ["e", "e"]],
         [0.4, 0.25, -1.0, -1.0]),
        # former book example 3: a cycle of consistent equations
        ([["x", "y"], ["y", "z"], ["z", "x"]], [2.0, 5.0, 0.1],
         [["x", "z"], ["z", "y"]],
         [10.0, 0.2]),
        ([["m", "n"]], [0.5], [["n", "m"], ["m", "m"], ["n", "k"]],
         [2.0, 1.0, -1.0]),
        ([["m", "n"]], [0.5], [["k", "k"], ["k", "j"]], [-1.0, -1.0]),
        ([["m", "n"]], [0.5], [], []),
    ],
)
def test_examples(solve, equations, values, queries, expected):
    assert solve(equations, values, queries) == approx(expected)


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    equations = [row[:] for row in KITCHEN]
    values = KITCHEN_VALUES[:]
    queries = [["pint", "tsp"], ["tsp", "pint"]]
    solve(equations, values, queries)
    assert equations == KITCHEN
    assert values == KITCHEN_VALUES
    assert queries == [["pint", "tsp"], ["tsp", "pint"]]


def random_instance(rng: random.Random):
    """Hidden positive values make every equation consistent."""
    names = [f"v{i}" for i in range(rng.randint(1, 9))]
    hidden = {v: rng.choice([0.5, 1.0, 2.0, 3.0, 4.0, 10.0])
              for v in names}
    pairs = [(a, b) for a in names for b in names if a < b]
    chosen = rng.sample(pairs, rng.randint(0, min(len(pairs), 8)))
    equations = [[a, b] if rng.random() < 0.5 else [b, a]
                 for a, b in chosen]
    values = [hidden[a] / hidden[b] for a, b in equations]
    pool = names + ["zz"]               # zz never appears in equations
    queries = [[rng.choice(pool), rng.choice(pool)]
               for _ in range(10)]
    return equations, values, queries, hidden


def test_random_agree_with_networkx():
    rng = random.Random(399)
    for _ in range(500):
        equations, values, queries, hidden = random_instance(rng)
        graph = nx.Graph()
        graph.add_edges_from(equations)
        expected = []
        for a, b in queries:
            if a in graph and b in graph and nx.has_path(graph, a, b):
                expected.append(hidden[a] / hidden[b])
            else:
                expected.append(-1.0)
        for solve in SOLVERS:
            got = solve(equations, values, queries)
            assert got == approx(expected), solve.__name__


def test_long_chain_is_fast():
    n = 20_000
    equations = [[f"v{i}", f"v{i + 1}"] for i in range(n)]
    values = [1.0] * n
    queries = [["v0", f"v{n}"], [f"v{n}", "v0"]] * 5
    assert calc_equation(equations, values, queries) == [1.0] * 10


# Numeric range. The book's constraints keep every chain product between
# 1e-300 and 1e300. These chains stay inside that range...
CHAIN = [[f"x{i}", f"x{i + 1}"] for i in range(800)]


@pytest.mark.parametrize("solve", [calc_equation, calc_equation_wide])
def test_long_chain_inside_the_float_range(solve):
    values = [2.0] * 400 + [0.5] * 400      # products reach 2**400
    assert solve(CHAIN, values, [["x0", "x800"], ["x800", "x0"],
                                 ["x0", "x400"]]) == [1.0, 1.0, 2.0 ** 400]


# ...and these do not: 8**400 overflows and 0.125**400 underflows, although
# the answer is exactly 1. The plain DFS returns inf and 0.0 here (outside
# its contract); the mantissa/exponent version still answers 1.0.
def test_chain_outside_the_float_range_plain_dfs_breaks():
    up_down = [8.0] * 400 + [0.125] * 400
    down_up = [0.125] * 400 + [8.0] * 400
    query = [["x0", "x800"]]
    assert calc_equation(CHAIN, up_down, query) == [math.inf]
    assert calc_equation(CHAIN, down_up, query) == [0.0]


def test_chain_outside_the_float_range_wide_version_survives():
    up_down = [8.0] * 400 + [0.125] * 400
    down_up = [0.125] * 400 + [8.0] * 400
    query = [["x0", "x800"], ["x800", "x0"]]
    assert calc_equation_wide(CHAIN, up_down, query) == [1.0, 1.0]
    assert calc_equation_wide(CHAIN, down_up, query) == [1.0, 1.0]
    # an answer that is itself out of range is reported as inf / 0.0
    big = calc_equation_wide(CHAIN[:400], [8.0] * 400,
                             [["x0", "x400"], ["x400", "x0"]])
    assert big == [math.inf, 0.0]
