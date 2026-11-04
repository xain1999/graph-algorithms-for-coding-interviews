def find_champion_rows(grid: list[list[int]]) -> int:
    """The team whose row says it beats all n - 1 others."""
    n = len(grid)
    for team in range(n):
        if sum(grid[team]) == n - 1:    # out-degree n - 1
            return team
    return -1
