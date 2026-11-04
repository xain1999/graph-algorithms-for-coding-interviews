from solutions.p084_nary_depth import Node


def max_depth_dfs(root: Node | None) -> int:
    """Iterative DFS: the stack holds (node, its depth) pairs."""
    if root is None:
        return 0
    best = 0
    stack = [(root, 1)]
    while stack:
        node, depth = stack.pop()
        best = max(best, depth)
        for child in node.children:
            stack.append((child, depth + 1))
    return best
