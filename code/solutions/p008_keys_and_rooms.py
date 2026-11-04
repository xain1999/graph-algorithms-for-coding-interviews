def can_visit_all_rooms(rooms: list[list[int]]) -> bool:
    """True if every room can be opened, starting in room 0."""
    seen = {0}                      # room 0 is never locked
    stack = [0]
    while stack:
        room = stack.pop()
        for key in rooms[room]:
            if key not in seen:     # a door we could not open yet
                seen.add(key)
                stack.append(key)
    return len(seen) == len(rooms)
