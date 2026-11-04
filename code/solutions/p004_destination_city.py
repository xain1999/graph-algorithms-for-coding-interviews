def dest_city(paths: list[list[str]]) -> str:
    """The one city that no path leaves from."""
    starts: set[str] = set()
    for start, _ in paths:
        starts.add(start)       # these cities have out-degree >= 1

    for _, end in paths:
        if end not in starts:   # out-degree 0: the journey ends here
            return end
    raise ValueError("every city has a way out: not a single line")
