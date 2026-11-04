import random
import time

import networkx as nx
import pytest

from solutions.p011_all_paths import all_paths
from solutions.p011_all_paths_bfs import all_paths_bfs
from solutions.p011_all_paths_memo import all_paths_memo

SOLVERS = [all_paths, all_paths_bfs, all_paths_memo]

EXAMPLE_1 = [[1, 2], [3, 4], [3], [4, 5], [5], []]
EXAMPLE_2 = [[1, 2, 3], [2, 3], [3], []]
EXAMPLE_3 = [[1, 2], [4], [3], [], []]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "graph, expected",
    [
        # book example 1, in the order the DFS finds them
        (EXAMPLE_1, [[0, 1, 3, 4, 5], [0, 1, 3, 5], [0, 1, 4, 5],
                     [0, 2, 3, 4, 5], [0, 2, 3, 5]]),
        # book example 2: every node points to every later node
        (EXAMPLE_2, [[0, 1, 2, 3], [0, 1, 3], [0, 2, 3], [0, 3]]),
        # former book example 3: the branch through 2 is a dead end
        (EXAMPLE_3, [[0, 1, 4]]),
        ([[1], []], [[0, 1]]),                  # smallest graph
        ([[], []], []),                         # target unreachable
        ([[1], [], []], []),
        ([[2], [2], []], [[0, 2]]),             # node 1 never visited
        ([[1], [2], [3], []], [[0, 1, 2, 3]]),  # a single chain
    ],
)
def test_examples(solve, graph, expected):
    if solve is all_paths_bfs:          # BFS finds short paths first
        assert sorted(solve(graph)) == sorted(expected)
    else:
        assert solve(graph) == expected


def all_paths_with_seen(graph):
    """The mistake shown in the book: DFS with a visited set."""
    target = len(graph) - 1
    paths, path, seen = [], [0], {0}

    def extend(node):
        if node == target:
            paths.append(path[:])
            return
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                path.append(nxt)
                extend(nxt)
                path.pop()

    extend(0)
    return paths


def test_visited_set_loses_paths():
    # The claim in the text: only the first path survives.
    assert all_paths_with_seen(EXAMPLE_1) == [[0, 1, 3, 4, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    graph = [row[:] for row in EXAMPLE_1]
    solve(graph)
    assert graph == EXAMPLE_1


def random_dag(rng: random.Random) -> list[list[int]]:
    n = rng.randint(2, 9)
    p = rng.choice((0.2, 0.4, 0.7))
    graph = [[v for v in range(u + 1, n) if rng.random() < p]
             for u in range(n)]
    for nbrs in graph:
        rng.shuffle(nbrs)
    # relabel the middle nodes so edges do not always go up
    middle = list(range(1, n - 1))
    rng.shuffle(middle)
    label = [0] + middle + [n - 1]
    relabeled = [[] for _ in range(n)]
    for u, nbrs in enumerate(graph):
        relabeled[label[u]] = [label[v] for v in nbrs]
    return relabeled


def test_random_dags_agree_with_networkx():
    rng = random.Random(797)
    for _ in range(800):
        graph = random_dag(rng)
        n = len(graph)
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        for u, nbrs in enumerate(graph):
            g.add_edges_from((u, v) for v in nbrs)
        assert nx.is_directed_acyclic_graph(g)
        expected = sorted(nx.all_simple_paths(g, 0, n - 1))
        got = all_paths(graph)
        assert sorted(got) == expected
        assert all_paths_memo(graph) == got     # same order, too
        assert sorted(all_paths_bfs(graph)) == expected


def complete_dag(n: int) -> list[list[int]]:
    return [list(range(u + 1, n)) for u in range(n)]


def test_worst_case_count():
    # Every subset of the n - 2 middle nodes gives one path.
    for n in range(2, 12):
        assert len(all_paths(complete_dag(n))) == 2 ** (n - 2)


@pytest.mark.parametrize("solve", SOLVERS)
def test_large_output_is_fast(solve):
    start = time.perf_counter()
    paths = solve(complete_dag(18))
    assert len(paths) == 2 ** 16
    assert time.perf_counter() - start < 3.0


def diamond_ladder(k: int) -> list[list[int]]:
    """0 -> target directly, plus a chain of k diamonds that dead-ends."""
    n = 3 * k + 3
    graph: list[list[int]] = [[] for _ in range(n)]
    graph[0] = [1, n - 1]
    a = 1
    for _ in range(k):
        graph[a] = [a + 1, a + 2]
        graph[a + 1] = [a + 3]
        graph[a + 2] = [a + 3]
        a += 3
    return graph


def test_counts_in_text():
    # Calls made by plain backtracking on the dead-end example.
    graph = diamond_ladder(20)
    assert len(graph) == 63
    calls = 0

    def extend(node):
        nonlocal calls
        calls += 1
        for nxt in graph[node]:
            if node != len(graph) - 1:
                extend(nxt)

    extend(0)
    assert calls == 2 ** 22 - 1
    assert all_paths(graph) == [[0, 62]]


def test_memo_skips_dead_ends_fast():
    graph = diamond_ladder(100)         # 2**100 dead-end walks
    start = time.perf_counter()
    assert all_paths_memo(graph) == [[0, len(graph) - 1]]
    assert time.perf_counter() - start < 1.0
