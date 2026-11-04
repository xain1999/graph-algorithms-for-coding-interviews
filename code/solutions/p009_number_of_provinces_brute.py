def count_provinces_brute(is_connected: list[list[int]]) -> int:
    """Work out who reaches whom, then count the distinct rows."""
    n = len(is_connected)
    reach = [[x == 1 for x in row] for row in is_connected]
    for k in range(n):              # allow k as a stopover
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    # every city in a province now has the same row
    return len({tuple(row) for row in reach})
