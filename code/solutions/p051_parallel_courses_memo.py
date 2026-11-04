def minimum_time_memo(n: int, relations: list[list[int]],
                      time: list[int]) -> int:
    """Memoized DFS over prerequisites (recursion depth = chain)."""
    prereqs: list[list[int]] = [[] for _ in range(n)]
    for before, after in relations:
        prereqs[after - 1].append(before - 1)

    memo = [-1] * n                     # -1 means not computed yet

    def finish(course: int) -> int:
        if memo[course] == -1:
            ready = max((finish(p) for p in prereqs[course]),
                        default=0)
            memo[course] = ready + time[course]
        return memo[course]

    return max(finish(c) for c in range(n))
