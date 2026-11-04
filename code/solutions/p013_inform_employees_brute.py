def time_to_inform_brute(n: int, head: int, manager: list[int],
                         inform_time: list[int]) -> int:
    """Walk up the chain of command from every employee."""
    longest = 0
    for emp in range(n):
        minute = 0
        boss = manager[emp]
        while boss != -1:               # climb until past the head
            minute += inform_time[boss]
            boss = manager[boss]
        longest = max(longest, minute)
    return longest
