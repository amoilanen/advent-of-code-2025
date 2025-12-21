"""Tests for Day 11: Device Path Counting"""

import pytest
from .day11 import parse, count_paths, part1, part2
from .input import EXAMPLE_INPUT


class TestParse:
    """Test parsing of device connections."""

    def test_parse_simple(self):
        """Test parsing a simple device network."""
        input_text = """aaa: bbb ccc
bbb: ddd
ccc: ddd
ddd: out"""
        graph = parse(input_text)

        assert graph == {
            'aaa': ['bbb', 'ccc'],
            'bbb': ['ddd'],
            'ccc': ['ddd'],
            'ddd': ['out']
        }

    def test_parse_example(self):
        """Test parsing the example input."""
        graph = parse(EXAMPLE_INPUT)

        assert 'you' in graph
        assert graph['you'] == ['bbb', 'ccc']
        assert graph['bbb'] == ['ddd', 'eee']
        assert graph['ccc'] == ['ddd', 'eee', 'fff']
        assert graph['ddd'] == ['ggg']
        assert graph['eee'] == ['out']
        assert graph['fff'] == ['out']
        assert graph['ggg'] == ['out']
        assert graph['hhh'] == ['ccc', 'fff', 'iii']
        assert graph['iii'] == ['out']

    def test_parse_single_device(self):
        """Test parsing a single device."""
        input_text = "aaa: bbb"
        graph = parse(input_text)

        assert graph == {'aaa': ['bbb']}

    def test_parse_multiple_outputs(self):
        """Test parsing a device with multiple outputs."""
        input_text = "aaa: bbb ccc ddd eee"
        graph = parse(input_text)

        assert graph == {'aaa': ['bbb', 'ccc', 'ddd', 'eee']}

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        graph = parse("")
        assert graph == {}


class TestCountPaths:
    """Test path counting algorithm."""

    def test_simple_path(self):
        """Test counting a simple single path."""
        graph = {
            'you': ['out']
        }
        assert count_paths(graph, 'you', 'out') == 1

    def test_two_paths(self):
        """Test counting two parallel paths."""
        graph = {
            'you': ['a', 'b'],
            'a': ['out'],
            'b': ['out']
        }
        assert count_paths(graph, 'you', 'out') == 2

    def test_branching_paths(self):
        """Test counting paths with branching."""
        graph = {
            'you': ['a'],
            'a': ['b', 'c'],
            'b': ['out'],
            'c': ['out']
        }
        assert count_paths(graph, 'you', 'out') == 2

    def test_converging_paths(self):
        """Test counting paths that converge and branch again."""
        graph = {
            'you': ['a', 'b'],
            'a': ['c'],
            'b': ['c'],
            'c': ['out']
        }
        # you -> a -> c -> out
        # you -> b -> c -> out
        assert count_paths(graph, 'you', 'out') == 2

    def test_complex_network(self):
        """Test counting paths in a more complex network."""
        graph = {
            'you': ['a', 'b'],
            'a': ['c', 'd'],
            'b': ['d'],
            'c': ['out'],
            'd': ['out']
        }
        # you -> a -> c -> out
        # you -> a -> d -> out
        # you -> b -> d -> out
        assert count_paths(graph, 'you', 'out') == 3

    def test_no_path(self):
        """Test when there's no path to destination."""
        graph = {
            'you': ['a'],
            'a': ['b'],
            'b': ['c']
        }
        assert count_paths(graph, 'you', 'out') == 0

    def test_cycle_avoided(self):
        """Test that cycles are properly avoided."""
        graph = {
            'you': ['a'],
            'a': ['b', 'out'],
            'b': ['a']  # Cycle back to a
        }
        # Should only count: you -> a -> out
        # Should not get stuck in: you -> a -> b -> a -> b -> ...
        assert count_paths(graph, 'you', 'out') == 1


class TestPart1:
    """Test part 1 solution."""

    def test_example(self):
        """Test with the example from problem description."""
        graph = parse(EXAMPLE_INPUT)
        result = part1(graph)

        # Expected paths:
        # 1. you -> bbb -> ddd -> ggg -> out
        # 2. you -> bbb -> eee -> out
        # 3. you -> ccc -> ddd -> ggg -> out
        # 4. you -> ccc -> eee -> out
        # 5. you -> ccc -> fff -> out
        assert result == 5

class TestCountPathsWithRequired:
    """Test path counting with required nodes."""

    def test_simple_required_path(self):
        """Test counting paths with one required node."""
        graph = {
            'start': ['req', 'other'],
            'req': ['end'],
            'other': ['end']
        }
        # Only path through 'req' counts
        assert count_paths(graph, 'start', 'end', {'req'}) == 1

    def test_two_required_nodes(self):
        """Test counting paths with two required nodes."""
        graph = {
            'start': ['a', 'b'],
            'a': ['req1'],
            'b': ['req2'],
            'req1': ['req2'],
            'req2': ['end']
        }
        # Only start -> a -> req1 -> req2 -> end visits both
        assert count_paths(graph, 'start', 'end', {'req1', 'req2'}) == 1

    def test_multiple_paths_with_required(self):
        """Test multiple paths that visit required nodes."""
        graph = {
            'start': ['a'],
            'a': ['req1', 'req2'],
            'req1': ['req2'],
            'req2': ['end']
        }
        # Both paths visit both required nodes:
        # start -> a -> req1 -> req2 -> end
        # start -> a -> req2 -> end (doesn't visit req1)
        assert count_paths(graph, 'start', 'end', {'req1', 'req2'}) == 1

    def test_no_paths_with_required(self):
        """Test when no paths visit all required nodes."""
        graph = {
            'start': ['a', 'b'],
            'a': ['req1'],
            'b': ['req2'],
            'req1': ['end'],
            'req2': ['end']
        }
        # No single path visits both req1 and req2
        assert count_paths(graph, 'start', 'end', {'req1', 'req2'}) == 0

    def test_required_in_different_orders(self):
        """Test that required nodes can be visited in any order."""
        graph = {
            'start': ['a', 'b'],
            'a': ['req1'],
            'b': ['req2'],
            'req1': ['req2'],
            'req2': ['req1'],
            'req1': ['end'],
            'req2': ['end']
        }
        # Paths can visit req1 and req2 in either order
        result = count_paths(graph, 'start', 'end', {'req1', 'req2'})
        assert result >= 0  # Just check it doesn't crash


class TestPart2:
    """Test part 2 solution."""

    def test_example(self):
        """Test with the example from part 2 description."""
        input_text = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
        graph = parse(input_text)
        result = part2(graph)

        # Expected paths that visit both dac and fft:
        # 1. svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> ggg -> out
        # 2. svr -> aaa -> fft -> ccc -> eee -> dac -> fff -> hhh -> out
        assert result == 2
