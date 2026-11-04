def check_if_prerequisite_closure(n: int,
                                  prerequisites: list[list[int]],
                                  queries: list[list[int]]
                                  ) -> list[bool]:
    """Transitive closure in the style of Floyd-Warshall."""
    reach = [[False] * n for _ in range(n)]
    for before, after in prerequisites:
        reach[before][after] = True
    for k in range(n):                  # allow k as a middle course
        for i in range(n):
            if reach[i][k]:
                row_i, row_k = reach[i], reach[k]
                for j in range(n):
                    if row_k[j]:
                        row_i[j] = True
    return [reach[u][v] for u, v in queries]
