def find_champion(grid: list[list[int]]) -> int:
    """Knockout: the current candidate meets every team once."""
    champion = 0
    for team in range(1, len(grid)):
        if grid[team][champion] == 1:   # team beats the candidate
            champion = team
    return champion
