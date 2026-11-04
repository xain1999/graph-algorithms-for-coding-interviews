from collections import defaultdict


def calc_equation(equations: list[list[str]], values: list[float],
                  queries: list[list[str]]) -> list[float]:
    """Answer each query a/b by multiplying ratios along a path."""
    graph: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for (a, b), ratio in zip(equations, values):
        graph[a].append((b, ratio))       # a / b = ratio
        graph[b].append((a, 1 / ratio))   # b / a = 1 / ratio

    def ratio_of(start: str, target: str) -> float:
        if start not in graph or target not in graph:
            return -1.0                   # unknown variable
        stack = [(start, 1.0)]            # (node, start / node)
        seen = {start}
        while stack:
            node, product = stack.pop()
            if node == target:
                return product
            for nxt, ratio in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, product * ratio))
        return -1.0                       # different components

    return [ratio_of(a, b) for a, b in queries]
