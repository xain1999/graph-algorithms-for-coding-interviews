def calc_equation_brute(equations: list[list[str]],
                        values: list[float],
                        queries: list[list[str]]) -> list[float]:
    """Derive every possible ratio first, then look queries up."""
    known: dict[tuple[str, str], float] = {}
    names: set[str] = set()
    for (a, b), ratio in zip(equations, values):
        names.update((a, b))
        known[a, a] = known[b, b] = 1.0
        known[a, b] = ratio
        known[b, a] = 1 / ratio

    # Floyd-Warshall style: allow k as a middle variable.
    for k in names:
        for i in names:
            if (i, k) not in known:
                continue
            for j in names:
                if (k, j) in known and (i, j) not in known:
                    known[i, j] = known[i, k] * known[k, j]

    return [known.get((a, b), -1.0) for a, b in queries]
