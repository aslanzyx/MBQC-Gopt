import json
import random
import time

import numpy as np
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from graphoptim.optimizers import GeometryOptimizer
from math import pi
from graphoptim.core import ClusterState
from graphoptim.optimizers.EdgeOptimizerDFS import EdgeOptimizerDFS
from graphoptim.optimizers.RegisterSizeOptimizer import RegisterSizeOptimizer
from graphoptim.optimizers.RegisterSizeOptimizerBFS import RegisterSizeOptimizerBFS
from graphoptim.optimizers.EdgeOptimizer import EdgeOptimizer
from graphoptim.optimizers.EdgeOptimizerBFS import EdgeOptimizerBFS


def random_circuit(angle_matrix: np.ndarray):
    m, n = angle_matrix.shape
    cluster = ClusterState(n)
    parity = 0
    for i in range(0, m, 2):
        for j in range(n):
            cluster.add_rotation_sequence(j, [angle_matrix[i, j], angle_matrix[i + 1, j]])
        if parity:
            for j in range(1, n - 1, 2):
                cluster.cz(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                cluster.cz(j, j + 1)
        parity ^= 1

    # Graph state reduction
    graph = cluster.to_graph_state()
    print(f"total number of nodes {len(graph.geometry.nodes())}")

    graph.eliminate_clifford()
    # graph.draw()
    # plt.show()

    # Make first schedule
    print(f"degree of reduced graph state {graph.geometry.max_degree_nodes()[1]}")
    sequence, size = graph.schedule()
    # graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()
    print(f"scheduling finished with size {size}")
    print(f"total number of nodes {len(graph.geometry.nodes())}")

    # test isomorphism
    start_time = time.time()
    eo = EdgeOptimizerDFS(graph, max_depth=1000, rev=True)
    eo.execute()
    print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    print(f"optimization finished with # of edges required {eo.min_edge_size}")
    print(f"executed with time {time.time() - start_time:.2f}")
    eo.save_track(f"benchmark/isomorphism/main_with_iso_rev_track_{m // 2}_{n}.json")


def save_angle_matrix(angles_matrix: np.ndarray, filename):
    with open(filename, 'wb') as f:
        np.save(f, angles_matrix)


def load_angle_matrix(filename):
    with open(filename, 'rb') as f:
        angles_matrix = np.load(f)
    return angles_matrix


def plot_isomorphism_analysis(filename):
    with open(filename, 'rb') as f:
        json_obj = json.load(f)
    isomorphic_track: dict = json_obj["isomorphic_track"]

    for kk, kkk in isomorphic_track.items():
        degrees = []
        reg_sizes = []
        if len(kkk) > 10:
            for k in kkk:
                degrees.append(json_obj[k]["max_degree"])
                reg_sizes.append(json_obj[k]["reg_size"])
        print(degrees)
        print(reg_sizes)


def plot_analysis(filename):
    with open(filename, 'rb') as f:
        json_obj = json.load(f)
    isomorphic_track: dict = json_obj

    depths = []
    degrees = []
    edge_sizes = []
    reg_sizes = []

    for depth, info in isomorphic_track.items():
        if depth.isnumeric():
            depths.append(int(depth))
            degrees.append(int(info["max_degree"]))
            reg_sizes.append(int(info["reg_size"]))
            edge_sizes.append(int(info["edge_size"]))

    plt.plot(depths, edge_sizes)
    plt.show()


n = 10
m = 10
filename = f"benchmark/isomorphism/main_track_{m}_{n}.json"
filename = f"benchmark/isomorphism/main_with_iso_track_{m}_{n}.json"
# filename = f"benchmark/isomorphism/main_with_no_iso_track_{m}_{n}.json"
filename = f"benchmark/isomorphism/main_with_iso_rev_track_{m}_{n}.json"

angle_matrix = load_angle_matrix(f"benchmark/isomorphism/angles_iso_{m}_{n}.npy")
random_circuit(angle_matrix)

# plot_isomorphism_analysis(filename)
plot_analysis(filename)
