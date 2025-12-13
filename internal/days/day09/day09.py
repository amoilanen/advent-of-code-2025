"""Day 9: Red Tile Rectangles

Find the largest rectangle using two red tiles as opposite corners.
Part 2 adds the constraint that rectangles can only include red/green tiles.
"""

from typing import List, Tuple, Set


def parse(input_text: str) -> List[Tuple[int, int]]:
    """
    Parse the input text into a list of red tile coordinates.

    Args:
        input_text: The input containing tile coordinates (x,y format)

    Returns:
        List of (x, y) tuples representing red tile positions
    """
    tiles = []
    for line in input_text.strip().split('\n'):
        if line.strip():
            x, y = map(int, line.strip().split(','))
            tiles.append((x, y))
    return tiles


def calculate_rectangle_area(tile1: Tuple[int, int], tile2: Tuple[int, int]) -> int:
    """
    Calculate the area of a rectangle with two tiles as opposite corners.

    The rectangle includes both corner tiles, so we add 1 to each dimension.
    For example, from x=2 to x=5 includes tiles at 2,3,4,5 = 4 tiles wide.

    Args:
        tile1: First corner (x, y)
        tile2: Second corner (x, y)

    Returns:
        Area of the rectangle (number of tiles)
    """
    x1, y1 = tile1
    x2, y2 = tile2
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def part1(tiles: List[Tuple[int, int]]) -> int:
    """
    Find the largest rectangle area using any two red tiles as opposite corners.

    Args:
        tiles: List of red tile coordinates

    Returns:
        Maximum rectangle area
    """
    if len(tiles) < 2:
        return 0

    max_area = 0

    # Check all pairs of tiles
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_rectangle_area(tiles[i], tiles[j])
            max_area = max(max_area, area)

    return max_area


def _point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """
    Check if a point is inside a polygon using ray casting algorithm.

    Args:
        point: (x, y) coordinates of the point
        polygon: List of (x, y) vertices of the polygon

    Returns:
        True if point is inside the polygon, False otherwise
    """
    x, y = point
    n = len(polygon)
    edge_crossings = 0

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    # Line going through the points p1 and p2 has the equation:
                    # y - p1y = m * (x - p1x)
                    # m = (p2y - p1y) / (p2x - p1x)
                    if p1y != p2y:
                        x_intersection = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersection: # Ray goes to the right
                        edge_crossings = edge_crossings + 1
        p1x, p1y = p2x, p2y

    return edge_crossings % 2 == 1


def _build_green_tiles(red_tiles: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """
    Build set of all green tiles (edges of polygon + interior).

    Args:
        red_tiles: List of red tile coordinates in order forming a closed loop

    Returns:
        Set of all green tile coordinates
    """
    green = set()

    # Find bounding box to check interior tiles
    min_x = min(x for x, y in red_tiles)
    max_x = max(x for x, y in red_tiles)
    min_y = min(y for x, y in red_tiles)
    max_y = max(y for x, y in red_tiles)

    # Check all tiles in bounding box
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if _point_in_polygon((x, y), red_tiles):
                green.add((x, y))

    return green


def _compress_coordinates(tiles: List[Tuple[int, int]]) -> Tuple[dict, dict, List[Tuple[int, int]]]:
    """
    Compress sparse coordinates to dense grid indices.

    OPTIMIZATION: Coordinate compression transforms a sparse coordinate space
    (e.g., coordinates ranging from 0 to 100,000) into a dense space where
    only the unique coordinates that appear in the input are represented.

    For example, if tiles are at x-coordinates [10, 100, 1000], we compress
    them to indices [0, 1, 2] (or with gaps: [0, -1, 1, -1, 2]).

    The gaps (inserting -1 before each coordinate) ensure that rectangles
    between non-adjacent points in the original space still have interior
    space in the compressed grid.

    Args:
        tiles: List of (x, y) coordinate pairs

    Returns:
        (x_map, y_map, compressed_tiles) where:
        - x_map: dict mapping original x -> compressed x index
        - y_map: dict mapping original y -> compressed y index
        - compressed_tiles: tiles in compressed coordinate space
    """
    # Extract unique x and y coordinates
    xs = sorted(set(x for x, y in tiles))
    ys = sorted(set(y for x, y in tiles))

    # Create compressed coordinates with gaps between each unique value
    # This preserves the structure: gaps allow for interior points in rectangles
    x_coords = []
    for x in xs:
        x_coords.extend([-1, x])  # Add gap before each coordinate
    y_coords = []
    for y in ys:
        y_coords.extend([-1, y])

    # Build mapping from original coordinates to compressed indices
    x_map = {x: i for i, x in enumerate(x_coords)}
    y_map = {y: i for i, y in enumerate(y_coords)}

    # Convert tiles to compressed space
    compressed_tiles = [(x_map[x], y_map[y]) for x, y in tiles]

    return x_map, y_map, compressed_tiles


def _create_grid(max_cx: int, max_cy: int) -> List[List[str]]:
    """
    Create an empty grid in compressed coordinate space.

    Args:
        max_cx: Maximum compressed x coordinate
        max_cy: Maximum compressed y coordinate

    Returns:
        2D grid with dimensions (max_cx + 2) × (max_cy + 2)
        Extra padding ensures border of empty space around polygon
    """
    return [[' ' for _ in range(max_cy + 2)] for _ in range(max_cx + 2)]


def _mark_polygon_edges(grid: List[List[str]], compressed_tiles: List[Tuple[int, int]]) -> None:
    n = len(compressed_tiles)
    for i in range(n):
        p1 = compressed_tiles[i]
        p2 = compressed_tiles[(i + 1) % n]  # Wrap around to close the loop
        # Draw line between consecutive red tiles
        for tile in _get_tiles_on_line(p1, p2):
            cx, cy = tile
            if 0 <= cx < len(grid) and 0 <= cy < len(grid[0]):
                grid[cx][cy] = '#'  # Mark as boundary (green tile), we mark both green and red as #

def _get_tiles_on_line(p1: Tuple[int, int], p2: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Get all integer coordinate tiles on a line between two points (inclusive).

    Args:
        p1: First point (x, y)
        p2: Second point (x, y)

    Returns:
        Set of all tiles on the line between p1 and p2
    """
    x1, y1 = p1
    x2, y2 = p2
    tiles = set()

    # Ensure we go from smaller to larger coordinate
    if x1 == x2:  # Vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles.add((x1, y))
    elif y1 == y2:  # Horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles.add((x, y1))
    else:
        # Should not happen according to problem (adjacent tiles are on same row/col)
        pass

    return tiles

def _flood_fill_exterior(grid: List[List[str]]) -> None:
    from collections import deque

    queue = deque([(0, 0)])  # Start from top-left corner (guaranteed outside)
    if grid[0][0] != '#':
        grid[0][0] = '.'  # Mark as exterior

        while queue:
            cx, cy = queue.popleft()
            # Check all 4 directions
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                # If neighbor is unmarked (' '), it's also exterior
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == ' ':
                    grid[nx][ny] = '.'  # Mark as exterior
                    queue.append((nx, ny))


def _find_largest_valid_rectangle(
    tiles: List[Tuple[int, int]],
    compressed_tiles: List[Tuple[int, int]],
    grid: List[List[str]]
) -> int:
    # Generate all rectangle candidates sorted by area (descending)
    pairs = []
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            # Calculate area in ORIGINAL coordinates (what we return)
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            pairs.append((area, i, j))

    pairs.sort(reverse=True)  # Largest area first

    # Check rectangles in compressed space
    max_area = 0
    for potential_area, i, j in pairs:
        # Early termination: if max possible area ≤ current best, we're done
        if potential_area <= max_area:
            break

        # Get corners in compressed space
        cx1, cy1 = compressed_tiles[i]
        cx2, cy2 = compressed_tiles[j]
        min_cx, max_cx = min(cx1, cx2), max(cx1, cx2)
        min_cy, max_cy = min(cy1, cy2), max(cy1, cy2)

        # Check if ALL tiles in rectangle are valid (not exterior)
        all_valid = True
        for cx in range(min_cx, max_cx + 1):
            if not all_valid:
                break
            for cy in range(min_cy, max_cy + 1):
                if grid[cx][cy] == '.':  # Found exterior tile
                    all_valid = False
                    break

        if all_valid:
            # This rectangle only contains green/red tiles
            max_area = potential_area

    return max_area

def part2(tiles: List[Tuple[int, int]]) -> int:
    if len(tiles) < 2:
        return 0
    x_map, y_map, compressed_tiles = _compress_coordinates(tiles)
    max_cx = max(cx for cx, cy in compressed_tiles)
    max_cy = max(cy for cx, cy in compressed_tiles)
    grid = _create_grid(max_cx, max_cy)
    _mark_polygon_edges(grid, compressed_tiles)
    _flood_fill_exterior(grid)
    return _find_largest_valid_rectangle(tiles, compressed_tiles, grid)
