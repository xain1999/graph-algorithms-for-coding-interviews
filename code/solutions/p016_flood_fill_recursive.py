DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def flood_fill_recursive(image: list[list[int]], sr: int, sc: int,
                         color: int) -> list[list[int]]:
    """Recursive version: short, but one call per pixel deep."""
    image = [row[:] for row in image]
    old = image[sr][sc]
    rows, cols = len(image), len(image[0])

    def paint(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols):
            return                      # off the image
        if image[r][c] != old:
            return                      # other color, or painted
        image[r][c] = color
        for dr, dc in DIRECTIONS:
            paint(r + dr, c + dc)

    if old != color:                    # without this: endless calls
        paint(sr, sc)
    return image
