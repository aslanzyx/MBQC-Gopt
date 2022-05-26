import json
import time

import matplotlib.pyplot as plt
import numpy as np
from math import pi
from graphoptim.core import ClusterState
from graphoptim.optimizers.EdgeOptimizerDFS import EdgeOptimizerDFS


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
    graph.eliminate_clifford()

    # Make first schedule
    print(f"degree of reduced graph state {graph.geometry.max_degree_nodes()[1]}")
    sequence, size = graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()
    print(f"scheduling finished with size {size}")

    # Optimization
    start_time = time.time()
    eo = EdgeOptimizerDFS(graph, max_depth=3000)
    eo.execute()
    print(f"optimization finished with quantum resource required {eo.min_reg_size}")
    print(f"optimization finished with # of edges required {eo.min_edge_size}")
    print(f"executed with time {time.time() - start_time:.2f}")
    # eo.save_track(f"benchmark/sample3/results/track_{m // 2}_{n}_{iter_num}.json")


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

    ax1.set_title("edge size nodes traversed")
    ax2.set_title("register size nodes traversed")
    ax3.set_title("max degree nodes traversed")
    ax4.set_title("degree l2-norm traversed")

    plt.show()


def plot_stuff():
    node_sizes = np.zeros((10, 10, 5))
    reg_sizes = np.zeros((10, 10, 5))
    for m in range(2, 22, 2):
        for n in range(2, 22, 2):
            for iter_num in range(5):
                filename = f"benchmark/sample3/results/track_{m}_{n}_{iter_num}.json"
                with open(filename, 'rb') as f:
                    json_obj = json.load(f)
                    node_sizes[m // 2 - 1, n // 2 - 1, iter_num] = json_obj["node_size"]
                    reg_sizes[m // 2 - 1, n // 2 - 1, iter_num] = json_obj["min_reg_size"]

    # node_sizes = node_sizes.reshape(500)
    # reg_sizes = reg_sizes.reshape(500)
    # z = np.polyfit(node_sizes, reg_sizes, 1)
    # z2 = np.polyfit(node_sizes, reg_sizes, 2)
    # print(node_sizes)
    # print(reg_sizes)
    #
    # X = np.linspace(0, 400, 400)
    #
    # pred = node_sizes * z[0] + z[1]
    # l2n0 = np.linalg.norm(reg_sizes - pred)
    # print(l2n0)
    # Y = X * z[0] + z[1]
    # # plt.plot(X, Y, 'c--')
    #
    # Y = X ** 2 * z2[0] + X * z2[1] + z2[2]
    # pred = node_sizes ** 2 * z2[0] + node_sizes * z2[1] + z2[2]
    # l2n1 = np.linalg.norm(pred - reg_sizes)
    # print(l2n1)
    # plt.plot(X, Y, 'b--')
    #
    # plt.scatter(node_sizes, reg_sizes, c='k', marker='.')
    # plt.legend(["quadratic fit", "data points"])
    #
    # plt.xlabel("graph state size")
    # plt.ylabel("MBQC register size")
    # plt.title("Relation between the register size and the graph state size")
    # plt.show()

    percentage_map = reg_sizes / node_sizes

    node_sizes = np.min(node_sizes, axis=2)
    reg_sizes = np.min(reg_sizes, axis=2)
    percentage_map = np.min(percentage_map, axis=2)
    diffs = reg_sizes - np.array([[2 * max(i, j) for j in range(10)] for i in range(10)])
    diffs_min = reg_sizes - np.array([[2 * min(i, j) for j in range(10)] for i in range(10)])

    plt.imshow(reg_sizes.T)
    plt.xticks(range(10), [2 * i + 2 for i in range(10)])
    plt.yticks(range(10), [2 * i + 2 for i in range(10)])
    plt.xlabel("circuit depth")
    plt.ylabel("register size")
    for i in range(0, 10):
        for j in range(0, 10):
            plt.text(i, j, f"{int(reg_sizes[i, j])}", ha='center', va='center', color='w')
    plt.title("Optimized qubit required by each circuit configurations")
    plt.show()

    plt.imshow(node_sizes.T)
    plt.xticks(range(10), [2 * i + 2 for i in range(10)])
    plt.yticks(range(10), [2 * i + 2 for i in range(10)])
    plt.xlabel("circuit depth")
    plt.ylabel("register size")
    for i in range(0, 10):
        for j in range(0, 10):
            plt.text(i, j, f"{int(node_sizes[i, j])}", ha='center', va='center', color='w')
    plt.title("Size of reduced graph state for each circuit configurations")
    plt.show()

    plt.imshow(percentage_map.T)
    plt.xticks(range(10), [2 * i + 2 for i in range(10)])
    plt.yticks(range(10), [2 * i + 2 for i in range(10)])
    plt.xlabel("circuit depth")
    plt.ylabel("register size")
    for i in range(0, 10):
        for j in range(0, 10):
            plt.text(i, j, f"{percentage_map[i, j]:.2f}", ha='center', va='center', color='w')
    plt.title("Ratio between the size of MBQC register and the graph state")
    plt.show()

    plt.imshow(diffs.T)
    plt.xticks(range(10), [2 * i + 2 for i in range(10)])
    plt.yticks(range(10), [2 * i + 2 for i in range(10)])
    plt.xlabel("circuit depth")
    plt.ylabel("register size")
    for i in range(0, 10):
        for j in range(0, 10):
            plt.text(i, j, f"{diffs[i, j]}", ha='center', va='center', color='w')
    plt.title("Difference between the MBQC register size and the max(height, depth)")
    plt.show()

    plt.imshow(diffs_min.T)
    plt.xticks(range(10), [2 * i + 2 for i in range(10)])
    plt.yticks(range(10), [2 * i + 2 for i in range(10)])
    plt.xlabel("circuit depth")
    plt.ylabel("register size")
    for i in range(0, 10):
        for j in range(0, 10):
            plt.text(i, j, f"{diffs_min[i, j]}", ha='center', va='center', color='w')
    plt.title("Difference between the MBQC register size and the min(height, depth)")
    plt.show()


# m = 20
# n = 20
# angles = np.random.rand(1, 2 * m * n)
# angle_matrix = np.round(8 * angles - 4) * pi / 4
# angle_matrix = angle_matrix.reshape(2 * m, n)
# random_circuit(angle_matrix)
# save_angle_matrix(angle_matrix, f"benchmark/sample3/angles/angles_track_{m}_{n}.npy")

# plot_analysis(f"benchmark/sample3/results/track_{20}_{20}_{0}.json")
plot_stuff()

# start_n = 2
# start_m = 2
# N = 22
# M = 22
# sample_num = 5
# for n in range(start_n, N, 2):
#     for m in range(start_m, M, 2):
#         for iter_num in range(sample_num):
#             angles = np.random.rand(1, 2 * m * n)
#             angle_matrix = np.round(8 * angles - 4) * pi / 4
#             angle_matrix = angle_matrix.reshape(2 * m, n)
#             random_circuit(angle_matrix)
#             save_angle_matrix(angle_matrix, f"benchmark/sample3/angles/angles_track_{m}_{n}_{iter_num}.npy")
#             print(f"iteration({m},{n},{iter_num}) completed")
