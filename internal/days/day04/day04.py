"""Day 4: Paper Roll Access

Determine which paper rolls can be accessed by forklifts based on the number
of adjacent rolls.
"""


def parse(input_text: str) -> list[list[int]]:
    """
    Parse the input into a grid of paper roll locations.

    Each line represents a row in the grid.
    '@' represents a paper roll (converted to 1), '.' represents empty space (converted to 0).

    Returns:
        A 2D list where 1 = paper roll, 0 = empty space
    """
    if not input_text.strip():
        return []

    lines = input_text.strip().split('\n')
    return [[1 if c == '@' else 0 for c in line] for line in lines]


def is_accessible(grid: list[list[int]], row: int, col: int) -> bool:
    """
    Check if a paper roll at the given position is accessible by a forklift.

    A roll is accessible if it has fewer than 4 rolls in the 8 adjacent positions.

    Args:
        grid: The grid of paper roll locations (1 = roll, 0 = empty)
        row: Row index of the roll to check
        col: Column index of the roll to check

    Returns:
        True if the roll is accessible, False otherwise
    """
    # Directions for 8 adjacent positions: N, NE, E, SE, S, SW, W, NW
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    neighbor_count = 0

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Check bounds
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[new_row]):
            neighbor_count += grid[new_row][new_col]
            # Early exit optimization: if we already have 4+ neighbors, not accessible
            if neighbor_count >= 4:
                return False

    return True


def count_accessible_rolls(grid: list[list[int]]) -> int:
    """
    Count how many paper rolls can be accessed by forklifts.

    A roll can be accessed if it has fewer than 4 rolls in its 8 adjacent positions.

    Args:
        grid: The grid of paper roll locations (1 = roll, 0 = empty)

    Returns:
        Number of accessible paper rolls
    """
    if not grid:
        return 0

    accessible_count = 0

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 1:
                if is_accessible(grid, row, col):
                    accessible_count += 1

    return accessible_count


def count_removable_rolls(grid: list[list[int]]) -> int:
    """
    Count how many paper rolls can be removed in total by iteratively removing
    accessible rolls until none remain.

    Algorithm:
    1. Make a copy of the grid
    2. Track all positions with rolls in a set
    3. Loop:
       - Find all currently accessible rolls (only check tracked positions)
       - If none, stop
       - Remove them (set to 0)
       - Update tracked positions
       - Add count to total
    4. Return total count

    Args:
        grid: The grid of paper roll locations (1 = roll, 0 = empty)

    Returns:
        Total number of rolls that can be removed
    """
    if not grid:
        return 0

    # Create a copy of the grid
    mutable_grid = [row[:] for row in grid]

    # Track all positions with rolls for faster iteration
    roll_positions = set()
    for row in range(len(mutable_grid)):
        for col in range(len(mutable_grid[row])):
            if mutable_grid[row][col] == 1:
                roll_positions.add((row, col))

    total_removed = 0

    while roll_positions:
        # Find all accessible rolls (only check positions we know have rolls)
        accessible_positions = []

        for row, col in roll_positions:
            if is_accessible(mutable_grid, row, col):
                accessible_positions.append((row, col))

        # If no accessible rolls found, we're done
        if not accessible_positions:
            break

        # Remove all accessible rolls
        for row, col in accessible_positions:
            mutable_grid[row][col] = 0
            roll_positions.remove((row, col))

        # Add to total count
        total_removed += len(accessible_positions)

    return total_removed


def part1(grid: list[list[int]]) -> int:
    """
    Calculate the number of paper rolls that can be accessed by forklifts.

    Args:
        grid: The grid of paper roll locations (1 = roll, 0 = empty)

    Returns:
        Number of accessible paper rolls
    """
    return count_accessible_rolls(grid)


def part2(grid: list[list[int]]) -> int:
    """
    Calculate the total number of paper rolls that can be removed by iteratively
    removing accessible rolls.

    Args:
        grid: The grid of paper roll locations (1 = roll, 0 = empty)

    Returns:
        Total number of rolls that can be removed
    """
    return count_removable_rolls(grid)
