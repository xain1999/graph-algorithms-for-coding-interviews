import random
import time

import networkx as nx
import pytest

from solutions.p033_nearest_exit import nearest_exit
from solutions.p033_nearest_exit_alt import nearest_exit_full

SOLVERS = [nearest_exit, nearest_exit_full]

EXAMPLE_1 = [
    "+++++.+",
    "+...+.+",
    "+.+...+",
    "..+.+.+",
    "+.+.+..",
    "+++++++",
]
EXAMPLE_2 = [
    "+++++",
    "...+.",
    "+.+..",
    "+...+",
    "+++++",
]
EXAMPLE_3 = [
    "+.++",
    "+..+",
    "++++",
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "maze, entrance, expected",
    [
        (EXAMPLE_1, [2, 3], 4),         # book example 1
        (EXAMPLE_2, [1, 0], 7),         # book example 2 (border entrance)
        (EXAMPLE_3, [0, 1], -1),        # only exit = entrance (edge case)
        (["."], [0, 0], -1),            # one cell: it is the entrance
        ([".."], [0, 0], 1),            # neighbor on the border
        (["+.+", "+.+", "+.+"], [1, 1], 1),
        (["...", "...", "..."], [1, 1], 1),
        (["+++", "+.+", "+++"], [1, 1], -1),   # sealed room
        (["....."], [0, 2], 1),         # one row: every cell is border
        (["+.+.+"], [0, 1], -1),        # walls between the open cells
    ],
)
def test_examples(solve, maze, entrance, expected):
    assert solve(maze, entrance) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    maze = list(EXAMPLE_1)
    entrance = [2, 3]
    solve(maze, entrance)
    assert maze == EXAMPLE_1 and entrance == [2, 3]


def networkx_answer(maze, entrance):
    rows, cols = len(maze), len(maze[0])
    g = nx.Graph()
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == ".":
                g.add_node((r, c))
                if r + 1 < rows and maze[r + 1][c] == ".":
                    g.add_edge((r, c), (r + 1, c))
                if c + 1 < cols and maze[r][c + 1] == ".":
                    g.add_edge((r, c), (r, c + 1))
    start = tuple(entrance)
    dist = nx.single_source_shortest_path_length(g, start)
    exits = [d for (r, c), d in dist.items()
             if (r, c) != start
             and (r in (0, rows - 1) or c in (0, cols - 1))]
    return min(exits, default=-1)


def test_random_mazes_agree_with_networkx_and_brute():
    rng = random.Random(1926)
    for _ in range(1500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        maze = ["".join(rng.choice("..+") for _ in range(cols))
                for _ in range(rows)]
        opens = [(r, c) for r in range(rows) for c in range(cols)
                 if maze[r][c] == "."]
        if not opens:
            continue
        entrance = list(rng.choice(opens))
        want = networkx_answer(maze, entrance)
        assert nearest_exit(maze, entrance) == want
        assert nearest_exit_full(maze, entrance) == want


def test_large_maze_is_fast():
    # 500 x 500 open field with the entrance in the middle, plus a
    # long serpentine maze whose only exit is far away.
    n = 500
    field = ["." * n for _ in range(n)]
    assert nearest_exit(field, [250, 250]) == 249
    # Corridors on odd rows, joined at alternating ends: the only
    # way out is to walk every corridor down to the bottom row.
    rows = [list("+" * n) for _ in range(n)]
    for r in range(1, n, 2):
        rows[r][1:n - 1] = "." * (n - 2)
    for r in range(2, n - 1, 2):
        rows[r][n - 2 if r % 4 == 2 else 1] = "."
    maze = ["".join(row) for row in rows]
    start = time.perf_counter()
    got = nearest_exit(maze, [1, 1])
    assert time.perf_counter() - start < 2.0
    assert got == 249 * (n - 1)     # 249 corridors and turns
    assert got == networkx_answer(maze, [1, 1])
