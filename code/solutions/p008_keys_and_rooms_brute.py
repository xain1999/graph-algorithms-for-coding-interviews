def can_visit_all_rooms_brute(rooms: list[list[int]]) -> bool:
    """Sweep the open rooms again and again until nothing changes."""
    is_open = [False] * len(rooms)
    is_open[0] = True
    changed = True
    while changed:
        changed = False
        for room in range(len(rooms)):
            if not is_open[room]:
                continue
            for key in rooms[room]:
                if not is_open[key]:
                    is_open[key] = True
                    changed = True
    return all(is_open)
