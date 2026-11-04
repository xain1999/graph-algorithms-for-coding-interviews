from templates.bfs_shortest import bfs_distances

from solutions.p033_nearest_exit import DIRECTIONS


def nearest_exit_full(maze: list[str], entrance: list[int]) -> int:
    """Measure every reachable cell, then pick the closest exit."""
    rows, cols = len(maze), len(maze[0])
    start = (entrance[0], entrance[1])

    def neighbors(cell: tuple[int, int]):
        r, c = cell
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] == "."):
                yield nr, nc

    dist = bfs_distances([start], neighbors)
    exits = [d for (r, c), d in dist.items()
             if (r, c) != start
             and (r in (0, rows - 1) or c in (0, cols - 1))]
    return min(exits, default=-1)
