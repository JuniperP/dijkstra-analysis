"""This module contains the classes for an undirected graph data structure including:

- Node
- Edge
- Graph

Author: Juniper Pasternak
Date: 2024-05-10
"""

import math
import functools
from typing import Optional


@functools.total_ordering
class Node:
    """A node or vertex of an undirected graph represented by adjacency lists.

    Comparison operators are implemented based on the length of the node.

    Attributes:
        data (object, optional): the data stored in the node
        inbound (list[Edge]): a list of inbound edges to the node
        outbound (list[Edge]): a list of outbound edges from the node
        length (float): the length of the node from an arbitrary starting node
    """

    def __init__(self, data=None, length: float = math.inf) -> None:
        self.data = data
        self.inbound: list["Edge"] = []
        self.outbound: list["Edge"] = []
        self.length: float = length

    def add_inbound(self, edge: "Edge") -> None:
        """Add an inbound edge to the node.

        Args:
            edge (Edge): the edge to be added
        """
        self.inbound.append(edge)

    def add_outbound(self, edge: "Edge") -> None:
        """Add an outbound edge to the node.

        Args:
            edge (Edge): the edge to be added
        """
        self.outbound.append(edge)

    # Implement total ordering comparators based on length
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Node):
            return False
        return self.length == value.length

    def __lt__(self, value: object) -> bool:
        if not isinstance(value, Node):
            return False
        return self.length < value.length

    def __str__(self) -> str:
        return f"Node({self.data}, length={self.length})"

    def __repr__(self) -> str:
        return f"Node({self.data}, length={self.length})"


class Edge:
    """A weighted edge of an undirected graph represented by adjacency lists.

    Attributes:
        tail (Node): the tail node of the edge
        head (Node): the head node of the edge
        weight (float): the weight of the edge
    """

    def __init__(self, tail: Node, head: Node, weight: float) -> None:
        """Construct an edge between two nodes with a given weight.
        Automatically adds the edge to the tail and head nodes.

        Args:
            tail (Node): tail of the edge
            head (Node): head of the edge
            weight (float): the weight of the edge
        """
        self.tail: Node = tail
        self.head: Node = head
        self.weight: float = weight

        tail.add_outbound(self)
        head.add_inbound(self)

    def __str__(self) -> str:
        return f"Edge({self.tail}, {self.head}, {self.weight})"

    def __repr__(self) -> str:
        return f"Edge({self.tail}, {self.head}, {self.weight})"


class Graph:
    """A simple (without parallel edges) undirected graph represented by adjacency lists.

    Attributes:
        nodes (list[Node]): a list of nodes in the graph
        edges (list[Edge]): a list of edges in the graph
    """

    def __init__(
        self, nodes: Optional[list[Node]] = None, edges: Optional[list[Edge]] = None
    ) -> None:
        # Initialize empty lists if no nodes or edges are provided
        self.nodes: list[Node] = nodes or []
        self.edges: list[Edge] = edges or []

    def add_node(self, node: Node) -> None:
        """Add a node to the graph.

        Args:
            node (Node): the node to be added
        """
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph.

        Args:
            edge (Edge): the edge to be added
        """
        self.edges.append(edge)

    def print_adjacency_list(self) -> None:
        """Print the adjacency list of the graph.

        The adjacency list is printed in the following format:
        ```
        A [0] -> B (1), C (3)
        ```
        where `A` is the node data, `0` is the length of the node, and `B` and `C`
        are the neighbors of the node with the edge weights `1` and `3`.
        """
        for node in self.nodes:
            neighbors = ", ".join(
                f"{edge.head.data} ({edge.weight})" for edge in node.outbound
            )
            print(f"{node.data} [{node.length}] -> {neighbors}")

    def print_node_lengths(self) -> None:
        """Print the lengths of all nodes in the graph."""
        for node in self.nodes:
            print(f"Node [{node.data}]: {node.length}")

    def to_matrix(self) -> list[list[float]]:
        """Convert the graph to a 2D list representing the graph.

        Each row represents the tail node and each column represents the head node.
        The value at the intersection of a row and column is the weight of the edge
        connecting the tail node to the head node. If there is no edge connecting the
        tail node to the head node, the value is infinity.

        For example, given a graph with nodes [A, B, C] and edges [(A, B, 1), (B, C, 2)],
        the adjacency matrix would be:

        ```text
        [
            [inf, 1  , inf],
            [inf, inf, 2  ],
            [inf, inf, inf]
        ]
        ```

        Returns:
            List[List[float]]: a 2D list representing the graph
        """
        n = len(self.nodes)
        # Empty n x n matrix with all values set to infinity
        matrix = [[math.inf for _ in range(n)] for _ in range(n)]

        # Fill in the matrix with edge weights
        for edge in self.edges:
            row = self.nodes.index(edge.tail)  # Row = tail node index
            col = self.nodes.index(edge.head)  # Column = head node index
            matrix[row][col] = edge.weight

        return matrix

    def __str__(self) -> str:
        return f"Graph(nodes={self.nodes}, edges={self.edges})"

    def __repr__(self) -> str:
        return f"Graph(nodes={self.nodes}, edges={self.edges})"


def matrix_to_graph(matrix: list[list[float]]) -> Graph:
    """Convert a 2D list representing a graph to a Graph object.

    Each row represents the tail node and each column represents the head node.
    The value at the intersection of a row and column is the weight of the edge
    connecting the tail node to the head node. If there is no edge connecting the
    tail node to the head node, the value is infinity.

    The data of the nodes in the resulting graph will be the indices of the nodes.

    For example, given a 2D list:

    ```text
    [
        [inf, 1  , inf],
        [inf, inf, 2  ],
        [inf, inf, inf]
    ]
    ```

    The resulting graph would have nodes [A, B, C] and edges [(A, B, 1), (B, C, 2)],
    where A, B, and C are Node(index) with index 0 through 2.

    Args:
        matrix (List[List[float]]): a 2D list representing the graph

    Returns:
        Graph: a Graph object representing the graph
    """
    # Check if the matrix is square
    if not all(len(row) == len(matrix) for row in matrix):
        raise ValueError(
            f"matrix must be square (provided {len(matrix)}x{len(matrix[0])})"
        )

    # Make node data alphabetical based on index:
    # A = 0, B = 1, etc., or AA = 0, AB = 1, etc. depending on how many nodes there are
    n = len(matrix)
    nodes = [Node(i) for i in range(n)]
    edges = []

    # Create edges from the matrix
    for row in range(n):
        for col in range(n):
            if matrix[row][col] != math.inf:
                edges.append(Edge(nodes[row], nodes[col], matrix[row][col]))

    return Graph(nodes, edges)
