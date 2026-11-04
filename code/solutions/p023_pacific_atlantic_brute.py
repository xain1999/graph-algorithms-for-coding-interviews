DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def pacific_atlantic_brute(
        heights: list[list[int]]) -> list[tuple[int, int]]:
    """Pour water on every cell and follow it downhill."""
    rows, cols = len(heights), len(heights[0])
    result = []
    for r in range(rows):
        for c in range(cols):
            pacific = atlantic = False
            seen = {(r, c)}
            stack = [(r, c)]
            while stack and not (pacific and atlantic):
                cr, cc = stack.pop()
                if cr == 0 or cc == 0:
                    pacific = True
                if cr == rows - 1 or cc == cols - 1:
                    atlantic = True
                for dr, dc in DIRECTIONS:
                    nr, nc = cr + dr, cc + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and (nr, nc) not in seen
                            and heights[nr][nc] <= heights[cr][cc]):
                        seen.add((nr, nc))  # downhill or level
                        stack.append((nr, nc))
            if pacific and atlantic:
                result.append((r, c))
    return result
