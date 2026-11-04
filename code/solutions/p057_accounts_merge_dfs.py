from collections import defaultdict


def accounts_merge_dfs(accounts: list[list[str]]) -> list[list[str]]:
    """Link each account's emails in a graph; DFS each component."""
    graph: dict[str, list[str]] = defaultdict(list)
    name_of: dict[str, str] = {}
    for account in accounts:
        first = account[1]
        for email in account[1:]:
            name_of[email] = account[0]
            graph[first].append(email)  # a star per account
            graph[email].append(first)

    seen: set[str] = set()
    result = []
    for start in name_of:
        if start in seen:
            continue
        seen.add(start)
        stack, group = [start], []
        while stack:
            email = stack.pop()
            group.append(email)
            for nxt in graph[email]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        result.append([name_of[start]] + sorted(group))
    return result
