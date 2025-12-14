"""Tests for Day 10: Button Configuration"""

import pytest
from .day10 import parse, solve_machine, part1, part2, parse_part2, solve_machine_part2
from .input import EXAMPLE_INPUT


class TestParse:
    """Test parsing of machine configurations."""

    def test_parse_single_machine(self):
        """Test parsing a single machine."""
        input_text = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        machines = parse(input_text)

        assert len(machines) == 1
        machine = machines[0]

        # Target state: [False, True, True, False]
        assert machine.target == [False, True, True, False]

        # Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)
        assert len(machine.buttons) == 6
        assert machine.buttons[0] == [3]
        assert machine.buttons[1] == [1, 3]
        assert machine.buttons[2] == [2]
        assert machine.buttons[3] == [2, 3]
        assert machine.buttons[4] == [0, 2]
        assert machine.buttons[5] == [0, 1]

    def test_parse_example(self):
        """Test parsing the example input."""
        machines = parse(EXAMPLE_INPUT)

        assert len(machines) == 3

        # First machine: [.##.]
        assert machines[0].target == [False, True, True, False]
        assert len(machines[0].buttons) == 6

        # Second machine: [...#.]
        assert machines[1].target == [False, False, False, True, False]
        assert len(machines[1].buttons) == 5

        # Third machine: [.###.#]
        assert machines[2].target == [False, True, True, True, False, True]
        assert len(machines[2].buttons) == 4

    def test_parse_multidigit_indices(self):
        """Test parsing buttons with multi-digit indices."""
        input_text = "[...........#] (0,10,11) {1,2,3}"
        machines = parse(input_text)

        machine = machines[0]
        assert len(machine.target) == 12
        assert machine.target[11] == True
        assert machine.buttons[0] == [0, 10, 11]


class TestSolveMachine:
    """Test solving individual machines."""

    def test_solve_example1(self):
        """Test solving first example machine."""
        # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)
        target = [False, True, True, False]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

        min_presses = solve_machine(target, buttons)
        assert min_presses == 2  # Press (0,2) and (0,1)

    def test_solve_example2(self):
        """Test solving second example machine."""
        # [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4)
        target = [False, False, False, True, False]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

        min_presses = solve_machine(target, buttons)
        assert min_presses == 3  # Press (0,4), (0,1,2), and (1,2,3,4)

    def test_solve_example3(self):
        """Test solving third example machine."""
        # [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2)
        target = [False, True, True, True, False, True]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

        min_presses = solve_machine(target, buttons)
        assert min_presses == 2  # Press (0,3,4) and (0,1,2,4,5)

    def test_solve_all_off(self):
        """Test when target is all off (should be 0 presses)."""
        target = [False, False, False]
        buttons = [[0], [1], [2]]

        min_presses = solve_machine(target, buttons)
        assert min_presses == 0

    def test_solve_single_button(self):
        """Test when only one button press is needed."""
        target = [True, False, True]
        buttons = [[0, 2], [1], [0, 1, 2]]

        min_presses = solve_machine(target, buttons)
        assert min_presses == 1  # Press button (0,2)

    def test_solve_no_solution(self):
        """Test when there's no solution."""
        target = [True, False]
        buttons = [[0, 1]]  # Can only toggle both together

        min_presses = solve_machine(target, buttons)
        assert min_presses is None


class TestPart1:
    """Test part 1 solution."""

    def test_example(self):
        """Test with the example from problem description."""
        machines = parse(EXAMPLE_INPUT)
        result = part1(machines)

        # 2 + 3 + 2 = 7
        assert result == 7

    def test_single_machine_all_off(self):
        """Test with a single machine where target is all off."""
        input_text = "[...] (0) (1) (2) {1,2,3}"
        machines = parse(input_text)
        result = part1(machines)

        assert result == 0

    def test_multiple_machines(self):
        """Test with multiple simple machines."""
        input_text = """[#] (0) {1}
[##] (0,1) {2,3}
[.] (0) {4}"""
        machines = parse(input_text)
        result = part1(machines)

        # Machine 1: 1 press for (0)
        # Machine 2: 1 press for (0,1)
        # Machine 3: 0 presses
        assert result == 2


class TestParsePart2:
    """Test parsing for part 2 (joltage requirements)."""

    def test_parse_single_machine(self):
        """Test parsing a single machine for part 2."""
        input_text = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        machines = parse_part2(input_text)

        assert len(machines) == 1
        machine = machines[0]

        # Targets: {3,5,4,7}
        assert machine.targets == [3, 5, 4, 7]

        # Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)
        assert len(machine.buttons) == 6
        assert machine.buttons[0] == [3]
        assert machine.buttons[1] == [1, 3]
        assert machine.buttons[2] == [2]
        assert machine.buttons[3] == [2, 3]
        assert machine.buttons[4] == [0, 2]
        assert machine.buttons[5] == [0, 1]

    def test_parse_example(self):
        """Test parsing the example input for part 2."""
        machines = parse_part2(EXAMPLE_INPUT)

        assert len(machines) == 3

        # First machine: {3,5,4,7}
        assert machines[0].targets == [3, 5, 4, 7]
        assert len(machines[0].buttons) == 6

        # Second machine: {7,5,12,7,2}
        assert machines[1].targets == [7, 5, 12, 7, 2]
        assert len(machines[1].buttons) == 5

        # Third machine: {10,11,11,5,10,5}
        assert machines[2].targets == [10, 11, 11, 5, 10, 5]
        assert len(machines[2].buttons) == 4


class TestSolveMachinePart2:
    """Test solving individual machines for part 2."""

    def test_solve_example1(self):
        """Test solving first example machine.

        Counters: {3,5,4,7}
        Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)

        One solution: press (3) once, (1,3) three times, (2,3) three times,
        (0,2) once, and (0,1) twice = 10 total presses
        """
        targets = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]

        min_presses = solve_machine_part2(targets, buttons)
        assert min_presses == 10

    def test_solve_example2(self):
        """Test solving second example machine.

        Counters: {7,5,12,7,2}
        Buttons: (0,2,3,4), (2,3), (0,4), (0,1,2), (1,2,3,4)

        Minimum: 12 presses
        """
        targets = [7, 5, 12, 7, 2]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]

        min_presses = solve_machine_part2(targets, buttons)
        assert min_presses == 12

    def test_solve_example3(self):
        """Test solving third example machine.

        Counters: {10,11,11,5,10,5}
        Buttons: (0,1,2,3,4), (0,3,4), (0,1,2,4,5), (1,2)

        Minimum: 11 presses
        """
        targets = [10, 11, 11, 5, 10, 5]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]

        min_presses = solve_machine_part2(targets, buttons)
        assert min_presses == 11

    def test_solve_all_zeros(self):
        """Test when all targets are zero (should be 0 presses)."""
        targets = [0, 0, 0]
        buttons = [[0], [1], [2]]

        min_presses = solve_machine_part2(targets, buttons)
        assert min_presses == 0

    def test_solve_simple_case(self):
        """Test a simple case with one button affecting one counter."""
        targets = [5, 0, 0]
        buttons = [[0], [1], [2]]

        min_presses = solve_machine_part2(targets, buttons)
        assert min_presses == 5


class TestPart2:
    """Test part 2 solution."""

    def test_example(self):
        """Test with the example from problem description."""
        machines = parse_part2(EXAMPLE_INPUT)
        result = part2(machines)

        # 10 + 12 + 11 = 33
        assert result == 33

    def test_single_machine_all_zeros(self):
        """Test with a single machine where all targets are zero."""
        input_text = "[...] (0) (1) (2) {0,0,0}"
        machines = parse_part2(input_text)
        result = part2(machines)

        assert result == 0

    def test_multiple_simple_machines(self):
        """Test with multiple simple machines."""
        input_text = """[#] (0) {5}
[##] (0) (1) {3,4}"""
        machines = parse_part2(input_text)
        result = part2(machines)

        # Machine 1: 5 presses of button (0)
        # Machine 2: 3 presses of button (0) + 4 presses of button (1) = 7
        # Total: 5 + 7 = 12
        assert result == 12
