def is_valid_order(n: int, dependencies: list[list[int]],
                   order: list[int]) -> bool:
    """True if order lists every task once and respects every pair."""
    if len(order) != n:
        return False
    pos = [-1] * n                      # pos[task] = index in order
    for i, task in enumerate(order):
        if pos[task] != -1:
            return False                # listed twice
        pos[task] = i

    for a, b in dependencies:           # a must come before b
        if pos[a] >= pos[b]:
            return False
    return True
