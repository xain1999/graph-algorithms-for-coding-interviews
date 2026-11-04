from collections import deque


def one_apart(a: str, b: str) -> bool:
    """True if a and b differ in exactly one position."""
    return sum(x != y for x, y in zip(a, b)) == 1


def ladder_length_pairs(begin: str, end: str,
                        words: list[str]) -> int:
    """Build the graph by comparing every pair, then run BFS."""
    if end not in words:
        return 0
    nodes = list(set(words) | {begin})
    graph: dict[str, list[str]] = {w: [] for w in nodes}
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if one_apart(a, b):
                graph[a].append(b)
                graph[b].append(a)

    dist = {begin: 1}
    queue = deque([begin])
    while queue:
        word = queue.popleft()
        if word == end:
            return dist[word]
        for nxt in graph[word]:
            if nxt not in dist:
                dist[nxt] = dist[word] + 1
                queue.append(nxt)
    return 0
