def count_provinces(is_connected: list[list[int]]) -> int:
    """Number of groups of cities linked directly or indirectly."""
    n = len(is_connected)
    seen = [False] * n
    provinces = 0
    for start in range(n):
        if seen[start]:
            continue
        provinces += 1              # untouched city: new province
        seen[start] = True
        stack = [start]
        while stack:
            city = stack.pop()
            row = is_connected[city]
            for other in range(n):  # the whole row: all neighbors
                if row[other] == 1 and not seen[other]:
                    seen[other] = True
                    stack.append(other)
    return provinces
