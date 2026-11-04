def find_champion_brute(n: int, edges: list[list[int]]) -> int:
    """Try each team: does a DFS from it reach every other team?"""
    graph: list[list[int]] = [[] for _ in range(n)]
    for winner, loser in edges:
        graph[winner].append(loser)

    champions = []
    for team in range(n):
        seen = {team}
        stack = [team]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if len(seen) == n:              # reaches everyone
            champions.append(team)
    return champions[0] if len(champions) == 1 else -1
