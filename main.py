"""The main module allows the user to run Dijkstra's algorithm on a graph.

The user can compare the number of operations between the simple and heap
implementations of Dijkstra's algorithm on a graph.

The user is also able to specify the graph file to run the algorithm on and
whether to print the debug information from the algorithms.

Author: Juniper Pasternak
Date: 2024-05-14
"""

import logging
from structures import Graph
from graph_io import read_adjacency_list
from dijkstra import OpsTracker, simple_shortest_path, heap_shortest_path


def main() -> None:
    """Run Dijkstra's algorithm on a graph and compare the number of operations."""
    # Get user input
    graph_file = input("Enter the graph file to run Dijkstra's algorithm on: ").strip()
    is_debug = input("Print debug information? (y/n): ").lower() == "y"

    graph: Graph = read_adjacency_list(graph_file)
    if is_debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.info(
        "Running algorithms on a graph with %s nodes and %s edges...",
        len(graph.nodes),
        len(graph.edges),
    )
    if is_debug:
        graph.print_adjacency_list()

    OpsTracker.reset()

    print("\nSimple Implementation:")
    simple_shortest_path(graph, graph.nodes[0])
    graph.print_node_lengths()

    print("\nHeap Implementation:")
    heap_shortest_path(graph, graph.nodes[0])
    graph.print_node_lengths()

    OpsTracker.print_operations()


if __name__ == "__main__":
    main()
