"""Day 7: Tachyon Manifold

A tachyon beam enters the manifold at location S and moves downward.
When it hits a splitter (^), it stops and creates two new beams
to the left and right. Count how many times the beam is split.
"""

from collections import deque
from typing import Tuple


def parse(input_text: str) -> Tuple[list[str], int, int]:
    """
    Parse the input grid and find the starting position S.

    Args:
        input_text: The grid text

    Returns:
        Tuple of (grid, start_row, start_col)
    """
    lines = input_text.strip().split('\n')
    grid = [line for line in lines if line.strip()]
    
    # Find the starting position S
    start_row = None
    start_col = None
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                start_row = row_idx
                start_col = col_idx
                break
        if start_row is not None:
            break
    
    if start_row is None or start_col is None:
        raise ValueError("Starting position S not found in grid")
    
    return grid, start_row, start_col


def part1(grid: list[str], start_row: int, start_col: int) -> int:
    """
    Count how many times the beam is split.

    Args:
        grid: The grid as a list of strings
        start_row: Starting row position
        start_col: Starting column position

    Returns:
        Number of times the beam is split
    """
    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    
    # Queue of beams: (row, col, direction)
    # Direction is 'down' for all beams
    # Start from the row below S (beam moves downward from S)
    queue = deque()
    queue.append((start_row + 1, start_col, 'down'))
    
    split_count = 0
    # Track which splitters we've already processed
    # Each splitter can only split once, even if multiple beams converge on it
    processed_splitters = set()
    # Track which beam starting positions we've already processed
    # to avoid duplicate work
    processed_beams = set()

    while queue:
        row, col, direction = queue.popleft()

        # Skip if we've already processed a beam from this position
        beam_key = (row, col)
        if beam_key in processed_beams:
            continue
        processed_beams.add(beam_key)

        # Move the beam downward until it hits a splitter or goes out of bounds
        current_row = row
        current_col = col
        
        # Move downward
        while True:
            # Check if we're out of bounds
            if current_row >= rows or current_col < 0 or current_col >= cols:
                # Beam exits the grid
                break
            
            char = grid[current_row][current_col]
            
            # Check if we hit a splitter
            if char == '^':
                splitter_key = (current_row, current_col)
                
                # Only count this splitter if we haven't processed it before
                if splitter_key not in processed_splitters:
                    processed_splitters.add(splitter_key)
                    split_count += 1
                
                # Create two new beams: one to the left, one to the right
                left_col = current_col - 1
                right_col = current_col + 1
                
                # Left beam
                if left_col >= 0:
                    queue.append((current_row, left_col, 'down'))
                
                # Right beam
                if right_col < cols:
                    queue.append((current_row, right_col, 'down'))
                
                break
            
            # Continue moving downward
            current_row += 1
    
    return split_count


def part2(grid: list[str], start_row: int, start_col: int) -> int:
    """
    Count the number of unique timelines (quantum many-worlds interpretation).

    In Part 2, a single quantum particle takes both paths at each splitter,
    creating multiple timelines. We count how many unique paths (timelines)
    exist from start to exit.

    Uses memoization to count paths efficiently: for each starting position,
    calculate how many distinct exit paths exist.

    Args:
        grid: The grid as a list of strings
        start_row: Starting row position
        start_col: Starting column position

    Returns:
        Number of unique timelines
    """
    rows = len(grid)
    cols = len(grid[0]) if grid else 0

    # Memoization: cache[row][col] = number of distinct paths from (row, col) to exit
    cache = {}

    def count_paths(row, col):
        """Count distinct paths from (row, col) to grid exit."""
        # Check if out of bounds - this is one exit path
        if row >= rows or col < 0 or col >= cols:
            return 1

        # Check cache
        if (row, col) in cache:
            return cache[(row, col)]

        # Get current cell
        char = grid[row][col]

        # If it's a splitter, count paths from both split directions
        if char == '^':
            # Split into left and right beams (at same row)
            # Then each continues downward
            left_paths = count_paths(row, col - 1)
            right_paths = count_paths(row, col + 1)
            total = left_paths + right_paths
        else:
            # Continue downward
            total = count_paths(row + 1, col)

        cache[(row, col)] = total
        return total

    # Start counting from position below S
    return count_paths(start_row + 1, start_col)

