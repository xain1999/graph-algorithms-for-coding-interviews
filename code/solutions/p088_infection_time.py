from collections import defaultdict, deque


class TreeNode:
    """A binary tree node: a value and two optional children."""

    def __init__(self, val: int, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None) -> None:
        self.val = val
        self.left = left
        self.right = right


def amount_of_time(root: TreeNode, start: int) -> int:
    """Minutes until the infection from start reaches every node."""
    graph: dict[int, list[int]] = defaultdict(list)
    stack = [root]
    while stack:                        # tree -> undirected graph
        node = stack.pop()
        for child in (node.left, node.right):
            if child is not None:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                stack.append(child)

    seen = {start}
    queue = deque([start])
    minutes = -1
    while queue:                        # one BFS layer per minute
        minutes += 1
        for _ in range(len(queue)):
            cur = queue.popleft()
            for nxt in graph[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
    return minutes
