def can_reach_recursive(arr: list[int], start: int) -> bool:
    """Recursive DFS: short, but as deep as the longest jump chain."""
    seen: set[int] = set()

    def dfs(i: int) -> bool:
        if not 0 <= i < len(arr) or i in seen:
            return False
        if arr[i] == 0:
            return True
        seen.add(i)                 # without this: endless loops
        return dfs(i + arr[i]) or dfs(i - arr[i])

    return dfs(start)
