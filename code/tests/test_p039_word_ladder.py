import random
import string
import time

import networkx as nx
import pytest

from solutions.p039_word_ladder import ladder_length
from solutions.p039_word_ladder_brute import (
    ladder_length_pairs,
    one_apart,
)

SOLVERS = [ladder_length, ladder_length_pairs]

WORDS_1 = ["load", "goad", "gold", "head", "held", "hold",
           "mead", "meld", "mold"]
WORDS_2 = ["cord", "card", "ward", "warm", "word", "worm", "wore",
           "core", "colt", "bolt"]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "begin, end, words, expected",
    [
        ("lead", "gold", WORDS_1, 4),       # book example 1
        ("cold", "warm", WORDS_2, 5),       # book example 2
        ("mint", "mist", ["mind", "mild", "milt"], 0),  # end missing from dictionary (edge case)
        ("a", "c", ["b", "c"], 2),          # one letter, one step
        ("ab", "ab", ["ab"], 1),            # begin equals end
        ("hot", "dog", ["hot", "dog"], 0),  # in the list, unreachable
        ("hit", "hot", ["hot", "hot"], 2),  # duplicates in the list
        ("lead", "lead", WORDS_1, 0),       # end missing, even if equal
        ("aaa", "bbb", ["aab", "abb", "bbb", "aba", "baa"], 4),
    ],
)
def test_examples(solve, begin, end, words, expected):
    assert solve(begin, end, words) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    words = WORDS_1[:]
    solve("lead", "gold", words)
    assert words == WORDS_1


def test_random_dictionaries_agree_with_networkx():
    rng = random.Random(127)
    for _ in range(600):
        length = rng.randint(1, 3)
        letters = "abc"[: rng.randint(2, 3)]
        def word():
            return "".join(rng.choice(letters) for _ in range(length))
        words = [word() for _ in range(rng.randint(1, 12))]
        begin = word()
        end = rng.choice(words) if rng.random() < 0.9 else word()
        g = nx.Graph()
        nodes = set(words) | {begin}
        g.add_nodes_from(nodes)
        g.add_edges_from((a, b) for a in nodes for b in nodes
                         if one_apart(a, b))
        if end in words and nx.has_path(g, begin, end):
            expected = nx.shortest_path_length(g, begin, end) + 1
        else:
            expected = 0
        for solve in SOLVERS:
            assert solve(begin, end, words) == expected


def test_large_dictionary_is_fast():
    rng = random.Random(5)
    letters = string.ascii_lowercase[:12]
    words = list({"".join(rng.choice(letters) for _ in range(6))
                  for _ in range(30_000)})
    start = time.perf_counter()
    for end in words[:5]:
        ladder_length(words[-1], end, words)
    assert time.perf_counter() - start < 5
