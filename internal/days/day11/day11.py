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


def count_paths(
    graph: Dict[str, List[str]],
    start: str,
    end: str,
    must_visit: Set[str] = None
) -> int:
    """
    Count all paths from start to end, optionally requiring certain nodes to be visited.

    Uses memoized DFS to efficiently count paths when must_visit is specified.
    For simple path counting (no must_visit), uses DFS with cycle detection.
    If must_visit is provided, only counts paths that visit all specified nodes.

    Args:
        graph: Dictionary mapping device to list of connected devices
        start: Starting device name
        end: Target device name
        must_visit: Optional set of device names that must be visited on each path

    Returns:
        Total number of paths from start to end (visiting all must_visit nodes if specified)
    """
    # Convert must_visit to frozenset for hashability in cache
    must_visit_nodes = frozenset(must_visit) if must_visit else frozenset()

    # Memoization cache: (current_node, nodes_found_so_far) -> path_count
    cache: Dict[Tuple[str, FrozenSet[str]], int] = {}

    def dfs_with_required(current: str, nodes_found: FrozenSet[str], visited: Set[str]) -> int:
        """
        DFS helper that counts paths while tracking which must_visit nodes have been found.

        Args:
            current: Current node in the path
            nodes_found: Set of must_visit nodes we've encountered so far
            visited: Set of nodes in the current path (for cycle detection)
        """
        # Check cache (only when tracking required nodes)
        if must_visit_nodes:
            cache_key = (current, nodes_found)
            if cache_key in cache:
                return cache[cache_key]

        # Base case: reached the target
        if current == end:
            # Only count this path if we've found all required nodes
            result = 1 if nodes_found == must_visit_nodes else 0
            if must_visit_nodes:
                cache[(current, nodes_found)] = result
            return result

        # If this device has no outputs, no paths
        if current not in graph:
            if must_visit_nodes:
                cache[(current, nodes_found)] = 0
            return 0

        # Count paths through all outputs
        path_count = 0
        for next_device in graph[current]:
            # Avoid cycles by not revisiting nodes in current path
            if next_device in visited:
                continue

            # Update nodes_found if next_device is one we must visit
            updated_nodes_found = (
                nodes_found | {next_device}
                if next_device in must_visit_nodes
                else nodes_found
            )

            # Add to visited set for cycle detection
            visited.add(next_device)
            path_count += dfs_with_required(next_device, updated_nodes_found, visited)
            visited.remove(next_device)

        if must_visit_nodes:
            cache[(current, nodes_found)] = path_count
        return path_count

    # Initialize nodes_found with start if it's in must_visit
    initial_nodes_found = frozenset({start}) if start in must_visit_nodes else frozenset()

    # Start DFS with start node in visited set
    return dfs_with_required(start, initial_nodes_found, {start})


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
    return count_paths(graph, 'svr', 'out', {'dac', 'fft'})
