from solutions.p087_distance_k import TreeNode


def distance_k_rec(root: TreeNode, target: TreeNode,
                   k: int) -> list[int]:
    """No parent map; recursive, so only for trees of height < 900."""
    found: list[int] = []

    def collect(node: TreeNode | None, depth: int) -> None:
        """Add the nodes exactly depth levels below node."""
        if node is None or depth < 0:
            return
        if depth == 0:
            found.append(node.val)
            return
        collect(node.left, depth - 1)
        collect(node.right, depth - 1)

    def down_to_target(node: TreeNode | None) -> int:
        """Edges from node down to target, or -1 if not below."""
        if node is None:
            return -1
        if node is target:
            collect(node, k)
            return 0
        for child, other in ((node.left, node.right),
                             (node.right, node.left)):
            d = down_to_target(child)
            if d >= 0:
                d += 1                  # now from node to target
                if d == k:
                    found.append(node.val)
                else:                   # turn into the other side
                    collect(other, k - d - 1)
                return d
        return -1

    down_to_target(root)
    return found
