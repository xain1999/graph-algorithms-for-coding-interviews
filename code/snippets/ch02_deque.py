from collections import deque

queue = deque([1, 2])
queue.append(3)             # add on the right: deque([1, 2, 3])
first = queue.popleft()     # take from the left in O(1): 1
queue.appendleft(0)         # deque([0, 2, 3])
last = queue.pop()          # take from the right: 3
