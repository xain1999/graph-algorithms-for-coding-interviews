def find_judge_brute(n: int, trust: list[list[int]]) -> int:
    """Test each person against the whole trust list."""
    for person in range(1, n + 1):
        trusts_someone = False
        trusted_by = 0
        for a, b in trust:
            if a == person:
                trusts_someone = True
            elif b == person:
                trusted_by += 1
        if not trusts_someone and trusted_by == n - 1:
            return person
    return -1
