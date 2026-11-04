def eventual_safe_nodes_brute(graph: list[list[int]]) -> list[int]:
    """Safe means: no node reachable from here lies on a cycle."""
    n = len(graph)

    def reachable(start: int) -> set[int]:
        """Nodes reachable from start in one or more steps."""
        seen: set[int] = set()
        stack = list(graph[start])
        while stack:
            node = stack.pop()
            if node not in seen:
                seen.add(node)
                stack.extend(graph[node])
        return seen

    reach = [reachable(v) for v in range(n)]
    on_cycle = [v in reach[v] for v in range(n)]
    return [v for v in range(n)
            if not on_cycle[v] and not any(on_cycle[u]
                                           for u in reach[v])]
