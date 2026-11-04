from collections import defaultdict, deque


def ladder_length(begin: str, end: str, words: list[str]) -> int:
    """Words in the shortest ladder from begin to end, or 0."""
    if end not in words:
        return 0
    # Bucket every word under each of its wildcard patterns.
    buckets: defaultdict[str, list[str]] = defaultdict(list)
    for word in words:
        for i in range(len(word)):
            buckets[word[:i] + "*" + word[i + 1:]].append(word)

    dist = {begin: 1}                   # begin counts as one word
    queue = deque([begin])
    while queue:
        word = queue.popleft()
        if word == end:
            return dist[word]
        for i in range(len(word)):
            pattern = word[:i] + "*" + word[i + 1:]
            # pop: a bucket is scanned once, then thrown away
            for nxt in buckets.pop(pattern, []):
                if nxt not in dist:
                    dist[nxt] = dist[word] + 1
                    queue.append(nxt)
    return 0
