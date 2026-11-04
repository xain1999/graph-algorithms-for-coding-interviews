def remove_stones_brute(stones: list[list[int]]) -> int:
    """DFS that tests every pair of stones for a shared line."""
    n = len(stones)
    seen = [False] * n
    groups = 0
    for start in range(n):
        if seen[start]:
            continue
        groups += 1                     # a new group of stones
        seen[start] = True
        stack = [start]
        while stack:
            row, col = stones[stack.pop()]
            for other in range(n):      # every stone is a candidate
                r, c = stones[other]
                if not seen[other] and (r == row or c == col):
                    seen[other] = True
                    stack.append(other)
    return n - groups                   # one stone stays per group
