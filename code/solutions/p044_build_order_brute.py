def is_valid_order_brute(n: int, dependencies: list[list[int]],
                         order: list[int]) -> bool:
    """Look up both tasks of every pair by scanning the order."""
    if sorted(order) != list(range(n)):
        return False                    # missing or repeated task
    for a, b in dependencies:
        if order.index(a) >= order.index(b):    # O(n) per lookup
            return False
    return True
