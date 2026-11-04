from collections import deque


class TreeNode:
    """A binary tree node: a value and two optional children."""

    def __init__(self, val: int, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def min_depth(root: TreeNode | None) -> int:
    """Nodes on the shortest root-to-leaf path (0 for no tree)."""
    if root is None:
        return 0
    depth = 0
    queue = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):     # exactly one level
            node = queue.popleft()
            if node.left is None and node.right is None:
                return depth            # first leaf = shallowest
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
    raise AssertionError("unreachable: every tree has a leaf")
