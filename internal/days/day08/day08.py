"""Day 8: Junction Box Circuits

The Elves need to connect junction boxes to form electrical circuits.
We connect the closest pairs and track circuit sizes using Union-Find.
"""

from typing import List, Tuple
import math


def parse(input_text: str) -> List[Tuple[int, int, int]]:
    """
    Parse the input text into a list of 3D coordinates.

    Args:
        input_text: The input containing junction box coordinates

    Returns:
        List of (x, y, z) tuples representing junction box positions
    """
    boxes = []
    for line in input_text.strip().split('\n'):
        if line.strip():
            x, y, z = map(int, line.strip().split(','))
            boxes.append((x, y, z))
    return boxes


def euclidean_distance(box1: Tuple[int, int, int], box2: Tuple[int, int, int]) -> float:
    """
    Calculate the Euclidean distance between two 3D points.

    Args:
        box1: First junction box (x, y, z)
        box2: Second junction box (x, y, z)

    Returns:
        Euclidean distance as a float
    """
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure for tracking circuits.

    Supports efficient union and find operations with path compression
    and union by size.
    """

    def __init__(self, n: int):
        """
        Initialize Union-Find with n elements.

        Args:
            n: Number of elements (junction boxes)
        """
        self.parent = list(range(n))  # Each element is its own parent initially
        self.size = [1] * n  # Size of each set (circuit)
        self.num_circuits = n  # Track number of separate circuits

    def find(self, x: int) -> int:
        """
        Find the root of element x with path compression (iterative).

        Uses a two-pass approach: first finds the root, then compresses
        the path by making all nodes point directly to the root.
        This avoids recursive overhead and ensures each node is updated
        exactly once.

        Args:
            x: Element to find root of

        Returns:
            Root of the set containing x
        """
        # First pass: find the root
        root = x
        while self.parent[root] != root:
            root = self.parent[root]

        # Second pass: compress the path
        while self.parent[x] != root:
            next_node = self.parent[x]
            self.parent[x] = root  # Point directly to root
            x = next_node

        return root

    def union(self, x: int, y: int) -> bool:
        """
        Unite the sets containing x and y.

        Uses union by size: attach the smaller tree to the larger tree.
        This keeps trees balanced and ensures logarithmic depth.

        Args:
            x: First element
            y: Second element

        Returns:
            True if sets were merged, False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            # Already in the same set
            return False

        # Union by size: attach smaller tree to larger tree
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

        # Decrement circuit count since we merged two circuits
        self.num_circuits -= 1

        return True

    def get_circuit_sizes(self) -> List[int]:
        """
        Get the sizes of all circuits.

        Returns:
            List of circuit sizes
        """
        # Find all unique roots and their sizes
        circuits = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in circuits:
                circuits[root] = self.size[root]
        return list(circuits.values())


def _generate_sorted_pairs(boxes: List[Tuple[int, int, int]]) -> List[Tuple[float, int, int]]:
    """
    Generate all pairs of boxes sorted by distance.

    Args:
        boxes: List of junction box coordinates

    Returns:
        List of (distance, index1, index2) tuples sorted by distance
    """
    n = len(boxes)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(boxes[i], boxes[j])
            pairs.append((dist, i, j))
    pairs.sort()
    return pairs


def _connect_boxes(
    boxes: List[Tuple[int, int, int]],
    pairs: List[Tuple[float, int, int]],
    max_connections: int = None
) -> UnionFind:
    """
    Connect junction boxes using Union-Find.

    Args:
        boxes: List of junction box coordinates
        pairs: Sorted list of (distance, index1, index2) tuples
        max_connections: Maximum number of connections to make (None = unlimited)

    Returns:
        UnionFind structure with connections made
    """
    n = len(boxes)
    uf = UnionFind(n)
    connections_attempted = 0

    for dist, i, j in pairs:
        if max_connections is not None and connections_attempted >= max_connections:
            break
        uf.union(i, j)
        connections_attempted += 1

    return uf


def part1(boxes: List[Tuple[int, int, int]], num_connections: int = 1000) -> int:
    """
    Connect the closest pairs of junction boxes and find the product of
    the three largest circuit sizes.

    Args:
        boxes: List of junction box coordinates
        num_connections: Number of closest pairs to connect (default: 1000)

    Returns:
        Product of the three largest circuit sizes
    """
    n = len(boxes)

    # Handle edge cases
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Generate sorted pairs and connect boxes
    pairs = _generate_sorted_pairs(boxes)
    uf = _connect_boxes(boxes, pairs, max_connections=num_connections)

    # Get all circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)

    # Calculate product of three largest
    result = 1
    for i in range(min(3, len(circuit_sizes))):
        result *= circuit_sizes[i]

    return result


def part2(boxes: List[Tuple[int, int, int]]) -> int:
    """
    Connect junction boxes until they're all in one circuit, then return
    the product of X coordinates of the last two boxes connected.

    Args:
        boxes: List of junction box coordinates

    Returns:
        Product of X coordinates of the last connection
    """
    n = len(boxes)

    # Handle edge cases
    if n == 0:
        return 0
    if n == 1:
        return boxes[0][0] ** 2

    # Generate sorted pairs
    pairs = _generate_sorted_pairs(boxes)

    # Connect boxes until all are in one circuit
    uf = UnionFind(n)
    last_i, last_j = 0, 0

    for dist, i, j in pairs:
        if uf.union(i, j):
            last_i, last_j = i, j
            if uf.num_circuits == 1:
                break

    # Return product of X coordinates
    return boxes[last_i][0] * boxes[last_j][0]
