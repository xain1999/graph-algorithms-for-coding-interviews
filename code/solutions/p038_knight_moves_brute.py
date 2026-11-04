from collections import deque

MOVES = ((1, 2), (2, 1), (2, -1), (1, -2),
         (-1, -2), (-2, -1), (-2, 1), (-1, 2))


def min_knight_moves_unbounded(x: int, y: int) -> int:
    """Plain BFS on the infinite board, in every direction."""
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == (x, y):
            return dist[(cx, cy)]
        for dx, dy in MOVES:
            nxt = (cx + dx, cy + dy)
            if nxt not in dist:
                dist[nxt] = dist[(cx, cy)] + 1
                queue.append(nxt)
    raise AssertionError("every square is reachable")
