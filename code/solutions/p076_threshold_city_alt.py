import heapq


def find_the_city_dijkstra(n: int, roads: list[list[int]],
                           threshold: int) -> int:
    """One Dijkstra per city, stopping beyond the threshold."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b, length in roads:
        graph[a].append((b, length))
        graph[b].append((a, length))
    best_city, best_count = -1, n
    for src in range(n):
        dist = {src: 0}
        heap = [(0, src)]
        done: set[int] = set()
        while heap:
            d, node = heapq.heappop(heap)
            if node in done:
                continue                # stale entry
            done.add(node)
            for nxt, length in graph[node]:
                nd = d + length
                # paths longer than the threshold never matter
                if nd <= threshold and nd < dist.get(nxt, nd + 1):
                    dist[nxt] = nd
                    heapq.heappush(heap, (nd, nxt))
        count = len(done) - 1           # every reached city but src
        if count <= best_count:
            best_city, best_count = src, count
    return best_city
