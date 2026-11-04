def longest_cycle_brute(edges: list[int]) -> int:
    """From each node, walk up to n steps to see if it comes back."""
    n = len(edges)
    best = -1
    for start in range(n):
        node = edges[start]
        for steps in range(1, n + 1):
            if node == -1:
                break
            if node == start:           # start lies on a cycle
                best = max(best, steps)
                break
            node = edges[node]
    return best
