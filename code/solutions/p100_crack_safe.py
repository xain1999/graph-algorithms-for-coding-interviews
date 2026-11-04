def crack_safe(n: int, k: int) -> str:
    """Shortest string containing every n-digit code over k digits."""
    start = "0" * (n - 1)
    next_digit: dict[str, int] = {}     # node -> first unused edge
    stack = [(start, "")]               # (node, digit that led here)
    digits: list[str] = []
    while stack:
        node, _ = stack[-1]
        d = next_digit.get(node, 0)
        if d < k:                       # unused edge: type digit d
            next_digit[node] = d + 1
            stack.append(((node + str(d))[1:], str(d)))
        else:                           # stuck: write its digit
            digits.append(stack.pop()[1])
    return start + "".join(reversed(digits))
