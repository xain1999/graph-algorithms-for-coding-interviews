import random
import string
import time

import pytest

from solutions.p050_alien_dictionary import alien_order
from solutions.p050_alien_dictionary_brute import (
    alien_order_brute,
    is_sorted_by,
)
from solutions.p050_alien_dictionary_dfs import alien_order_dfs

SOLVERS = [alien_order, alien_order_dfs, alien_order_brute]

WORDS_1 = ["cone", "cent", "cane", "eat", "ate", "ten", "tent"]


def is_valid(words: list[str], order: str) -> bool:
    """A valid answer uses each letter once and sorts the words."""
    letters = set("".join(words))
    return (len(order) == len(letters) and set(order) == letters
            and is_sorted_by(words, order))


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "words",
    [
        WORDS_1,                            # book example 1
        ["ab", "abc"],                      # a prefix first is fine
        ["zz"],                             # one word, one letter
        ["k", "k", "k"],                    # equal words
        ["xy", "yx"],                       # x before y; y is free
        ["b", "a", "ab"],                   # "a" before "ab" is fine
    ],
)
def test_valid_orders(solve, words):
    order = solve(words)
    assert is_valid(words, order)


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "words",
    [
        ["rot", "tor", "orb", "rib"],       # book example 2: r<t<o<r
        ["dome", "dot", "do"],              # prefix, not in book
        ["abc", "ab"],                      # the classic prefix trap
        ["a", "b", "a"],                    # a < b and b < a
        ["ba", "bb", "aa", "ab"],           # cycle a < b < a
    ],
)
def test_impossible(solve, words):
    assert solve(words) == ""


def test_example_1_answer():
    assert alien_order(WORDS_1) == "coneat"


def test_example_1_has_twelve_answers():
    from itertools import permutations
    valid = ["".join(p) for p in permutations("aceont")
             if is_sorted_by(WORDS_1, "".join(p))]
    assert len(valid) == 12 and "coneat" in valid
    assert alien_order_dfs(WORDS_1) in valid


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    words = WORDS_1[:]
    solve(words)
    assert words == WORDS_1


def random_sorted_words(rng: random.Random, alphabet: str):
    rank = {ch: i for i, ch in enumerate(alphabet)}
    words = ["".join(rng.choice(alphabet)
                     for _ in range(rng.randint(1, 4)))
             for _ in range(rng.randint(1, 7))]
    return sorted(words, key=lambda w: [rank[ch] for ch in w])


def test_random_sorted_lists_give_valid_orders():
    rng = random.Random(269)
    for _ in range(1500):
        k = rng.randint(1, 6)
        alphabet = "".join(rng.sample(string.ascii_lowercase, k))
        words = random_sorted_words(rng, alphabet)
        for solve in SOLVERS:
            assert is_valid(words, solve(words))


def test_random_lists_agree_on_possibility():
    rng = random.Random(50)
    for _ in range(1500):
        letters = "abcde"[:rng.randint(1, 5)]
        words = ["".join(rng.choice(letters)
                         for _ in range(rng.randint(1, 3)))
                 for _ in range(rng.randint(1, 5))]
        expected = alien_order_brute(words) != ""
        for solve in (alien_order, alien_order_dfs):
            order = solve(words)
            assert (order != "") == expected
            if order:
                assert is_valid(words, order)


def test_large_input_is_fast():
    # 26 letters, 2000 long words sorted by a shuffled alphabet.
    rng = random.Random(7)
    alphabet = "".join(rng.sample(string.ascii_lowercase, 26))
    rank = {ch: i for i, ch in enumerate(alphabet)}
    words = ["".join(rng.choice(alphabet) for _ in range(50))
             for _ in range(2000)]
    words.sort(key=lambda w: [rank[ch] for ch in w])
    start = time.perf_counter()
    for solve in (alien_order, alien_order_dfs):
        assert is_valid(words, solve(words))
    assert time.perf_counter() - start < 1.0


def test_long_chain_dfs_is_iterative():
    # Every letter of a 26-letter chain, one adjacent pair per edge.
    alphabet = string.ascii_lowercase
    words = [ch * 3 for ch in alphabet]
    assert alien_order(words) == alphabet
    assert alien_order_dfs(words) == alphabet
