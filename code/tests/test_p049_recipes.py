import random
import time

import pytest

from solutions.p049_recipes import find_all_recipes
from solutions.p049_recipes_brute import find_all_recipes_brute

SOLVERS = [find_all_recipes, find_all_recipes_brute]

RECIPES_1 = ["pizza", "dough", "calzone", "sauce"]
INGREDIENTS_1 = [["dough", "sauce", "cheese"], ["flour", "water"],
                 ["dough", "cheese", "ham"], ["tomato"]]
SUPPLIES_1 = ["water", "cheese", "flour", "tomato"]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "recipes, ingredients, supplies, expected",
    [
        # book example 1: calzone needs ham, which nobody has
        (RECIPES_1, INGREDIENTS_1, SUPPLIES_1,
         {"dough", "sauce", "pizza"}),
        # book example 2: a cycle of two recipes, plus one outside it
        (["glaze", "syrup", "toffee"],
         [["syrup", "sugar"], ["glaze", "water"], ["sugar", "butter"]],
         ["sugar", "water", "butter"], {"toffee"}),
        # a chain, given in reverse order (not in book)
        (["d", "c", "b"], [["c"], ["b"], ["a"]], ["a"],
         {"b", "c", "d"}),
        (["x"], [["y"]], [], set()),             # nothing in stock
        (["x"], [["y"]], ["y"], {"x"}),
        # a recipe can list the same ingredient twice
        (["x"], [["y", "y"]], ["y"], {"x"}),
        # a self-loop: a recipe that needs itself
        (["x"], [["x", "y"]], ["y"], set()),
        # a cycle blocks everything that depends on it
        (["a", "b", "c"], [["b"], ["a"], ["a", "s"]], ["s"], set()),
    ],
)
def test_examples(solve, recipes, ingredients, supplies, expected):
    made = solve(recipes, ingredients, supplies)
    assert set(made) == expected and len(made) == len(expected)


def test_example_order():
    assert find_all_recipes(RECIPES_1, INGREDIENTS_1, SUPPLIES_1) == [
        "dough", "sauce", "pizza"]


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    recipes = RECIPES_1[:]
    ingredients = [i[:] for i in INGREDIENTS_1]
    supplies = SUPPLIES_1[:]
    solve(recipes, ingredients, supplies)
    assert recipes == RECIPES_1 and ingredients == INGREDIENTS_1
    assert supplies == SUPPLIES_1


def random_instance(rng: random.Random):
    k = rng.randint(1, 8)
    recipes = [f"r{i}" for i in range(k)]
    basics = [f"s{i}" for i in range(rng.randint(1, 5))]
    names = recipes + basics
    ingredients = [rng.sample(names, rng.randint(1, min(4, len(names))))
                   for _ in recipes]
    supplies = [s for s in basics if rng.random() < 0.7]
    return recipes, ingredients, supplies


def test_made_recipes_are_in_dependency_order():
    rng = random.Random(2115)
    for _ in range(1000):
        recipes, ingredients, supplies = random_instance(rng)
        made = find_all_recipes(recipes, ingredients, supplies)
        have = set(supplies)
        need = dict(zip(recipes, ingredients))
        for recipe in made:              # every step uses known items
            assert all(item in have for item in need[recipe])
            have.add(recipe)


def test_random_against_brute_force():
    rng = random.Random(49)
    for _ in range(2000):
        recipes, ingredients, supplies = random_instance(rng)
        fast = find_all_recipes(recipes, ingredients, supplies)
        slow = find_all_recipes_brute(recipes, ingredients, supplies)
        assert sorted(fast) == sorted(slow)


def test_long_chain_is_fast():
    # Recipe i needs recipe i + 1, listed so that the brute force's
    # sweeps make only one recipe each: about n^2 / 2 checks for it.
    n = 3000
    recipes = [f"r{i}" for i in range(n)]
    ingredients = [[f"r{i + 1}"] for i in range(n - 1)] + [["salt"]]
    start = time.perf_counter()
    made = find_all_recipes(recipes, ingredients, ["salt"])
    assert made == recipes[::-1]
    assert time.perf_counter() - start < 1.0


def test_wide_instance_is_fast():
    n = 10_000
    recipes = [f"r{i}" for i in range(n)]
    ingredients = [[f"s{(i + j) % 100}" for j in range(5)]
                   + ([f"r{i - 1}"] if i else []) for i in range(n)]
    supplies = [f"s{j}" for j in range(100)]
    start = time.perf_counter()
    assert len(find_all_recipes(recipes, ingredients, supplies)) == n
    assert time.perf_counter() - start < 1.0
