from solutions.p028_min_depth import TreeNode


def min_depth_dfs(root: TreeNode | None) -> int:
    """Recursive DFS: visit every leaf, keep the shallowest."""
    if root is None:
        return 0
    if root.left is None:       # all leaves are on the right
        return 1 + min_depth_dfs(root.right)
    if root.right is None:      # all leaves are on the left
        return 1 + min_depth_dfs(root.left)
    return 1 + min(min_depth_dfs(root.left),
                   min_depth_dfs(root.right))
