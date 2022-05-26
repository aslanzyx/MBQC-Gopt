import random

import numpy as np
from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile
from graphoptim.optimizers import GeometryOptimizer
from math import pi
from graphoptim.core import ClusterState


def random_circuit(m, n, density, shot):
    k = int(n * density)
    cluster = ClusterState(n)
    circuit = QuantumCircuit(n, n)
    parity = 0
    for i in range(m):
        t_id = random.sample(range(n), k)
        for j in range(n):
            if j in t_id:
                cluster.rx(j, pi / 6)
                circuit.rx(pi / 6, j)
            else:
                gate_id = random.randint(0, 3)
                if gate_id == 0:
                    cluster.h(j)
                    circuit.h(j)
                elif gate_id == 1:
                    cluster.x(j)
                    circuit.x(j)
                elif gate_id == 2:
                    cluster.z(j)
                    circuit.z(j)
                elif gate_id == 3:
                    cluster.s(j)
                    circuit.s(j)
        if parity:
            for j in range(1, n - 1, 2):
                cluster.cz(j, j + 1)
                circuit.cz(j, j + 1)
        else:
            for j in range(0, n - 1, 2):
                cluster.cz(j, j + 1)
                circuit.cz(j, j + 1)
        parity ^= 1

    # Graph state reduction
    graph = cluster.to_graph_state()
    graph.eliminate_pauli()

    # Make first schedule
    print(f"degree of reduced graph state {graph.geometry.max_degree_nodes()[1]}")
    _, size = graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()

    # Draw first graph
    # graph.draw()
    # plt.title(f"max degree {degree}, scheduled with {size} qubit")
    # plt.show()

    # Search for an optimized geometry
    go = GeometryOptimizer(graph.geometry)
    go.execute()
    print(f"geometry optimized with degree {go.minimax_degree}")

    # Process local complementation
    sequence = go.optimized_lc_sequence()
    for node in sequence:
        graph.local_complement(node)

    # Make schedule again
    # print(graph.geometry.max_degree_nodes())
    _, size = graph.schedule()
    _, degree = graph.geometry.max_degree_nodes()

    # Draw the graph state
    graph.draw()
    plt.title(f"optimized max degree {degree}, scheduled with {size} qubit")
    plt.show()

    # Assert for fusion nodes
    graph.assert_fusion_nodes()

    # counts_mbqc = graph.run(shot)

    # Process circuit measurements
    # circuit.measure(range(n), range(n))
    # simulator = QasmSimulator()
    # qasm_circuit = transpile(circuit, simulator)
    # job = simulator.run(circuit, shot=shot)
    # result = job.result()
    # counts_qc = result.get_counts(qasm_circuit)

    # Draw plots
    # plot_histogram([counts_mbqc, counts_qc],
    #                title="MBQC result compare to theoretical results",
    #                legend=["MBQC", "UC"])
    # circuit.draw(output='mpl')
    # plt.show()


random_circuit(6, 10, .6, 10000)
