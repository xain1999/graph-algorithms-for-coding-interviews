def check_if_prerequisite_brute(n: int,
                                prerequisites: list[list[int]],
                                queries: list[list[int]]
                                ) -> list[bool]:
    """Answer each query with its own DFS from u, looking for v."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for before, after in prerequisites:
        graph[before].append(after)

    def reaches(u: int, v: int) -> bool:
        seen = {u}
        stack = [u]
        while stack:
            node = stack.pop()
            if node == v:
                return True
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    return [reaches(u, v) for u, v in queries]
