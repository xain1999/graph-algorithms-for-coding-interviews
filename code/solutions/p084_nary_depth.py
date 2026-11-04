from collections import deque


class Node:
    """An N-ary tree node: a value and a list of children."""

    def __init__(self, val: int,
                 children: "list[Node] | None" = None) -> None:
        self.val = val
        self.children = children if children is not None else []


def max_depth(root: Node | None) -> int:
    """Nodes on the longest root-to-leaf path (0 for no tree)."""
    if root is None:
        return 0
    depth = 0
    queue = deque([root])
    while queue:
        depth += 1                      # one more level reached
        for _ in range(len(queue)):     # exactly the current level
            node = queue.popleft()
            queue.extend(node.children)
    return depth
