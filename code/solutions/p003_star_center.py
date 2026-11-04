def find_center(edges: list[list[int]]) -> int:
    """The center is the one node the first two edges share."""
    a, b = edges[0]
    c, d = edges[1]
    return a if a in (c, d) else b
