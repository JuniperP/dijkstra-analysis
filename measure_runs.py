"""This module contains utilities for measuring the performance of Dijkstra's algorithm.

The script can be used to measure the number of operations in Dijkstra's algorithm on graphs
with different densities and sizes. The results are then serialized to a JSON file.

Author: Juniper Pasternak
Date: 2024-05-14
"""

import json
import os
import dataclasses
from dijkstra import OpsTracker, simple_shortest_path, heap_shortest_path
from structures import Graph
from graph_io import read_adjacency_list


@dataclasses.dataclass
class RunData:
    """Data from Dijkstra's algorithm run on a single graph.

    Attributes:
        n (int): the number of nodes in the graph
        m (int): the number of edges in the graph
        simple_ops (int): the number of operations in the simple implementation
        heap_ops (int): the number of operations in the heap implementation
    """

    n: int
    m: int
    simple_ops: int
    heap_ops: int

    def to_dict(self) -> dict:
        """Convert the data to a dictionary for serialization."""
        return dataclasses.asdict(self)


def densities_to_json(data: list[dict[int, list[RunData]]], filename: str) -> None:
    """Serialize the data from running Dijkstra's algorithm by density group to a JSON file.

    The JSON file is structured like the following example:
    ```json
    [
        {
            "10":
            [
                {
                    "n": 10,
                    "m": 20,
                    "simple_ops": 100,
                    "heap_ops": 50
                }
            ]
        }
    ]
    ```

    Args:
        data (list[dict[int, list[RunData]]]): the data from the run_densities function
        filename (str): the name of the file to write the data to
    """
    # Convert integer keys to strings and RunData objects to dictionaries
    converted_data = [
        {str(k): [run_data.to_dict() for run_data in v] for k, v in dict_item.items()}
        for dict_item in data
    ]

    # Serialize the converted data to a JSON string
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(converted_data, file)


def run_densities(primary_folder: str) -> list[dict[int, list[RunData]]]:
    """Run Dijkstra's algorithm on graphs in folders with different densities.

    Args:
        primary_folder (str): the primary folder containing the density folders

    Returns:
        list[dict[int, list[RunData]]]: the data from running Dijkstra's algorithm by density group
    """
    # Get the list of density folders in the primary folder
    density_folders = [
        f
        for f in os.listdir(primary_folder)
        if os.path.isdir(os.path.join(primary_folder, f)) and f.startswith("density_")
    ]
    density_folders.sort()

    # Store data from running Dijkstra's algorithm by density group
    data = [
        run_folder(os.path.join(primary_folder, folder)) for folder in density_folders
    ]

    return data


def run_folder(folder: str) -> dict[int, list[RunData]]:
    """Run Dijkstra's algorithm on all graphs in a folder and return the results by graph size.

    Args:
        folder (str): the folder containing the graphs

    Return:
        dict[int, list[RunData]]: the data from running Dijkstra's algorithm by graph size
    """
    # Get the list of .adj files in the folder
    files = [
        f
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.endswith(".adj")
    ]
    files.sort()

    # Store data from running Dijkstra's algorithm by graph size
    data = {}
    for i, file in enumerate(files):
        print(
            f"Folder '{os.path.basename(folder)}':",
            f"Measuring '{file}' ({i + 1}/{len(files)})...",
        )
        graph = read_adjacency_list(os.path.join(folder, file))
        run_data = run_dijkstra(graph)
        if run_data.n not in data:
            data[run_data.n] = []
        data[run_data.n].append(run_data)

    return data


def run_dijkstra(graph: Graph) -> RunData:
    """Run Dijkstra's algorithm on a graph and return the operations data.

    Args:
        graph (Graph): the graph to run Dijkstra's algorithm on

    Returns:
        RunData: the data from the run
    """
    OpsTracker.reset()

    simple_shortest_path(graph, graph.nodes[0])
    simple_ops = OpsTracker.simple_ops

    heap_shortest_path(graph, graph.nodes[0])
    heap_ops = round(OpsTracker.heap_ops)

    return RunData(len(graph.nodes), len(graph.edges), simple_ops, heap_ops)


def main() -> None:
    """Run the algorithms on various density groups and save the results to a JSON file."""
    primary_folder = input(
        "Enter the primary folder containing the density folders: "
    ).strip()
    data = run_densities(primary_folder)
    densities_to_json(data, "densities.json")


if __name__ == "__main__":
    main()
