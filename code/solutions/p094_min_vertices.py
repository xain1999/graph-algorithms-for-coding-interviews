def find_smallest_set_of_vertices(
        n: int, edges: list[list[int]]) -> list[int]:
    """Nodes with in-degree 0: exactly those no other node reaches."""
    has_incoming = [False] * n
    for _, to in edges:
        has_incoming[to] = True
    return [node for node in range(n) if not has_incoming[node]]
