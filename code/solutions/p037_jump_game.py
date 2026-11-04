from collections import deque


def can_reach(arr: list[int], start: int) -> bool:
    """True if a jump sequence from start lands on a value 0."""
    n = len(arr)
    seen = [False] * n
    seen[start] = True
    queue = deque([start])
    while queue:
        i = queue.popleft()
        if arr[i] == 0:
            return True
        for j in (i + arr[i], i - arr[i]):  # the two jumps
            if 0 <= j < n and not seen[j]:
                seen[j] = True              # mark when enqueued
                queue.append(j)
    return False
