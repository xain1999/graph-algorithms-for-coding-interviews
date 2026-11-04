from collections import deque


def smallest_swaps_brute(s: str, pairs: list[list[int]]) -> str:
    """BFS over every string the swaps can reach; keep the least."""
    seen = {s}
    queue = deque([s])
    while queue:
        word = queue.popleft()
        for i, j in pairs:
            chars = list(word)
            chars[i], chars[j] = chars[j], chars[i]
            nxt = "".join(chars)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return min(seen)
