def time_to_inform_memo(n: int, head: int, manager: list[int],
                        inform_time: list[int]) -> int:
    """Climb the chain, but stop at the first known minute."""
    heard = [-1] * n                    # -1 means not known yet
    heard[head] = 0
    for emp in range(n):
        chain = []
        node = emp
        while heard[node] == -1:        # climb to a known employee
            chain.append(node)
            node = manager[node]
        for person in reversed(chain):  # fill in top-down
            boss = manager[person]
            heard[person] = heard[boss] + inform_time[boss]
    return max(heard)
