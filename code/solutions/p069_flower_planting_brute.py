def plant_flowers_brute(n: int, paths: list[list[int]],
                        kinds: int = 4) -> list[int]:
    """Backtracking with `kinds` flower types; [] if none works."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for x, y in paths:
        graph[x - 1].append(y - 1)
        graph[y - 1].append(x - 1)
    flower = [0] * n                    # 0: nothing planted yet

    def plant(garden: int) -> bool:
        if garden == n:
            return True                 # every garden is planted
        for kind in range(1, kinds + 1):
            if all(flower[nb] != kind for nb in graph[garden]):
                flower[garden] = kind
                if plant(garden + 1):
                    return True
        flower[garden] = 0              # undo before going back
        return False

    return flower if plant(0) else []
