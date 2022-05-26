import time

import numpy as np
from math import pi
from graphoptim.core import ClusterState
from graphoptim.optimizers.EdgeOptimizerDFS import EdgeOptimizerDFS


def random_circuit(angle_matrix: np.ndarray):
    m, n = angle_matrix.shape
    cluster = ClusterState(n)
    parity = 0
    for i in range(0, m, gate_series_num):
        for j in range(n):
            cluster.add_rotation_sequence(j, [angle_matrix[i + k, j] for k in range(gate_series_num)])
        if parity:
            for j in range(1, n - 1, 2):
                cluster.cz(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                cluster.cz(j, j + 1)
        parity ^= 1

    # Graph state reduction
    graph = cluster.to_graph_state()
    graph.eliminate_clifford()

    # Make first schedule
    print(f"degree of reduced graph state {graph.geometry.max_degree_nodes()[1]}")
    sequence, size = graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()
    print(f"scheduling finished with size {size}")

    # Optimization
    start_time = time.time()
    eo = EdgeOptimizerDFS(graph, max_depth=5000)
    eo.execute()
    print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    print(f"optimization finished with # of edges required {eo.minimax_edge_size}")
    print(f"executed with time {time.time() - start_time:.2f}")
    eo.save_track(f"benchmark/sample2/track_{m // 2}_{n}_{iter_num}.json")


def save_angle_matrix(angles_matrix: np.ndarray, filename):
    with open(filename, 'wb') as f:
        np.save(f, angles_matrix)


def load_angle_matrix(filename):
    with open(filename, 'rb') as f:
        angles_matrix = np.load(f)
    return angles_matrix


N = 10
M = 10
spacing = 2
gate_series_num = 4
sample_num = 5

for n in range(spacing, N + spacing, spacing):
    for m in range(spacing, M + spacing, spacing):
        for iter_num in range(sample_num):
            angles = np.random.rand(1, gate_series_num * m * n)
            angle_matrix = np.round(8 * angles - 4) * pi / 4
            angle_matrix = angle_matrix.reshape(gate_series_num * m, n)
            random_circuit(angle_matrix)
            save_angle_matrix(angle_matrix, f"benchmark/sample2/angles_rand4_{m}_{n}_{iter_num}.npy")
            print(f"iteration({m},{n},{iter_num}) completed")
