class Node:
    """A graph node: a label and the list of adjacent nodes."""

    def __init__(self, val: int) -> None:
        self.val = val
        self.neighbors: list[Node] = []


def clone_graph(node: Node | None) -> Node | None:
    """Deep copy of the graph that contains node, by recursive DFS."""
    if node is None:
        return None
    copies: dict[Node, Node] = {}       # original -> its copy

    def copy(old: Node) -> Node:
        if old in copies:               # met before: reuse the copy
            return copies[old]
        new = Node(old.val)
        copies[old] = new               # register BEFORE recursing
        for nxt in old.neighbors:
            new.neighbors.append(copy(nxt))
        return new

    return copy(node)
