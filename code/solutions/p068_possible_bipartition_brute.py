def possible_bipartition_brute(n: int,
                               dislikes: list[list[int]]) -> bool:
    """Backtracking: place people 1..n one at a time."""
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    group = [0] * (n + 1)               # 0: not placed, else 1 or 2

    def place(person: int) -> bool:
        if person > n:
            return True                 # everyone has a group
        for g in (1, 2):
            if all(group[o] != g for o in graph[person]):
                group[person] = g
                if place(person + 1):
                    return True
                group[person] = 0       # undo, try the other group
        return False

    return place(1)
