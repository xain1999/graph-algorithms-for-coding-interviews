from collections import defaultdict


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """One entry per person: name, then their emails sorted."""
    parent = list(range(len(accounts)))     # one node per account

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    owner: dict[str, int] = {}          # email -> first account
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in owner:
                parent[find(i)] = find(owner[email])  # same person
            else:
                owner[email] = i

    groups: dict[int, list[str]] = defaultdict(list)
    for email, i in owner.items():
        groups[find(i)].append(email)
    return [[accounts[root][0]] + sorted(emails)
            for root, emails in groups.items()]
