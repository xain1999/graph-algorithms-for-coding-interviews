def dest_city_brute(paths: list[list[str]]) -> str:
    """For each end city, scan all paths for one that leaves it."""
    for _, end in paths:
        has_way_out = False
        for start, _ in paths:
            if start == end:
                has_way_out = True
                break
        if not has_way_out:
            return end
    raise ValueError("every city has a way out: not a single line")
