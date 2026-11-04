from collections import deque


def earliest_all_friends_brute(n: int, logs: list[list[int]]) -> int:
    """Try each time in order; BFS over the friendships so far."""
    for t in sorted({log[0] for log in logs}):
        graph: list[list[int]] = [[] for _ in range(n)]
        for time, a, b in logs:
            if time <= t:
                graph[a].append(b)
                graph[b].append(a)
        seen = [False] * n
        seen[0] = True
        queue = deque([0])
        reached = 1
        while queue:
            person = queue.popleft()
            for friend in graph[person]:
                if not seen[friend]:
                    seen[friend] = True
                    reached += 1
                    queue.append(friend)
        if reached == n:
            return t
    return -1
