from collections import deque


def flatten(board: list[list[int]]) -> list[int]:
    """jump[s] for squares 1..n*n, in the order they are numbered."""
    jump = [-1]                         # index 0 is unused
    for band, row in enumerate(reversed(board)):  # bottom row first
        jump.extend(row if band % 2 == 0 else reversed(row))
    return jump


def snakes_and_ladders_flat(board: list[list[int]]) -> int:
    """The same BFS on a flattened board: no coordinates at all."""
    jump = flatten(board)
    goal = len(jump) - 1
    dist = [-1] * (goal + 1)
    dist[1] = 0
    queue = deque([1])
    while queue:
        square = queue.popleft()
        for nxt in range(square + 1, min(square + 6, goal) + 1):
            if jump[nxt] != -1:
                nxt = jump[nxt]
            if dist[nxt] == -1:
                dist[nxt] = dist[square] + 1
                queue.append(nxt)
    return dist[goal]
