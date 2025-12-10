"""Tests for Day 10 solution"""

from .day10 import parse, part1, solve_machine, build_augmented_matrix, gaussian_elimination_gf2
from .input import EXAMPLE_INPUT


class TestParse:
    def test_parse_example(self):
        """Test parsing the example input."""
        machines = parse(EXAMPLE_INPUT)
        assert len(machines) == 3
        
        target1, buttons1, joltage1 = machines[0]
        assert target1 == [0, 1, 1, 0]
        assert buttons1 == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        assert joltage1 == [3, 5, 4, 7]
        
        target2, buttons2, joltage2 = machines[1]
        assert target2 == [0, 0, 0, 1, 0]
        assert buttons2 == [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        assert joltage2 == [7, 5, 12, 7, 2]
        
        target3, buttons3, joltage3 = machines[2]
        assert target3 == [0, 1, 1, 1, 0, 1]
        assert buttons3 == [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        assert joltage3 == [10, 11, 11, 5, 10, 5]
    
    def test_parse_single_machine(self):
        """Test parsing a single machine."""
        input_text = "[#.] (0) (1) {5,10}"
        machines = parse(input_text)
        assert len(machines) == 1
        target, buttons, joltage = machines[0]
        assert target == [1, 0]
        assert buttons == [[0], [1]]
        assert joltage == [5, 10]
    
    def test_parse_empty_buttons(self):
        """Test parsing with empty button list."""
        input_text = "[#] () {1}"
        machines = parse(input_text)
        assert len(machines) == 1
        target, buttons, joltage = machines[0]
        assert target == [1]
        assert buttons == [[]]
        assert joltage == [1]
    
    def test_parse_empty_input(self):
        """Test parsing empty input."""
        machines = parse("")
        assert machines == []
    
    def test_parse_multidigit_light_indices(self):
        """Test parsing buttons with multi-digit light indices."""
        input_text = "[###] (0,10,20) (5) {1,2,3}"
        machines = parse(input_text)
        assert len(machines) == 1
        target, buttons, joltage = machines[0]
        assert buttons[0] == [0, 10, 20]
        assert joltage == [1, 2, 3]


class TestSolveMachine:
    def test_machine_1_from_example(self):
        """Test first machine from example: expected result is 2."""
        target = [0, 1, 1, 0]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        result = solve_machine(target, buttons)
        assert result == 2
    
    def test_machine_2_from_example(self):
        """Test second machine from example: expected result is 3."""
        target = [0, 0, 0, 1, 0]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        result = solve_machine(target, buttons)
        assert result == 3
    
    def test_machine_3_from_example(self):
        """Test third machine from example: expected result is 2."""
        target = [0, 1, 1, 1, 0, 1]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        result = solve_machine(target, buttons)
        assert result == 2
    
    def test_simple_one_button(self):
        """Test simple case with one button."""
        target = [1]
        buttons = [[0]]
        result = solve_machine(target, buttons)
        assert result == 1
    
    def test_simple_two_buttons_one_light(self):
        """Test two buttons affecting the same light."""
        target = [1]
        buttons = [[0], [0]]
        result = solve_machine(target, buttons)
        assert result == 1
    
    def test_no_buttons_all_off(self):
        """Test when all lights should be off and no buttons available."""
        target = [0, 0]
        buttons = []
        result = solve_machine(target, buttons)
        assert result == 0
    
    def test_no_buttons_need_on(self):
        """Test when lights need to be on but no buttons available."""
        target = [1]
        buttons = []
        result = solve_machine(target, buttons)
        assert result == -1


class TestBuildAugmentedMatrix:
    def test_simple_matrix(self):
        """Test building augmented matrix for simple case."""
        target = [1, 0]
        buttons = [[0], [1]]
        matrix = build_augmented_matrix(2, buttons, target)
        assert len(matrix) == 2
        assert matrix[0] == [1, 0, 1]
        assert matrix[1] == [0, 1, 0]
    
    def test_button_affects_multiple_lights(self):
        """Test button that affects multiple lights."""
        target = [1, 1]
        buttons = [[0, 1]]
        matrix = build_augmented_matrix(2, buttons, target)
        assert matrix[0] == [1, 1]
        assert matrix[1] == [1, 1]
    
    def test_multiple_buttons(self):
        """Test matrix with multiple buttons."""
        target = [1, 0, 1]
        buttons = [[0, 2], [1], [0]]
        matrix = build_augmented_matrix(3, buttons, target)
        assert matrix[0] == [1, 0, 1, 1]
        assert matrix[1] == [0, 1, 0, 0]
        assert matrix[2] == [1, 0, 0, 1]


class TestGaussianElimination:
    def test_simple_system(self):
        """Test Gaussian elimination on simple system."""
        matrix = [
            [1, 0, 1],
            [0, 1, 0]
        ]
        result = gaussian_elimination_gf2(matrix)
        assert result is True
    
    def test_inconsistent_system(self):
        """Test inconsistent system (no solution)."""
        matrix = [
            [0, 0, 1],
            [1, 1, 0]
        ]
        result = gaussian_elimination_gf2(matrix)
        assert result is False
    
    def test_dependent_equations(self):
        """Test system with dependent equations."""
        matrix = [
            [1, 1, 1],
            [1, 1, 1]
        ]
        result = gaussian_elimination_gf2(matrix)
        assert result is True


class TestPart1:
    def test_example_input(self):
        """Test part1 with the example input."""
        machines = parse(EXAMPLE_INPUT)
        result = part1(machines)
        assert result == 7
    
    def test_single_machine(self):
        """Test part1 with single machine."""
        input_text = "[#] (0) {1,2}"
        machines = parse(input_text)
        result = part1(machines)
        assert result == 1
    
    def test_multiple_machines(self):
        """Test part1 with multiple simple machines."""
        input_text = "[#] (0) {1,2}\n[##] (0,1) {3,4}"
        machines = parse(input_text)
        result = part1(machines)
        assert result == 2


class TestSolveMachinePart2:
    def test_machine_1_from_example(self):
        """Test first machine from example (part2): expected result is 10."""
        machines = parse(EXAMPLE_INPUT)
        from .day10 import solve_machine_part2
        _, buttons, joltage = machines[0]
        result = solve_machine_part2(joltage, buttons)
        assert result == 10
    
    def test_machine_2_from_example(self):
        """Test second machine from example (part2): expected result is 12."""
        machines = parse(EXAMPLE_INPUT)
        from .day10 import solve_machine_part2
        _, buttons, joltage = machines[1]
        result = solve_machine_part2(joltage, buttons)
        assert result == 12
    
    def test_machine_3_from_example(self):
        """Test third machine from example (part2): expected result is 11."""
        machines = parse(EXAMPLE_INPUT)
        from .day10 import solve_machine_part2
        _, buttons, joltage = machines[2]
        result = solve_machine_part2(joltage, buttons)
        assert result == 11
    
    def test_simple_single_counter(self):
        """Test simple case with one counter."""
        from .day10 import solve_machine_part2
        targets = [5]
        buttons = [[0]]
        result = solve_machine_part2(targets, buttons)
        assert result == 5
    
    def test_multiple_buttons_same_counter(self):
        """Test multiple buttons affecting the same counter."""
        from .day10 import solve_machine_part2
        targets = [5]
        buttons = [[0], [0]]
        result = solve_machine_part2(targets, buttons)
        assert result == 5


class TestPart2:
    def test_example_input(self):
        """Test part2 with the example input."""
        from .day10 import part2
        machines = parse(EXAMPLE_INPUT)
        result = part2(machines)
        assert result == 33
    
    def test_single_machine(self):
        """Test part2 with single machine."""
        from .day10 import part2
        input_text = "[##] (0) (1) {5,7}"
        machines = parse(input_text)
        result = part2(machines)
        assert result == 12
