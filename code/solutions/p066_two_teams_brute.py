from itertools import product


def split_into_teams_brute(n: int,
                           rivals: list[list[int]]) -> list[int]:
    """Try all 2^n splits; return the first valid one, or []."""
    for team in product((0, 1), repeat=n):
        if all(team[a] != team[b] for a, b in rivals):
            return list(team)
    return []
