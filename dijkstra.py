"""This module offers two different implementations of Dijkstra's algorithm.

The first implementation is a simple version that finds repeatedly finds the edge that
minimizes the length of the head node, requiring `O(m * n)` time complexity.

The second implementation is a more efficient version that uses a priority queue to
store the edges that need to be checked, requiring `O(m * log m)` time complexity.

Author: Juniper Pasternak
Date: 2024-05-12
"""

import math
import logging
from typing import Optional
from heapq import heappop, heappush
from structures import Node, Edge, Graph


class OpsTracker:
    """A static class for tracking the number of operations in each implementation.
    
    Attributes:
        simple_ops (int): the number of operations in the simple implementation
        heap_ops (float): the number of operations in the heap implementation
    """

    simple_ops: int = 0
    heap_ops: float = 0  # Use a float to allow for better logarithmic approximations

    @staticmethod
    def reset() -> None:
        """Reset the number of operations for each implementation."""
        OpsTracker.simple_ops = 0
        OpsTracker.heap_ops = 0

    @staticmethod
    def incr_simple(amount: int = 1) -> None:
        """Increment the number of operations for the simple implementation.
        
        Args:
            amount (int, optional): the number of operations to increment by; defaults to 1
        """
        OpsTracker.simple_ops += amount

    @staticmethod
    def incr_heap(amount: int = 1) -> None:
        """Increment the number of operations for the heap implementation.
        
        Args:
            amount (int, optional): the number of operations to increment by; defaults to 1
        """
        OpsTracker.heap_ops += amount

    @staticmethod
    def add_heap_op(heap_size: int) -> None:
        """Add the number of operations for a heap operation in the heap implementation.

        The number of operations is approximated as `log2(n) + 1`, where `n` is the number of
        elements in the heap.
        
        Args:
            heap_size (int): the number of elements in the heap
        """
        OpsTracker.heap_ops += math.log2(heap_size) + 1

    @staticmethod
    def print_operations() -> None:
        """Print the number of operations for each implementation."""
        print(f"Simple implementation operations: {OpsTracker.simple_ops}")
        print(f"Heap implementation operations: {round(OpsTracker.heap_ops)}")


def simple_shortest_path(graph: Graph, start: Node) -> None:
    """Simple implementation of Dijkstra's algorithm.

    Given a weighted directed graph and a starting node, this function calculates the
    shortest path to each node connected from the starting node. These values are stored
    in the length attribute of each node. Nodes that are not reachable from
    the starting node will have a length of math.inf.

    Args:
        graph (Graph): the graph to be traversed
        start (Node): the starting node
    """

    def get_best_edge(visited: list[Node]) -> tuple[Optional[Edge], float]:
        """Get the edge that minimizes the length of the head node.

        This is a helper function for the main algorithm that finds the edge that
        checks all edges from visited nodes to unvisited nodes and returns the edge
        that minimizes the length of the head node along with that weight.

        If there are no more edges to take, the function will return (None, math.inf).

        Args:
            visited (list[Node]): the list of visited nodes

        Returns:
            tuple[Optional[Edge], float]: the best edge and its length
        """
        OpsTracker.incr_simple(2)
        best_edge: Optional[Edge] = None
        best_criterion: float = math.inf

        for node in visited:
            OpsTracker.incr_simple()
            for edge in node.outbound:
                # Check edges such that the tail is visited and the head is not
                if id(edge.head) not in (id(x) for x in visited):
                    OpsTracker.incr_simple(2)
                    # Calculate the hypothetical length of the head node
                    criterion = edge.tail.length + edge.weight

                    # Update best edge and criterion if the current edge is better
                    if criterion < best_criterion:
                        OpsTracker.incr_simple(2)
                        best_edge = edge
                        best_criterion = criterion

        return best_edge, best_criterion

    OpsTracker.incr_simple(2)
    visited = [start]

    # Set starting weight to 0 and all others to infinity
    start.length = 0
    for node in graph.nodes:
        OpsTracker.incr_simple()
        if node is not start:
            OpsTracker.incr_simple()
            node.length = math.inf

    # Keep adding the node that minimizes the length to the visited list
    # until there are no more edges to take to new nodes
    while True:
        next_edge, weight = get_best_edge(visited)
        logging.debug("Currently visited nodes: %s", visited)
        logging.debug("Next edge to take: %s with weight %s", next_edge, weight)

        OpsTracker.incr_simple()
        if next_edge is None:  # There are no more edges to take
            break

        # Add the head node to the visited list and update its length
        OpsTracker.incr_simple(2)
        visited.append(next_edge.head)
        next_edge.head.length = weight


def heap_shortest_path(graph: Graph, start: Node) -> None:
    """Efficient implementation of Dijkstra's algorithm using a priority queue.

    Given a weighted directed graph and a starting node, this function calculates the
    shortest path to each node connected from the starting node. These values are stored
    in the length attribute of each node. Nodes that are not reachable from
    the starting node will have a length of math.inf.

    Args:
        graph (Graph): the graph to be traversed
        start (Node): the starting node
    """

    def heap_str(heap: list[Node]) -> str:
        """Return a string representation of the heap for debugging purposes."""
        return f"[{', '.join(f"(N{node.data}:{int(node.length)})" for node in heap)}]"

    OpsTracker.incr_heap(3)
    # Set starting weight to 0 and all others to infinity
    start.length = 0
    for node in graph.nodes:
        OpsTracker.incr_heap()
        if node is not start:
            OpsTracker.incr_heap()
            node.length = math.inf

    visited = []
    heap = [start]

    while len(heap) > 0:
        logging.debug("Currently visited nodes: %s", visited)
        logging.debug("Heap: %s", heap_str(heap))

        # Get the node with the smallest length from the heap
        OpsTracker.add_heap_op(len(heap))
        current = heappop(heap)

        # Skip if the node has already been visited
        OpsTracker.incr_heap()
        if id(current) in (id(x) for x in visited):
            continue

        OpsTracker.incr_heap()
        visited.append(current)

        for edge in current.outbound:
            OpsTracker.incr_heap(3)
            # Calculate the hypothetical length of the head node
            criterion = current.length + edge.weight

            # Update the head node's length if the criterion is better
            if criterion < edge.head.length:
                OpsTracker.incr_heap()
                edge.head.length = criterion

            # Add the head node to the heap if it hasn't been visited yet
            if edge.head not in visited:
                OpsTracker.add_heap_op(max(1, len(heap))) # Min of 1 to avoid log(0)
                heappush(heap, edge.head)
