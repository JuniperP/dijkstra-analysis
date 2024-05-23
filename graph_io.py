"""This module contains functions for reading and writing graphs to files.

Author: Juniper Pasternak
Date: 2024-05-10
"""

import json
from structures import Node, Edge, Graph, matrix_to_graph


def read_adjacency_list(filename: str) -> Graph:
    """Read an adjacency list representing a graph from a `.adj` file.

    `.adj` files are plaintext files where each line represents a node, followed by its
    neighbors (separated by tabs). Neighbors should be in the form `node_name,weight`.

    For example, the following file represents a graph with nodes `A`, `B`, and `C`:
    ```
    A	B,1	C,3
    B	C,2
    C
    ```
    (Note that the separators here are tabs, not spaces.)

    This file represents the following graph:
    ```
    A -> B (1), C (3)
    B -> C (2)
    ```

    Args:
        filename (str): the name of the file to be read

    Returns:
        Graph: the graph read from the file
    """
    with open(filename, "r", encoding="utf-8") as file:
        # Split each line into a list of the node_name and its neighbors
        # Omit lines with only whitespace
        adj_lists: list[list[str]] = [
            line.strip().split("\t") for line in file if line.strip()
        ]

    # Create nodes from the adjacency list and store them in a list and dictionary
    nodes_list: list[Node] = []
    nodes_dict: dict[str, Node] = {}
    for node_name, *_ in adj_lists:
        node = Node(node_name)
        nodes_list.append(node)
        nodes_dict[node_name] = node

    # Create edges from the adjacency list
    edges: list[Edge] = []
    for node_name, *neighbors in adj_lists:
        tail = nodes_dict[node_name]

        # Add edges for each neighbor in the tail's adjacency list
        for neighbor in neighbors:
            neighbor_name, weight = neighbor.split(",")
            head = nodes_dict[neighbor_name]
            edge = Edge(tail, head, float(weight))
            edges.append(edge)

    return Graph(nodes_list, edges)


def write_adjacency_list(graph: Graph, filename: str) -> None:
    """Write a graph to a `.adj` file as an adjacency list.

    `.adj` files are plaintext files where each line represents a node, followed by its
    neighbors (separated by tabs). Neighbors should be in the form `node_name,weight`.

    For example, the following file represents a graph with nodes `A`, `B`, and `C`:
    ```
    A	B,1	C,3
    B	C,2
    C
    ```
    (Note that the separators here are tabs, not spaces.)

    This file represents the following graph:
    ```
    A -> B (1), C (3)
    B -> C (2)
    ```

    Args:
        graph (Graph): the graph to be written
        filename (str): the name of the file to be written (including the extension)
    """
    with open(filename, "w", encoding="utf-8") as file:
        for node in graph.nodes:
            neighbors = "\t".join(
                f"{edge.head.data},{edge.weight}" for edge in node.outbound
            )
            file.write(f"{node.data}\t{neighbors}\n")


def read_matrix_file(filename: str) -> Graph:
    """Read a matrix representing a graph from a JSON file.

    Args:
        filename (str): the name of the file to be read

    Returns:
        Graph: the graph read from the file
    """
    with open(filename, "r", encoding="utf-8") as file:
        matrix = json.load(file)
    return matrix_to_graph(matrix)


def write_matrix_file(graph: Graph, filename: str) -> None:
    """Write a graph to a JSON file as a matrix.

    Args:
        graph (Graph): the graph to be written
        filename (str): the name of the file to be written (including the extension)
    """
    matrix = graph.to_matrix()
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(matrix, file)
