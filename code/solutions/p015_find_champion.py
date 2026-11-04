def find_champion(n: int, edges: list[list[int]]) -> int:
    """The only team nobody beats, or -1 if there is no such one."""
    indegree = [0] * n
    for _winner, loser in edges:
        indegree[loser] += 1            # someone beats `loser`

    unbeaten = [team for team in range(n) if indegree[team] == 0]
    return unbeaten[0] if len(unbeaten) == 1 else -1
