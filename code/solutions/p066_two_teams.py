from collections import deque


def split_into_teams(n: int, rivals: list[list[int]]) -> list[int]:
    """team[i] in {0, 1}, rivals always apart; [] if impossible."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in rivals:
        graph[a].append(b)
        graph[b].append(a)

    team = [-1] * n                     # -1: not placed yet
    for start in range(n):              # every group of players
        if team[start] != -1:
            continue
        team[start] = 0                 # free choice for a new group
        queue = deque([start])
        while queue:
            player = queue.popleft()
            for rival in graph[player]:
                if team[rival] == -1:
                    team[rival] = 1 - team[player]  # forced
                    queue.append(rival)
                elif team[rival] == team[player]:
                    return []           # odd cycle of rivals
    return team
