def minimum_time_brute(n: int, relations: list[list[int]],
                       time: list[int]) -> int:
    """Recompute every course's finish time from scratch."""
    prereqs: list[list[int]] = [[] for _ in range(n)]
    for before, after in relations:
        prereqs[after - 1].append(before - 1)

    def finish(course: int) -> int:
        # No memo: a shared prerequisite is recomputed every time.
        ready = max((finish(p) for p in prereqs[course]), default=0)
        return ready + time[course]

    return max(finish(c) for c in range(n))
