def find_order_brute(n: int,
                     prerequisites: list[list[int]]) -> list[int]:
    """Take every course whose prerequisites are done, in rounds."""
    needs: list[list[int]] = [[] for _ in range(n)]
    for course, pre in prerequisites:
        needs[course].append(pre)

    taken = [False] * n
    order: list[int] = []
    progress = True
    while progress:
        progress = False
        for course in range(n):
            if not taken[course] and all(taken[p]
                                         for p in needs[course]):
                taken[course] = True
                order.append(course)
                progress = True
    return order if len(order) == n else []
