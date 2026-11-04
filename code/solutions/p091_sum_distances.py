def sum_of_distances(n: int, edges: list[list[int]]) -> list[int]:
    """For every node, the sum of its distances to all other nodes."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # Root at 0. The list grows while we read it (a BFS queue that is
    # never popped), so every parent comes before its children.
    parent = [-1] * n
    depth = [0] * n
    order = [0]
    for node in order:
        for nxt in graph[node]:
            if nxt != parent[node]:
                parent[nxt] = node
                depth[nxt] = depth[node] + 1
                order.append(nxt)

    size = [1] * n                      # nodes in each subtree
    for node in reversed(order[1:]):    # children before parents
        size[parent[node]] += size[node]

    answer = [0] * n
    answer[0] = sum(depth)              # distances from the root
    for node in order[1:]:              # parents before children
        # Moving the root from parent to node: size[node] nodes get
        # one step closer, the other n - size[node] one step farther.
        answer[node] = answer[parent[node]] + n - 2 * size[node]
    return answer
