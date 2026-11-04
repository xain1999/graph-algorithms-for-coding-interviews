from solutions.p034_open_lock import neighbors


def open_lock_bidirectional(deadends: list[str], target: str) -> int:
    """Grow layers from both ends until they touch."""
    dead = set(deadends)
    if "0000" in dead or target in dead:
        return -1
    if target == "0000":
        return 0
    front, back = {"0000"}, {target}
    seen = {"0000", target} | dead
    turns = 0
    while front and back:
        if len(front) > len(back):      # always grow the smaller side
            front, back = back, front
        turns += 1
        layer = set()
        for state in front:
            for nxt in neighbors(state):
                if nxt in back:
                    return turns        # the two searches meet
                if nxt not in seen:
                    seen.add(nxt)
                    layer.add(nxt)
        front = layer
    return -1
