import math
from collections import defaultdict


def calc_equation_wide(equations: list[list[str]],
                       values: list[float],
                       queries: list[list[str]]) -> list[float]:
    """calc_equation for chains of any length: each running product
    is kept as mantissa * 2**exponent, so it cannot overflow or
    underflow on the way. Only an answer outside the float range
    itself is lost."""
    graph: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for (a, b), ratio in zip(equations, values):
        graph[a].append((b, ratio))
        graph[b].append((a, 1 / ratio))

    def ratio_of(start: str, target: str) -> float:
        if start not in graph or target not in graph:
            return -1.0
        stack = [(start, 1.0, 0)]         # (node, mantissa, exponent)
        seen = {start}
        while stack:
            node, mant, exp = stack.pop()
            if node == target:
                try:
                    return math.ldexp(mant, exp)
                except OverflowError:
                    return math.inf       # the answer is too big
            for nxt, ratio in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    m, e = math.frexp(mant * ratio)
                    stack.append((nxt, m, exp + e))
        return -1.0

    return [ratio_of(a, b) for a, b in queries]
