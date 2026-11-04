def find_judge(n: int, trust: list[list[int]]) -> int:
    """Label of the town judge, or -1 if there is none."""
    score = [0] * (n + 1)       # index 0 unused: people are 1..n
    for a, b in trust:
        score[a] -= 1           # a trusts someone (out-degree)
        score[b] += 1           # b is trusted (in-degree)

    for person in range(1, n + 1):
        if score[person] == n - 1:
            return person
    return -1
