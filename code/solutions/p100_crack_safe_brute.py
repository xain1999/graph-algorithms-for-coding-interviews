def crack_safe_brute(n: int, k: int) -> str:
    """Backtracking: append a digit only if it makes a new code.

    Recursion depth is k**n; meant for small n and k only.
    """
    total = k ** n
    text = ["0"] * n
    seen = {"0" * n}

    def extend() -> bool:
        if len(seen) == total:
            return True
        tail = "".join(text[len(text) - n + 1:]) if n > 1 else ""
        for d in map(str, range(k)):
            code = tail + d
            if code in seen:
                continue
            seen.add(code)
            text.append(d)
            if extend():
                return True
            text.pop()
            seen.remove(code)
        return False

    extend()
    return "".join(text)
