def accounts_merge_brute(
        accounts: list[list[str]]) -> list[list[str]]:
    """Merge any two groups that share an email, until none do."""
    groups = [(account[0], set(account[1:])) for account in accounts]
    merged = True
    while merged:
        merged = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if groups[i][1] & groups[j][1]:   # common email
                    groups[i][1].update(groups[j][1])
                    groups.pop(j)
                    merged = True
                    break
            if merged:
                break                   # indices shifted: rescan
    return [[name] + sorted(emails) for name, emails in groups]
