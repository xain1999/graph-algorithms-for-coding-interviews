from collections import deque
from collections.abc import Callable, Hashable, Iterable
from typing import TypeVar

Node = TypeVar("Node", bound=Hashable)


def bfs_distances(
    starts: Iterable[Node],
    neighbors: Callable[[Node], Iterable[Node]],
) -> dict[Node, int]:
    """Fewest edges from the nearest start to each reachable node."""
    dist = {s: 0 for s in starts}       # one start or many: same code
    queue = deque(dist)
    while queue:
        node = queue.popleft()
        for nxt in neighbors(node):
            if nxt not in dist:         # first visit = shortest
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist
