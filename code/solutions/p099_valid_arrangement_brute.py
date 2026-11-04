def valid_arrangement_brute(
        pairs: list[list[int]]) -> list[list[int]]:
    """Backtracking: extend the chain with any unused fitting pair.

    Exponential in the worst case; recursion depth len(pairs).
    """
    used = [False] * len(pairs)
    chain: list[list[int]] = []

    def extend() -> bool:
        if len(chain) == len(pairs):
            return True
        for i, (a, b) in enumerate(pairs):
            if used[i] or (chain and chain[-1][1] != a):
                continue
            used[i] = True
            chain.append([a, b])
            if extend():
                return True
            chain.pop()
            used[i] = False
        return False

    extend()
    return chain
