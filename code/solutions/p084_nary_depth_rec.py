from solutions.p084_nary_depth import Node


def max_depth_rec(root: Node | None) -> int:
    """Recursive DFS; Python's recursion limit caps the depth."""
    if root is None:
        return 0
    return 1 + max((max_depth_rec(c) for c in root.children),
                   default=0)
