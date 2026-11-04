DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def flood_fill(image: list[list[int]], sr: int, sc: int,
               color: int) -> list[list[int]]:
    """Copy of image with the start pixel's region repainted."""
    image = [row[:] for row in image]   # leave the input untouched
    old = image[sr][sc]
    if old == color:
        return image        # nothing to repaint, and no endless loop
    rows, cols = len(image), len(image[0])
    image[sr][sc] = color               # painting = marking as seen
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and image[nr][nc] == old):
                image[nr][nc] = color   # paint when pushed
                stack.append((nr, nc))
    return image
