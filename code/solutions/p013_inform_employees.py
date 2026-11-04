def time_to_inform(n: int, head: int, manager: list[int],
                   inform_time: list[int]) -> int:
    """Minutes until every employee has heard the news."""
    reports: list[list[int]] = [[] for _ in range(n)]
    for emp, boss in enumerate(manager):
        if boss != -1:
            reports[boss].append(emp)   # edge boss -> emp

    longest = 0
    stack = [(head, 0)]                 # (employee, minute heard)
    while stack:
        emp, minute = stack.pop()
        longest = max(longest, minute)
        passed_on = minute + inform_time[emp]
        for report in reports[emp]:     # a tree: no visited set
            stack.append((report, passed_on))
    return longest
