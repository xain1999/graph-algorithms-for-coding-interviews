def plant_flowers(n: int, paths: list[list[int]]) -> list[int]:
    """Flower type 1-4 per garden, different along every path."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for x, y in paths:
        graph[x - 1].append(y - 1)      # gardens are 1-indexed
        graph[y - 1].append(x - 1)

    flower = [0] * n                    # 0: nothing planted yet
    for garden in range(n):
        used = {flower[nb] for nb in graph[garden]}
        for kind in (1, 2, 3, 4):
            if kind not in used:        # at most 3 types are taken
                flower[garden] = kind
                break
    return flower
