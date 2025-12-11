"""Day 10: Button Configuration

Part 1: Toggle indicator lights to match a target configuration.
Each button toggles specific lights. Since toggling is XOR, pressing a button
twice is the same as not pressing it at all. This is a linear algebra problem
over GF(2).

Part 2: Increment joltage counters to match target values.
Each button press increments specific counters by 1. This is an Integer Linear
Programming (ILP) problem where we minimize total button presses subject to
reaching target counter values.
"""

import re
from typing import List, Tuple, Optional
try:
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


def parse(input_text: str) -> List[Tuple[List[bool], List[List[int]]]]:
    """
    Parse the input text into a list of machine configurations.

    Each machine has:
    - A target state for indicator lights (list of bools)
    - A list of buttons, where each button is a list of light indices it toggles

    Args:
        input_text: The input containing machine configurations

    Returns:
        List of (target_state, buttons) tuples
    """
    machines = []

    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue

        # Extract target state from [square brackets]
        target_match = re.search(r'\[(.*?)\]', line)
        if not target_match:
            continue

        target_str = target_match.group(1)
        target = [c == '#' for c in target_str]

        # Extract buttons from (parentheses)
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        buttons = []
        for button_str in button_matches:
            indices = [int(x) for x in button_str.split(',')]
            buttons.append(indices)

        machines.append((target, buttons))

    return machines


def solve_machine(target: List[bool], buttons: List[List[int]]) -> Optional[int]:
    """
    Find the minimum number of button presses needed to reach the target state.

    Uses brute force to try all possible combinations of button presses.
    Since toggling is XOR, we only need to consider pressing each button 0 or 1 times.

    Args:
        target: Target state for each light (True = on, False = off)
        buttons: List of buttons, where each button is a list of light indices

    Returns:
        Minimum number of button presses, or None if no solution exists
    """
    n_lights = len(target)
    n_buttons = len(buttons)

    # If target is all off and no buttons, return 0
    if not any(target):
        return 0

    # Try all 2^n_buttons combinations
    min_presses = None

    for mask in range(1 << n_buttons):
        # Simulate pressing buttons according to the mask
        state = [False] * n_lights
        presses = 0

        for j in range(n_buttons):
            if mask & (1 << j):
                presses += 1
                # Toggle lights for this button
                for light_idx in buttons[j]:
                    if light_idx < n_lights:
                        state[light_idx] = not state[light_idx]

        # Check if we reached the target state
        if state == target:
            if min_presses is None or presses < min_presses:
                min_presses = presses

    return min_presses


def part1(machines: List[Tuple[List[bool], List[List[int]]]]) -> int:
    """
    Calculate the total minimum button presses for all machines.

    Args:
        machines: List of (target_state, buttons) tuples

    Returns:
        Sum of minimum presses for all machines
    """
    total = 0

    for target, buttons in machines:
        min_presses = solve_machine(target, buttons)
        if min_presses is not None:
            total += min_presses

    return total


def parse_part2(input_text: str) -> List[Tuple[List[int], List[List[int]]]]:
    """
    Parse the input text for part 2 (joltage requirements).

    Each machine has:
    - Target joltage values for counters (from {curly braces})
    - A list of buttons, where each button is a list of counter indices it increments

    Args:
        input_text: The input containing machine configurations

    Returns:
        List of (target_values, buttons) tuples
    """
    machines = []

    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue

        # Extract target values from {curly braces}
        target_match = re.search(r'\{([0-9,]+)\}', line)
        if not target_match:
            continue

        target_str = target_match.group(1)
        targets = [int(x) for x in target_str.split(',')]

        # Extract buttons from (parentheses)
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        buttons = []
        for button_str in button_matches:
            indices = [int(x) for x in button_str.split(',')]
            buttons.append(indices)

        machines.append((targets, buttons))

    return machines


def solve_machine_part2(targets: List[int], buttons: List[List[int]]) -> Optional[int]:
    """
    Find the minimum number of button presses to reach target counter values.

    This is an Integer Linear Programming (ILP) problem:
    - Variables: x_i = number of times button i is pressed
    - Constraints: For each counter j, sum(x_i for buttons affecting j) = target_j
    - Objective: minimize sum(x_i)

    Args:
        targets: Target values for each counter
        buttons: List of buttons, where each button is a list of counter indices

    Returns:
        Minimum number of button presses, or None if no solution exists
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("scipy and numpy are required for part 2")

    n_counters = len(targets)
    n_buttons = len(buttons)

    # If all targets are zero, no button presses needed
    if all(t == 0 for t in targets):
        return 0

    # Build constraint matrix A where A[i,j] = 1 if button j affects counter i
    A = [[0] * n_buttons for _ in range(n_counters)]
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                A[counter_idx][j] = 1

    # Convert to numpy arrays
    A = np.array(A, dtype=float)
    b_l = np.array(targets, dtype=float)  # lower bounds
    b_u = np.array(targets, dtype=float)  # upper bounds (equality constraints)

    # Objective: minimize sum of button presses
    c = np.ones(n_buttons)

    # All variables are integers >= 0
    integrality = np.ones(n_buttons)  # 1 = integer variable
    bounds = Bounds(lb=np.zeros(n_buttons), ub=np.inf)

    # Set up constraints (Ax = b, where b_l <= Ax <= b_u with b_l = b_u)
    constraints = LinearConstraint(A, b_l, b_u)

    # Solve the ILP problem
    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        return None


def part2(machines: List[Tuple[List[int], List[List[int]]]]) -> int:
    """
    Calculate the total minimum button presses for all machines (part 2).

    Args:
        machines: List of (target_values, buttons) tuples

    Returns:
        Sum of minimum presses for all machines
    """
    total = 0

    for targets, buttons in machines:
        min_presses = solve_machine_part2(targets, buttons)
        if min_presses is not None:
            total += min_presses

    return total
