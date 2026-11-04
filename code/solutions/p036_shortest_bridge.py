from collections import deque

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def shortest_bridge(grid: list[list[int]]) -> int:
    """Fewest water cells to fill so the two islands touch."""
    rows, cols = len(grid), len(grid[0])
    first = next((r, c) for r in range(rows) for c in range(cols)
                 if grid[r][c] == 1)

    # Phase 1: iterative DFS collects every cell of one island.
    dist = [[-1] * cols for _ in range(rows)]
    dist[first[0]][first[1]] = 0
    stack = [first]
    island = []
    while stack:
        r, c = stack.pop()
        island.append((r, c))
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 1 and dist[nr][nc] == -1):
                dist[nr][nc] = 0
                stack.append((nr, nc))

    # Phase 2: multi-source BFS from all of its cells at once.
    queue = deque(island)
    while queue:
        r, c = queue.popleft()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if dist[nr][nc] != -1:
                continue            # first island, or water seen
            if grid[nr][nc] == 1:
                return dist[r][c]   # touched the other island
            dist[nr][nc] = dist[r][c] + 1   # one more flip
            queue.append((nr, nc))
    raise ValueError("the grid must hold exactly two islands")
