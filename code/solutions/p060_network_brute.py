def make_connected_brute(n: int, cables: list[list[int]]) -> int:
    """Move one spare cable at a time until everything is joined."""
    links = [(a, b) for a, b in cables]     # our own copy

    def label_components(cable_list: list[tuple[int, int]]
                         ) -> tuple[list[int], int]:
        graph: list[list[int]] = [[] for _ in range(n)]
        for a, b in cable_list:
            graph[a].append(b)
            graph[b].append(a)
        comp, count = [-1] * n, 0
        for start in range(n):
            if comp[start] == -1:
                comp[start] = count
                stack = [start]
                while stack:
                    node = stack.pop()
                    for nxt in graph[node]:
                        if comp[nxt] == -1:
                            comp[nxt] = count
                            stack.append(nxt)
                count += 1
        return comp, count

    moves = 0
    while True:
        comp, count = label_components(links)
        if count == 1:
            return moves
        for k in range(len(links)):    # find a spare cable
            rest = links[:k] + links[k + 1:]
            if label_components(rest)[1] == count:
                break
        else:
            return -1                   # every cable is needed
        other = comp.index(1)           # a node outside group 0
        links = rest + [(0, other)]     # re-plug the spare cable
        moves += 1
