from collections import deque
from collections.abc import Iterator


def neighbors(state: str) -> Iterator[str]:
    """The eight positions one turn away from state."""
    for i in range(4):
        digit = int(state[i])
        for step in (1, -1):
            turned = (digit + step) % 10    # 9 + 1 wraps to 0
            yield state[:i] + str(turned) + state[i + 1:]


def open_lock(deadends: list[str], target: str) -> int:
    """Fewest turns from "0000" to target, or -1."""
    dead = set(deadends)
    if "0000" in dead:
        return -1                       # jammed before the first turn
    if target == "0000":
        return 0
    seen = {"0000"} | dead              # dead ends are never entered
    queue = deque(["0000"])
    turns = 0
    while queue:
        turns += 1
        for _ in range(len(queue)):     # one layer = one more turn
            state = queue.popleft()
            for nxt in neighbors(state):
                if nxt in seen:
                    continue
                if nxt == target:
                    return turns
                seen.add(nxt)           # mark when enqueued
                queue.append(nxt)
    return -1
