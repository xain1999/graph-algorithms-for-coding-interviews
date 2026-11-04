from collections import deque

from solutions.p010_clone_graph import Node


def clone_graph_bfs(node: Node | None) -> Node | None:
    """Same deep copy with BFS: no recursion, any depth."""
    if node is None:
        return None
    copies: dict[Node, Node] = {node: Node(node.val)}
    queue = deque([node])
    while queue:
        old = queue.popleft()
        for nxt in old.neighbors:
            if nxt not in copies:       # first sighting: copy it
                copies[nxt] = Node(nxt.val)
                queue.append(nxt)
            copies[old].neighbors.append(copies[nxt])
    return copies[node]
