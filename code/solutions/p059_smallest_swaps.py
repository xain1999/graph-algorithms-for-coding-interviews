from collections import defaultdict


def smallest_string_with_swaps(s: str,
                               pairs: list[list[int]]) -> str:
    """Sort the letters inside each group of swappable indices."""
    parent = list(range(len(s)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    for i, j in pairs:
        parent[find(i)] = find(j)

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(s)):
        groups[find(i)].append(i)       # indices come out sorted

    result = [""] * len(s)
    for indices in groups.values():
        letters = sorted(s[i] for i in indices)
        for i, letter in zip(indices, letters):
            result[i] = letter          # smallest letter first
    return "".join(result)
