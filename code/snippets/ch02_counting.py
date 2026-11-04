from collections import Counter, defaultdict

edges = [(0, 1), (0, 2), (2, 1)]
indegree = Counter(v for _, v in edges)    # {1: 2, 2: 1}
outdegree = Counter(u for u, _ in edges)   # {0: 2, 2: 1}
zero = indegree[0]                         # 0, not a KeyError

graph: defaultdict[int, list[int]] = defaultdict(list)
for u, v in edges:
    graph[u].append(v)                     # [] created on first use
