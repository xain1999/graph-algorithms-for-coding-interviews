def crack_safe_greedy(n: int, k: int) -> str:
    """Prefer-largest greedy: append the largest digit that types a
    code not seen before; stop when no digit does."""
    text = "0" * n
    seen = {text}
    while True:
        tail = text[len(text) - n + 1:] if n > 1 else ""
        for d in reversed(range(k)):
            code = tail + str(d)
            if code not in seen:
                seen.add(code)
                text += str(d)
                break
        else:
            return text
