import json
import random
import time

import numpy as np
from matplotlib import pyplot as plt
from graphoptim.core import ClusterState
from graphoptim.optimizers.DegreeNormOptimizerDFS import DegreeNormOptimizerDFS
from graphoptim.optimizers.EdgeOptimizerDFS import EdgeOptimizerDFS
from graphoptim.optimizers.MaxDegreeOptimizerDFS import MaxDegreeOptimizerDFS
from graphoptim.optimizers.RegisterSizeOptimizerBFS import RegisterSizeOptimizerBFS
from graphoptim.optimizers.RegisterSizeOptimizerDFS import RegisterSizeOptimizerDFS


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

    # Make first schedule
    print(f"degree of reduced graph state {graph.geometry.max_degree_nodes()[1]}")
    sequence, size = graph.schedule()
    # graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()
    print(f"scheduling finished with size {size}")
    print(f"total number of nodes {len(graph.geometry.nodes())}")

    # start_time = time.time()
    # eo = EdgeOptimizerDFS(graph, max_depth=2000)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/eo_bfs_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = EdgeOptimizerDFS(graph, max_depth=1500, rev=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/eo_bfs_rev_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = EdgeOptimizerDFS(graph, max_depth=10000, rev=True, traverse_all=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/eo_bfs_rev_all_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = DegreeNormOptimizerDFS(graph, max_depth=1500, rev=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/dno_bfs_rev_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = DegreeNormOptimizerDFS(graph, max_depth=10000, rev=True, traverse_all=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/dno_bfs_rev_all_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = MaxDegreeOptimizerDFS(graph, max_depth=1500, rev=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/mdo_bfs_rev_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = MaxDegreeOptimizerDFS(graph, max_depth=10000, rev=True, traverse_all=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/mdo_bfs_rev_all_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = RegisterSizeOptimizerDFS(graph, max_depth=1500, rev=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/rso_bfs_rev_track_{m // 2}_{n}.json")

    # NOTE: Done
    # start_time = time.time()
    # eo = RegisterSizeOptimizerDFS(graph, max_depth=10000, rev=True, traverse_all=True)
    # eo.execute()
    # print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    # print(f"optimization finished with # of edges required {eo.min_edge_size}")
    # print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/performance/rso_bfs_rev_all_track_{m // 2}_{n}.json")


def save_angle_matrix(angles_matrix: np.ndarray, filename):
    with open(filename, 'wb') as f:
        np.save(f, angles_matrix)


def load_angle_matrix(filename):
    with open(filename, 'rb') as f:
        angles_matrix = np.load(f)
    return angles_matrix


def plot_analysis(filename):
    with open(filename, 'rb') as f:
        json_obj = json.load(f)
    isomorphic_track: dict = json_obj

    depths = []
    max_degrees = []
    degree_norms = []
    edge_sizes = []
    reg_sizes = []

    for depth, info in isomorphic_track.items():
        if depth.isnumeric():
            depths.append(int(depth))
            max_degrees.append(int(info["max_degree"]))
            degree_norms.append(int(info["degree_norm"]))
            reg_sizes.append(int(info["reg_size"]))
            edge_sizes.append(int(info["edge_size"]))

    sep = 5
    depths = depths[::sep]
    max_degrees = max_degrees[::sep]
    degree_norms = degree_norms[::sep]
    edge_sizes = edge_sizes[::sep]
    reg_sizes = reg_sizes[::sep]

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    ax1.plot(depths, edge_sizes, 'k', lw=1)
    ax2.plot(depths, reg_sizes, 'k', lw=1)
    ax3.plot(depths, max_degrees, 'k', lw=1)
    ax4.plot(depths, degree_norms, 'k', lw=1)
    ax1.axvline(x=json_obj["min_edge_size_idx"], c='red', ls=":", lw=2)
    ax2.axvline(x=json_obj["min_reg_size_idx"], c='red', ls=":", lw=2)
    ax3.axvline(x=json_obj["minimax_degree_idx"], c='red', ls=":", lw=2)
    ax4.axvline(x=json_obj["min_degree_norm_idx"], c='red', ls=":", lw=2)

    ax1.set_xlabel("number of node traversed")
    ax1.set_ylabel("edge size")
    ax2.set_xlabel("number of node traversed")
    ax2.set_ylabel("register size")
    ax3.set_xlabel("number of node traversed")
    ax3.set_ylabel("max degree")
    ax4.set_xlabel("number of node traversed")
    ax4.set_ylabel("degree l2-norm")

    ax1.set_title(f"Minimum edge size: {json_obj['min_edge_size']} "
                  f"reached at {json_obj['min_edge_size_idx']}-th iteration")
    ax2.set_title(f"Minimum register size: {json_obj['min_reg_size']} "
                  f"reached at {json_obj['min_reg_size_idx']}-th iteration")
    ax3.set_title(f"Minimum max degree: {json_obj['minimax_degree']} "
                  f"reached at {json_obj['minimax_degree_idx']}-th iteration")
    ax4.set_title(f"Minimum degree l2-norm: {json_obj['min_degree_norm']:.2f} "
                  f"reached at {json_obj['min_degree_norm_idx']}-th iteration")
    # ax2.set_title("register size: ")
    # ax3.set_title("max degree")
    # ax4.set_title("degree l2-norm traversed")

    plt.show()


n = 20
m = 20
# angles = np.random.rand(1, 2 * m * n)
# angle_matrix = np.round(8 * angles - 4) * pi / 4
# angle_matrix = angle_matrix.reshape(2 * m, n)
# angle_matrix = load_angle_matrix(f"benchmark/performance/angles_rand3_{m}_{n}.npy")
# random_circuit(angle_matrix)

filenames = [
    f"benchmark/performance/eo_bfs_track_{m}_{n}.json",
    f"benchmark/performance/eo_bfs_rev_track_{m}_{n}.json",
    f"benchmark/performance/eo_bfs_rev_all_track_{m}_{n}.json",
    f"benchmark/performance/dno_bfs_rev_track_{m}_{n}.json",
    f"benchmark/performance/dno_bfs_rev_all_track_{m}_{n}.json",
    f"benchmark/performance/mdo_bfs_rev_track_{m}_{n}.json",
    f"benchmark/performance/mdo_bfs_rev_all_track_{m}_{n}.json",
    f"benchmark/performance/rso_bfs_rev_track_{m}_{n}.json",
    f"benchmark/performance/rso_bfs_rev_all_track_{m}_{n}.json"
]

plot_analysis(filenames[7])
