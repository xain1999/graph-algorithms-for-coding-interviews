from solutions.p088_infection_time import TreeNode


def amount_of_time_brute(root: TreeNode, start: int) -> int:
    """Simulate minute by minute, rescanning every edge each time."""
    edges: list[tuple[int, int]] = []
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child is not None:
                edges.append((node.val, child.val))
                stack.append(child)

    infected = {start}
    minutes = 0
    while True:
        # Snapshot first: nodes infected now spread from next minute.
        new = {b for a, b in edges if a in infected} | {
            a for a, b in edges if b in infected}
        new -= infected
        if not new:
            return minutes
        infected |= new
        minutes += 1
