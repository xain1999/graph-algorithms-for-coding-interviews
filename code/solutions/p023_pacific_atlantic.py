DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def pacific_atlantic(
        heights: list[list[int]]) -> list[tuple[int, int]]:
    """Cells whose rain can reach both oceans, in row-major order."""
    rows, cols = len(heights), len(heights[0])

    def climb(sources: list[tuple[int, int]]) -> set[tuple[int, int]]:
        """All cells from which water can flow down to a source."""
        seen = set(sources)
        stack = list(seen)
        while stack:
            r, c = stack.pop()
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):
                    seen.add((nr, nc))      # uphill or level
                    stack.append((nr, nc))
        return seen

    pacific = climb([(0, c) for c in range(cols)]
                    + [(r, 0) for r in range(rows)])
    atlantic = climb([(rows - 1, c) for c in range(cols)]
                     + [(r, cols - 1) for r in range(rows)])
    return [(r, c) for r in range(rows) for c in range(cols)
            if (r, c) in pacific and (r, c) in atlantic]
