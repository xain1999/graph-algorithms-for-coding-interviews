def root_tree_rec(n: int, edges: list[list[int]],
                  root: int) -> list[int]:
    """Recursive DFS: safe only for trees of depth below ~900."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n

    def visit(node: int) -> None:
        for nxt in graph[node]:
            if nxt != parent[node]:
                parent[nxt] = node
                visit(nxt)

    visit(root)
    return parent
