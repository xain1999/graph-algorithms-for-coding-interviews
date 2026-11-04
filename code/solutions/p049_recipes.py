from collections import defaultdict, deque


def find_all_recipes(recipes: list[str], ingredients: list[list[str]],
                     supplies: list[str]) -> list[str]:
    """Every recipe that can be made, in the order it gets made."""
    # edge item -> recipe for every ingredient the recipe needs
    needed_by: defaultdict[str, list[str]] = defaultdict(list)
    missing: dict[str, int] = {}        # in-degree of each recipe
    for recipe, items in zip(recipes, ingredients):
        missing[recipe] = len(items)
        for item in items:
            needed_by[item].append(recipe)

    queue = deque(supplies)             # supplies are ready at once
    made: list[str] = []
    while queue:
        item = queue.popleft()
        for recipe in needed_by[item]:
            missing[recipe] -= 1
            if missing[recipe] == 0:    # its last ingredient arrived
                made.append(recipe)
                queue.append(recipe)
    return made
