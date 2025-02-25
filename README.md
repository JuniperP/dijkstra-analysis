# Dijkstra's Algorithm Project

This project implements and compares the simple and heap implementations of Dijkstra's algorithm on various graphs.

Note: All mentions of `python` in this document refer to Python 3.
(If you have both Python 2 and Python 3 installed, you may need to use `python3` instead of `python`.)

**Author:** Juniper Pasternak following the guidelines of the [project assignment](https://www.cs.kzoo.edu/cs215/PP1.html).

## Table of Contents

- [Dijkstra's Algorithm Project](#dijkstras-algorithm-project)
  - [Table of Contents](#table-of-contents)
  - [Pre-requisites](#pre-requisites)
  - [Usage](#usage)
  - [File Summary](#file-summary)
    - [Python Scripts](#python-scripts)
    - [Other Files](#other-files)
    - [Folders](#folders)

## Pre-requisites

- [Python 3.12 or higher](https://www.python.org/)
- Optional (For data visualization)
  - `python -m pip install -r requirements.txt`

## Usage

The following are the python scripts intended to be ran directly:

- `main.py`: Run Dijkstra's algorithm on a graph file. The script asks for the graph file and uses the first node as the source node.
  - Example: `python main.py` with `graphs/simple_test.adj` as the graph file.
- `measure_runs.py`: Measure the number of operations for each run of the algorithm on the random graphs. The script asks for the primary folder containing multiple density folders.
  - Example: `python measure_runs.py` with `graphs/` as the primary folder.
- `random_graph.py`: Generate random graphs. The script asks for various parameters to generate the graph. Use `h` in the script for help.
  - Example: `python random_graph.py` with `random_graphs/` as the output folder, and `10, 20, 30`, `0.1, 0.2, 0.3`, `3`, and `1, 5` as the parameters.
- `analysis.ipynb`: Jupyter notebook with data visualization of the operation counts. The notebook reads the `data.json` file and generates plots.
  - Example: `jupyter notebook analysis.ipynb`

## File Summary

### Python Scripts

- `analysis.ipynb`: Jupyter notebook with data visualization of the operation counts.
- `dijkstra.py`: Contains implementations of Dijkstra's algorithm.
- `graph_io.py`: Contains functions for reading and writing graphs from/to files.
- `main.py`: Script to run Dijkstra's algorithm on a graph file.
- `measure_runs.py`: Script to measure the number of operations for each run of the algorithm.
- `random_graph.py`: Script to generate random graphs.
- `structures.py`: Contains the implementation of the graph data structure.

### Other Files

- `Analysis.pdf`: Written analysis of the algorithms, time complexities, and results.
- `data.json`: Contains the operation counts for each run of the algorithm on the random graphs.
- `README.md`: This file. Used to provide information about the project.
- `requirements.txt`: Contain the required Python packages for data visualization.

### Folders

- `graphs/`: Contains sample graph files.
Credit for 2 test files: [Algorithms Illuminated Datasets](https://www.algorithmsilluminated.org/datasets/)
`problem9.8.txt` and `problem9.8test.txt`.
  - `density_0/` to `_2/`: Contains random graphs organized by density.
- `plots/`: Contains plots generated by `analysis.ipynb`.
