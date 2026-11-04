def max_probability_brute(n: int, edges: list[list[int]],
                          succ_prob: list[float], start: int,
                          end: int) -> float:
    """Bellman-Ford with products: relax all edges n - 1 times."""
    best = [0.0] * n
    best[start] = 1.0
    for _ in range(n - 1):
        changed = False
        for (a, b), p in zip(edges, succ_prob):
            for u, v in ((a, b), (b, a)):
                if best[u] * p > best[v]:
                    best[v] = best[u] * p
                    changed = True
        if not changed:
            break
    return best[end]
