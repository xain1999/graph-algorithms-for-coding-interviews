from collections import deque

MOVES = ((1, 2), (2, 1), (2, -1), (1, -2),
         (-1, -2), (-2, -1), (-2, 1), (-1, 2))


def min_knight_moves(x: int, y: int) -> int:
    """Fewest knight moves from (0, 0) to (x, y)."""
    x, y = abs(x), abs(y)           # symmetry: solve in one quadrant
    dist = {(0, 0): 0}
    queue = deque([(0, 0)])
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == (x, y):
            return dist[(cx, cy)]
        for dx, dy in MOVES:
            nx, ny = cx + dx, cy + dy
            # the target's box, widened by 2 on every side
            if (-2 <= nx <= x + 2 and -2 <= ny <= y + 2
                    and (nx, ny) not in dist):
                dist[(nx, ny)] = dist[(cx, cy)] + 1
                queue.append((nx, ny))
    raise AssertionError("every square is reachable")
