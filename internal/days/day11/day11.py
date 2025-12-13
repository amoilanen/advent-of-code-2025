"""Day 11: Device Path Counting

Part 1: Count all paths from 'you' to 'out' through a device network.
Each device can have multiple outputs, and data flows forward only (no backwards flow).
"""

from typing import Dict, List, Set, FrozenSet, Tuple
from functools import lru_cache


def parse(input_text: str) -> Dict[str, List[str]]:
    """
    Parse the input text into a graph representation.

    Each line format: "device_name: output1 output2 ..."

    Args:
        input_text: The input containing device connections

    Returns:
        Dictionary mapping device name to list of connected devices
    """
    graph = {}

    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue

        # Split on colon to separate device from its outputs
        parts = line.split(':')
        if len(parts) != 2:
            continue

        device = parts[0].strip()
        outputs = parts[1].strip().split()

        graph[device] = outputs

    return graph


def count_paths(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count all paths from start to end in the graph using DFS.

    Uses depth-first search to enumerate all possible paths.
    Tracks visited nodes in current path to avoid cycles.

    Args:
        graph: Dictionary mapping device to list of connected devices
        start: Starting device name
        end: Target device name

    Returns:
        Total number of paths from start to end
    """
    def dfs(current: str, visited: Set[str]) -> int:
        # Base case: reached the target
        if current == end:
            return 1

        # If this device has no outputs, no paths
        if current not in graph:
            return 0

        # Count paths through all outputs
        path_count = 0
        for next_device in graph[current]:
            # Avoid cycles by not revisiting nodes in current path
            if next_device not in visited:
                visited.add(next_device)
                path_count += dfs(next_device, visited)
                visited.remove(next_device)

        return path_count

    # Start DFS with initial node in visited set
    return dfs(start, {start})


def count_paths_with_required(
    graph: Dict[str, List[str]],
    start: str,
    end: str,
    required: Set[str]
) -> int:
    """
    Count all paths from start to end that visit all required nodes.

    Uses memoized DFS to efficiently count paths. Assumes DAG (no cycles).
    Only counts paths that visit all required nodes before reaching end.

    Args:
        graph: Dictionary mapping device to list of connected devices
        start: Starting device name
        end: Target device name
        required: Set of device names that must be visited

    Returns:
        Total number of paths from start to end that visit all required nodes
    """
    required_frozen = frozenset(required)

    # Memoization cache: (current, required_visited_frozenset) -> count
    cache: Dict[Tuple[str, FrozenSet[str]], int] = {}

    def dfs(current: str, required_visited: FrozenSet[str]) -> int:
        # Check cache
        cache_key = (current, required_visited)
        if cache_key in cache:
            return cache[cache_key]

        # Base case: reached the target
        if current == end:
            result = 1 if required_visited == required_frozen else 0
            cache[cache_key] = result
            return result

        # If this device has no outputs, no paths
        if current not in graph:
            cache[cache_key] = 0
            return 0

        # Count paths through all outputs
        path_count = 0
        for next_device in graph[current]:
            new_required = required_visited | ({next_device} if next_device in required else frozenset())
            path_count += dfs(next_device, new_required)

        cache[cache_key] = path_count
        return path_count

    # Track if start is a required node
    initial_required = frozenset({start}) if start in required else frozenset()

    # Start DFS
    return dfs(start, initial_required)


def part1(graph: Dict[str, List[str]]) -> int:
    """
    Count all paths from 'you' to 'out'.

    Args:
        graph: Dictionary mapping device to list of connected devices

    Returns:
        Number of paths from 'you' to 'out'
    """
    return count_paths(graph, 'you', 'out')


def part2(graph: Dict[str, List[str]]) -> int:
    """
    Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'.

    Args:
        graph: Dictionary mapping device to list of connected devices

    Returns:
        Number of paths from 'svr' to 'out' that visit both 'dac' and 'fft'
    """
    return count_paths_with_required(graph, 'svr', 'out', {'dac', 'fft'})
