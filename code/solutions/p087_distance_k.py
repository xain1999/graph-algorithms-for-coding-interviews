from collections import deque


class TreeNode:
    """A binary tree node: a value and two optional children."""

    def __init__(self, val: int, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def distance_k(root: TreeNode, target: TreeNode,
               k: int) -> list[int]:
    """Values of all nodes exactly k edges away from target."""
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    queue = deque([root])
    while queue:                        # pass 1: record parents
        node = queue.popleft()
        for child in (node.left, node.right):
            if child is not None:
                parent[child] = node
                queue.append(child)

    seen = {target}
    queue = deque([target])
    for _ in range(k):                  # pass 2: k layers of BFS
        for _ in range(len(queue)):
            node = queue.popleft()
            for nxt in (node.left, node.right, parent[node]):
                if nxt is not None and nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return [node.val for node in queue]
