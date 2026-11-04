from functools import cache


def all_paths_memo(graph: list[list[int]]) -> list[list[int]]:
    """Paths from each node to the target, built once per node."""
    target = len(graph) - 1

    @cache
    def paths_from(node: int) -> tuple[tuple[int, ...], ...]:
        if node == target:
            return ((target,),)
        return tuple((node,) + rest
                     for nxt in graph[node]
                     for rest in paths_from(nxt))

    return [list(p) for p in paths_from(0)]
