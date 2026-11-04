def find_all_recipes_brute(recipes: list[str],
                           ingredients: list[list[str]],
                           supplies: list[str]) -> list[str]:
    """Sweep over the recipes until a sweep makes nothing new."""
    available = set(supplies)
    made: list[str] = []
    changed = True
    while changed:
        changed = False
        for recipe, items in zip(recipes, ingredients):
            if recipe not in available and all(
                    item in available for item in items):
                available.add(recipe)
                made.append(recipe)
                changed = True
    return made
