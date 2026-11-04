from itertools import permutations


def is_sorted_by(words: list[str], order: str) -> bool:
    """True if words are sorted under the given alphabet."""
    rank = {ch: i for i, ch in enumerate(order)}
    keys = [[rank[ch] for ch in word] for word in words]
    # Python compares lists element by element; a prefix comes first.
    return all(a <= b for a, b in zip(keys, keys[1:]))


def alien_order_brute(words: list[str]) -> str:
    """Try every ordering of the letters that appear."""
    letters = sorted(set("".join(words)))
    for perm in permutations(letters):
        order = "".join(perm)
        if is_sorted_by(words, order):
            return order
    return ""
