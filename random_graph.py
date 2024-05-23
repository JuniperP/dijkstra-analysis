"""This module offers functions for generating random graphs.

The interactive creation function allows the user to create a highly configurable
random graphs with different densities and sizes in bulk.

These graphs are saved as adjacency lists in separate files within density folders.

This script runs the interactive creation function when executed as a standalone script.

Author: Juniper Pasternak
Date: 2024-05-13
"""

import os
import math
import random
import logging
from typing import Optional, Callable
from structures import Graph, Node, Edge
from graph_io import write_adjacency_list

HELP_MSG = """
Random Graph Mass Creation Help
-------------------------------
The interactive mass creation of random graphs allows you to create a
configurable amount of random graphs with different densities and sizes.

The user is prompted for the following inputs:

- The primary folder to save the graphs to.
    This folder will contain subfolders for each density group.
    Example: 'graphs' will create a folder 'graphs' with subfolders.

- The node counts of the graphs to be created.
    These node counts are comma-separated.
    Example: '10, 20, 30' will create graphs with 10, 20, and 30 nodes.

- The densities of the graphs to be created.
    These densities are comma-separated and represent the ratio of the number
    of edges to the maximum possible number of edges. The user may enter
    a python evaluable math expression to generate a range of densities.
    The expression expects the variable 'n' for the number of nodes.
    Use 'math' for mathematical functions: e.g. 'math.log(n) / n'.
    Example: '0.1, 0.2, 0.3' will create graphs with 10%, 20%, and 30% density.

- How many graphs to create for each size within the density group.
    Example: '5' will create 5 graphs for each size within the density group.

- The range of edge weights to be generated.
    These weights are integers, comma-separated, inclusive,
    and are used to generate random edge weights.
    Example: '1, 10' will generate edge weights from 1 to 10.

"""


def interactive_creation() -> None:
    """Mass create a configurable amount of random graphs interactively.

    The user is prompted for the following inputs:
    - The primary folder to save the graphs to.
    - The node counts of the graphs to be created.
    - The densities of the graphs to be created.
    - How many graphs to create for each size within the density group.
    - The range of edge weights to be generated.

    Each density group receives a separate folder within the primary folder.
    Each graph is saved as a separate file within the density group folder,
    named according to the node count.
    """
    print("\n --- Interactive Random Graph Mass Creation --- ")

    start_input = input("Type 'h' for help; or anything else to continue.\n").lower()
    if start_input == "h":
        print(HELP_MSG)

    # Get the primary folder to save the graphs to
    primary_folder = input("Enter the primary folder to save the graphs to: ")
    if not os.path.exists(primary_folder):
        os.makedirs(primary_folder)

    # Get the node counts of the graphs to be created
    n_counts_input = input(
        "Enter the node counts of the graphs to be created (comma-separated):\n"
    )
    node_counts = [int(n.strip()) for n in n_counts_input.split(",")]

    # Possible security issue with eval; ignore because the user runs this locally
    # pylint: disable=eval-used

    # Get the densities of the graphs to be created
    densities_input = input(
        "Enter the density groups of the graphs to be created (comma-separated):\n"
    )

    # Parse the densities as lambda functions, expecting 'n' as the number of nodes
    # The list will contain lambda functions that take 'n' as an argument
    densities: list[Callable[[int], float]] = []
    for density in densities_input.split(","):
        try:
            densities.append(eval(f"lambda n: float({density})", {"math": math}))
        except Exception as e:
            logging.error("FATAL: invalid density expression: %s", density)
            raise ValueError(f"invalid density expression: {density}") from e

    # Get how many graphs to create for each size within the density group
    num_graphs = int(input("Enter how many graphs to create for each size: ").strip())

    # Get the range of edge weights to be generated
    weight_range_input = input(
        "Enter the range of edge weights to be generated (comma-separated):\n"
    )
    range_values = weight_range_input.split(",")
    weight_range = (int(range_values[0].strip()), int(range_values[1].strip()))

    # Display the settings to the user
    print("\nSettings:")
    print(f"Primary folder: {primary_folder}")
    print(f"Node counts: {node_counts}")
    print(f"Densities: {densities_input}")
    print(f"Graphs per size: {num_graphs}")
    print(f"Edge weight range: {weight_range}")

    # Confirm the settings with the user
    confirm = input("Do you want to create the graphs with these settings? (y/n): ")
    if confirm.lower() != "y":
        print("Exiting...")
        return

    # Create the graphs
    mass_create_graphs(primary_folder, node_counts, densities, num_graphs, weight_range)
    print(
        f"Successfully created {len(densities) * len(node_counts) * num_graphs} graphs."
    )


def mass_create_graphs(
    primary_folder: str,
    node_counts: list[int],
    densities: list[Callable],
    num_graphs: int,
    weight_range: tuple[int, int],
) -> None:
    """Mass create random graphs with different densities and sizes.

    Each density group receives a separate folder within the primary folder.
    Each graph is saved as a separate file within the density group folder,
    named according to the node count.

    Args:
        primary_folder (str): the primary folder to save the graphs to
        node_counts (list[int]): the node counts of the graphs to be created
        densities (list[Callable]): the densities of the graphs to be created
        num_graphs (int): how many graphs to create for each size within the density group
        weight_range (tuple[int, int]): the range of edge weights to be generated
    """
    for i, density in enumerate(densities):
        density_folder = os.path.join(primary_folder, f"density_{i}")
        if not os.path.exists(density_folder):
            os.makedirs(density_folder)

        for n in node_counts:
            for i in range(num_graphs):
                graph = generate_random_graph(n, weight_range, density(n))
                filename = os.path.join(density_folder, f"graph_{n}_{i}.adj")
                write_adjacency_list(graph, filename)


def generate_random_graph(
    n: int,
    weight_range: tuple[int, int],
    density: float,
    std_dev: Optional[float] = None,
) -> Graph:
    """Generate a random graph with a given number of nodes, edge weight range, and density.

    The edge weights are generated as random integers within the given inclusive range.

    The density of the graph is defined as the ratio of the number of edges to the maximum
    possible number of edges. This means each node will have on average `density * (n - 1)`
    outbound edges. The actual number of edges per node will be normally distributed around
    this average with a standard deviation of `std_dev`. Because of this implementation,
    there is no guarantee that the graph will be connected.

    For example, a graph with 5 nodes and a density of 0.5 will have on average 2 outbound
    edges per node for a total of 10 edges. The actual number of edges per node can vary.

    In general, a graph with with density `1 / (n - 1)` will have an average of 1 edge per
    node, and a graph with density 1 will have the maximum possible number of edges, that is,
    `n - 1` edges per node.

    If the standard deviation is not provided, it defaults to `0.2 * density * (n - 1)`.

    Args:
        n (int): the number of nodes in the graph
        weight_range (tuple[int, int]): the range of edge weights to be generated, inclusive
        density (float): the ratio of the numbers of edges to maximum possible edges
        std_dev (float, optional): the standard deviation for the number of edges per node
    """
    if std_dev is None:
        std_dev = 0.2 * density * (n - 1)
    nodes: list[Node] = [Node(i) for i in range(n)]

    # Generate edges for each node
    edges: list[Edge] = []
    for tail in nodes:
        # Calculate the number of edges for this node
        num_edges: int = round(random.gauss(density * (n - 1), std_dev))
        num_edges = clamp(num_edges, 0, n - 1)

        # Randomly select head nodes
        other_nodes = nodes.copy()
        remove_by_ref(other_nodes, tail)  # Tail node should not be a head
        heads = random.sample(other_nodes, num_edges)

        # Generate edges for this node
        for head in heads:
            weight = random.randint(*weight_range)
            edges.append(Edge(tail, head, weight))

    return Graph(nodes, edges)


def clamp(value, min_value, max_value):
    """Clamp a value between a minimum and maximum value."""
    return max(min_value, min(value, max_value))


def remove_by_ref(lst, obj):
    """Remove an object from a list by reference rather than value."""
    lst[:] = [x for x in lst if id(x) != id(obj)]


if __name__ == "__main__":
    interactive_creation()
