from collections import deque


def alien_order(words: list[str]) -> str:
    """Letters in an order consistent with words, or "" if none."""
    # Every letter is a node, even one that never gets an edge.
    graph: dict[str, list[str]] = {}
    for word in words:
        for ch in word:
            graph.setdefault(ch, [])
    indegree = dict.fromkeys(graph, 0)

    for first, second in zip(words, words[1:]):
        for a, b in zip(first, second):
            if a != b:                  # the first difference decides
                if b not in graph[a]:   # add each edge a -> b once
                    graph[a].append(b)
                    indegree[b] += 1
                break
        else:                           # one word is a prefix
            if len(first) > len(second):
                return ""               # "abc" cannot precede "ab"

    queue = deque(ch for ch in graph if indegree[ch] == 0)
    order: list[str] = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if len(order) < len(graph):
        return ""                       # a cycle among the letters
    return "".join(order)
