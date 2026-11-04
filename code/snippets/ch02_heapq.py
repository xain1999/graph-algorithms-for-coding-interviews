import heapq

heap: list[tuple[int, str]] = []
heapq.heappush(heap, (5, "e"))
heapq.heappush(heap, (1, "a"))
heapq.heappush(heap, (3, "c"))
smallest = heapq.heappop(heap)      # (1, 'a'): always the minimum
peek = heap[0]                      # (3, 'c'): look, don't remove

nums = [4, 9, 2]
max_heap = [-x for x in nums]       # before 3.14, heapq is min-only,
heapq.heapify(max_heap)             # so store negated values
largest = -heapq.heappop(max_heap)  # 9
