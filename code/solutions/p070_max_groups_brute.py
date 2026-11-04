from itertools import product


def max_groups_brute(n: int, edges: list[list[int]]) -> int:
    """Try every assignment of groups 1..n; tiny n only."""
    best = -1
    for groups in product(range(1, n + 1), repeat=n):
        m = max(groups)
        if len(set(groups)) != m:       # groups 1..m all used
            continue
        if all(abs(groups[a - 1] - groups[b - 1]) == 1
               for a, b in edges):
            best = max(best, m)
    return best
