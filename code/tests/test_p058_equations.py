import itertools
import random
import time

import pytest

from solutions.p058_equations import equations_possible
from solutions.p058_equations_brute import equations_possible_brute

SOLVERS = [equations_possible, equations_possible_brute]

EXAMPLE_1 = ["m==n", "k!=p", "n==o", "r==k", "p==q", "o!=q", "s==r"]
EXAMPLE_2 = EXAMPLE_1 + ["q==m"]
TRAP = ["p!=s", "p==q", "r==s", "q==r"]     # fools a single pass


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "equations, expected",
    [
        (EXAMPLE_1, True),                  # book example 1
        (EXAMPLE_2, False),                 # book example 2
        (["u!=v", "v!=w", "w==u"], True),   # a pitfall in the book
        (["z!=z"], False),
        (TRAP, False),                      # single-pass trap
        (["a==a"], True),
        (["a!=b"], True),
        (["a==b", "b!=a"], False),
        (["c!=d", "d==e", "e!=c"], True),   # != is not transitive
        (["x==y", "y!=z", "z==w", "w==x"], False),
    ],
)
def test_examples(solve, equations, expected):
    assert solve(equations) == expected


def single_pass(equations):
    """The broken one-pass version described in the book."""
    parent = list(range(26))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for eq in equations:
        a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
        if eq[1] == "=":
            parent[find(a)] = find(b)
        elif find(a) == find(b):
            return False
    return True


def test_single_pass_is_fooled_by_the_trap():
    assert single_pass(TRAP) is True
    assert equations_possible(TRAP) is False


def by_assignment(equations):
    """Try every assignment of 3 values to the letters used."""
    letters = sorted({eq[0] for eq in equations}
                     | {eq[3] for eq in equations})
    for values in itertools.product(range(3), repeat=len(letters)):
        val = dict(zip(letters, values))
        if all((val[e[0]] == val[e[3]]) == (e[1] == "=")
               for e in equations):
            return True
    return False


def test_random_agree_with_assignments():
    # With at most two "!=" the groups that must differ form a
    # forest, so three values are always enough when any work.
    rng = random.Random(990)
    for _ in range(800):
        letters = "abcdef"[:rng.randint(1, 6)]
        eqs = [rng.choice(letters) + "==" + rng.choice(letters)
               for _ in range(rng.randint(0, 6))]
        eqs += [rng.choice(letters) + "!=" + rng.choice(letters)
                for _ in range(rng.randint(0, 2))]
        if not eqs:
            continue
        rng.shuffle(eqs)
        expected = by_assignment(eqs)
        assert equations_possible(eqs) == expected
        assert equations_possible_brute(eqs) == expected


def test_does_not_mutate_input():
    eqs = EXAMPLE_2[:]
    equations_possible(eqs)
    assert eqs == EXAMPLE_2


def test_large_input_is_fast():
    rng = random.Random(1)
    letters = "abcdefghijklmnopqrstuvwxyz"
    eqs = [rng.choice(letters) + rng.choice(("==", "!="))
           + rng.choice(letters) for _ in range(10**4)]
    start = time.perf_counter()
    equations_possible(eqs)
    assert time.perf_counter() - start < 0.5
