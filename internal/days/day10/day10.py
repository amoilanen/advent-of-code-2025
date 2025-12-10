"""Day 10: Button Configuration

Each machine has indicator lights that need to match a target configuration.
Buttons toggle specific lights. Find the minimum button presses needed.

This is solved using Gaussian elimination over GF(2).
"""

import re


def parse(input_text: str) -> list[tuple[list[int], list[list[int]], list[int]]]:
    """Parse machines into (target, buttons, joltage) tuples.
    
    Each line has format: [diagram] (buttons1) (buttons2) ... {joltage}
    Returns list of (target_state, buttons_config, joltage_targets) where:
    - target_state: list of 0s and 1s representing the target diagram (for part 1)
    - buttons_config: list of lists, each inner list has indices that button affects
    - joltage_targets: list of target joltage levels (for part 2)
    """
    machines = []
    
    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue
        
        diagram_match = re.search(r'\[(.*?)\]', line)
        if not diagram_match:
            continue
        
        diagram = diagram_match.group(1)
        target_state = [1 if c == '#' else 0 for c in diagram]
        
        buttons_matches = re.findall(r'\(([\d,]*)\)', line)
        buttons_config = []
        for button_str in buttons_matches:
            if button_str:
                indices = [int(x.strip()) for x in button_str.split(',')]
                buttons_config.append(indices)
            else:
                buttons_config.append([])
        
        joltage_match = re.search(r'\{([\d,]+)\}', line)
        joltage_targets = []
        if joltage_match:
            joltage_targets = [int(x.strip()) for x in joltage_match.group(1).split(',')]
        
        machines.append((target_state, buttons_config, joltage_targets))
    
    return machines


def solve_machine(target_state: list[int], buttons: list[list[int]]) -> int:
    """Solve a single machine using Gaussian elimination over GF(2).
    
    Returns the minimum number of button presses needed.
    """
    num_lights = len(target_state)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return 0 if all(x == 0 for x in target_state) else -1
    
    matrix = build_augmented_matrix(num_lights, buttons, target_state)
    
    if not gaussian_elimination_gf2(matrix):
        return -1
    
    solution = back_substitute_gf2(matrix, num_buttons)
    
    if solution is None:
        return -1
    
    return sum(solution)


def build_augmented_matrix(num_lights: int, buttons: list[list[int]], target: list[int]) -> list[list[int]]:
    """Build augmented matrix [A | b] for the system Ax = b (mod 2).
    
    Rows represent lights, columns represent buttons, last column is target.
    """
    matrix = []
    
    for light_idx in range(num_lights):
        row = []
        for button_idx in range(len(buttons)):
            if light_idx in buttons[button_idx]:
                row.append(1)
            else:
                row.append(0)
        row.append(target[light_idx])
        matrix.append(row)
    
    return matrix


def gaussian_elimination_gf2(matrix: list[list[int]]) -> bool:
    """Perform Gaussian elimination over GF(2).
    
    Reduces matrix to row echelon form.
    Returns False if the system is inconsistent (no solution).
    """
    rows = len(matrix)
    cols = len(matrix[0])
    
    current_row = 0
    
    for col in range(cols - 1):
        pivot_row = find_pivot_gf2(matrix, current_row, col)
        
        if pivot_row == -1:
            continue
        
        swap_rows(matrix, current_row, pivot_row)
        
        for row in range(rows):
            if row != current_row and matrix[row][col] == 1:
                xor_rows(matrix[row], matrix[current_row])
        
        current_row += 1
    
    for row in range(rows):
        all_zero = all(matrix[row][col] == 0 for col in range(cols - 1))
        if all_zero and matrix[row][cols - 1] == 1:
            return False
    
    return True


def find_pivot_gf2(matrix: list[list[int]], start_row: int, col: int) -> int:
    """Find pivot row for given column, starting from start_row."""
    for row in range(start_row, len(matrix)):
        if matrix[row][col] == 1:
            return row
    return -1


def swap_rows(matrix: list[list[int]], row1: int, row2: int) -> None:
    """Swap two rows in the matrix."""
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]


def xor_rows(row1: list[int], row2: list[int]) -> None:
    """XOR row1 with row2 (modify row1 in place)."""
    for i in range(len(row1)):
        row1[i] = (row1[i] + row2[i]) % 2


def back_substitute_gf2(matrix: list[list[int]], num_buttons: int) -> list[int] | None:
    """Back substitution to find solution with minimum number of 1s.
    
    Returns the solution vector with minimum weight or None if no solution.
    Handles underdetermined systems by trying all combinations of free variables.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    
    pivot_cols = []
    for row in range(rows):
        for col in range(num_buttons):
            if matrix[row][col] == 1:
                pivot_cols.append(col)
                break
    
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    if not free_vars:
        solution = back_substitute_fixed_gf2(matrix, num_buttons, {})
        return solution if solution is not None else None
    
    best_solution = None
    best_weight = float('inf')
    
    for assignment in range(1 << len(free_vars)):
        free_var_assignment = {}
        for i, var in enumerate(free_vars):
            free_var_assignment[var] = (assignment >> i) & 1
        
        solution = back_substitute_fixed_gf2(matrix, num_buttons, free_var_assignment)
        if solution is not None:
            weight = sum(solution)
            if weight < best_weight:
                best_weight = weight
                best_solution = solution
    
    return best_solution


def back_substitute_fixed_gf2(matrix: list[list[int]], num_buttons: int, free_var_assignment: dict[int, int]) -> list[int] | None:
    """Back substitution with fixed free variables.
    
    Returns the solution vector or None if inconsistent.
    """
    rows = len(matrix)
    
    solution = [0] * num_buttons
    
    for var, val in free_var_assignment.items():
        solution[var] = val
    
    for row in range(rows - 1, -1, -1):
        pivot_col = -1
        for col in range(num_buttons):
            if matrix[row][col] == 1:
                pivot_col = col
                break
        
        if pivot_col == -1:
            if matrix[row][num_buttons] == 1:
                return None
            continue
        
        val = matrix[row][num_buttons]
        for col in range(pivot_col + 1, num_buttons):
            val = (val + matrix[row][col] * solution[col]) % 2
        
        solution[pivot_col] = val
    
    return solution


def solve_machine_part2(targets: list[int], buttons: list[list[int]]) -> int:
    """Solve joltage counter configuration (minimize total button presses).
    
    This solves the system A*x = b where:
    - A[i][j] = 1 if button j affects counter i
    - b is the target joltage levels  
    - x are button press counts (non-negative integers)
    - Minimize sum(x)
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return 0 if all(x == 0 for x in targets) else -1
    
    matrix = build_augmented_matrix_int(num_counters, buttons, targets)
    
    if not gaussian_elimination_int(matrix):
        return -1
    
    solution = solve_min_weight_int(matrix, num_buttons)
    
    if solution is None:
        return -1
    
    return sum(solution)


def build_augmented_matrix_int(num_counters: int, buttons: list[list[int]], targets: list[int]) -> list[list[int]]:
    """Build augmented matrix for integer system A*x = b."""
    matrix = []
    
    for counter_idx in range(num_counters):
        row = []
        for button_idx in range(len(buttons)):
            if counter_idx in buttons[button_idx]:
                row.append(1)
            else:
                row.append(0)
        row.append(targets[counter_idx])
        matrix.append(row)
    
    return matrix


def gaussian_elimination_int(matrix: list[list[int]]) -> bool:
    """Gaussian elimination with integer arithmetic."""
    rows = len(matrix)
    cols = len(matrix[0])
    
    current_row = 0
    
    for col in range(cols - 1):
        pivot_row = find_pivot_int(matrix, current_row, col)
        
        if pivot_row == -1:
            continue
        
        swap_rows(matrix, current_row, pivot_row)
        
        for row in range(rows):
            if row != current_row and matrix[row][col] != 0:
                subtract_rows_int(matrix[row], matrix[current_row])
        
        current_row += 1
    
    for row in range(rows):
        all_zero = all(matrix[row][col] == 0 for col in range(cols - 1))
        if all_zero and matrix[row][cols - 1] != 0:
            return False
    
    return True


def find_pivot_int(matrix: list[list[int]], start_row: int, col: int) -> int:
    """Find pivot row for given column."""
    for row in range(start_row, len(matrix)):
        if matrix[row][col] != 0:
            return row
    return -1


def subtract_rows_int(row1: list[int], row2: list[int]) -> None:
    """Subtract row2 from row1 (modify row1 in place)."""
    for i in range(len(row1)):
        row1[i] -= row2[i]


def solve_min_weight_int(matrix: list[list[int]], num_buttons: int) -> list[int] | None:
    """Solve integer system and find minimum weight solution.
    
    For underdetermined systems with free variables, find assignments that
    minimize the sum while keeping all variables non-negative.
    """
    rows = len(matrix)
    
    pivot_info = []
    for row in range(rows):
        for col in range(num_buttons):
            if matrix[row][col] != 0:
                pivot_info.append((row, col))
                break
    
    free_vars = [i for i in range(num_buttons) if not any(col == i for _, col in pivot_info)]
    
    if not free_vars:
        solution = compute_solution_int(matrix, num_buttons, {})
        return solution if solution is not None else None
    
    solution = find_min_solution_with_free_vars(matrix, num_buttons, pivot_info, free_vars)
    return solution


def find_min_solution_with_free_vars(matrix: list[list[int]], num_buttons: int, pivot_info: list[tuple[int, int]], free_vars: list[int]) -> list[int] | None:
    """Find minimum solution by trying various free variable assignments."""
    
    def try_free_vars(assignment: dict[int, int]) -> tuple[list[int] | None, int]:
        """Try a specific free variable assignment and return (solution, total_sum) or (None, inf)."""
        solution = compute_solution_int(matrix, num_buttons, assignment)
        if solution is not None and all(x >= 0 for x in solution):
            return (solution, sum(solution))
        return (None, float('inf'))
    
    best_solution = None
    best_weight = float('inf')
    
    # First try all free variables set to 0
    zero_assignment = {var: 0 for var in free_vars}
    solution, weight = try_free_vars(zero_assignment)
    if weight < best_weight:
        best_weight = weight
        best_solution = solution
    
    # If we have few free variables, try a limited brute force with pruning
    if len(free_vars) <= 3:
        if len(free_vars) == 1:
            max_value = 1000
        elif len(free_vars) == 2:
            max_value = 300
        else:
            max_value = 150
        
        def try_all_combinations(var_idx: int, current_assignment: dict[int, int]):
            nonlocal best_solution, best_weight
            
            if var_idx == len(free_vars):
                solution, weight = try_free_vars(current_assignment)
                if weight < best_weight:
                    best_weight = weight
                    best_solution = solution
                return
            
            # Try values up to max_value, with pruning based on best weight found
            limit = max_value + 1
            if best_weight < float('inf'):
                limit = min(limit, int(best_weight) + 1)
            
            for val in range(limit):
                current_assignment[free_vars[var_idx]] = val
                try_all_combinations(var_idx + 1, current_assignment)
        
        try_all_combinations(0, {})
    else:
        # For many free variables, use a limited search
        import random
        random.seed(42)
        
        # Try some strategic values first
        for _ in range(min(1000, 2 ** len(free_vars))):
            assignment = {var: random.randint(0, 30) for var in free_vars}
            solution, weight = try_free_vars(assignment)
            if weight < best_weight:
                best_weight = weight
                best_solution = solution
    
    return best_solution


def compute_solution_int(matrix: list[list[int]], num_buttons: int, free_var_assignment: dict[int, int]) -> list[int] | None:
    """Compute solution with fixed free variables."""
    rows = len(matrix)
    
    solution = [0] * num_buttons
    for var, val in free_var_assignment.items():
        solution[var] = val
    
    for row in range(rows - 1, -1, -1):
        pivot_col = -1
        for col in range(num_buttons):
            if matrix[row][col] != 0:
                pivot_col = col
                break
        
        if pivot_col == -1:
            if matrix[row][num_buttons] != 0:
                return None
            continue
        
        val = matrix[row][num_buttons]
        for col in range(pivot_col + 1, num_buttons):
            if matrix[row][col] != 0:
                val -= matrix[row][col] * solution[col]
        
        if val % matrix[row][pivot_col] != 0:
            return None
        
        solution[pivot_col] = val // matrix[row][pivot_col]
    
    return solution


def part1(machines: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
    """Calculate total minimum button presses for all machines (part 1)."""
    total = 0
    
    for target_state, buttons, _ in machines:
        min_presses = solve_machine(target_state, buttons)
        if min_presses >= 0:
            total += min_presses
    
    return total


def part2(machines: list[tuple[list[int], list[list[int]], list[int]]]) -> int:
    """Calculate total minimum button presses for joltage configuration (part 2)."""
    total = 0
    
    for _, buttons, joltage_targets in machines:
        if joltage_targets:
            min_presses = solve_machine_part2(joltage_targets, buttons)
            if min_presses >= 0:
                total += min_presses
    
    return total
