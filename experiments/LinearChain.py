import random

from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

from graphoptim.core.ClusterState import ClusterState
from qiskit import QuantumCircuit, transpile
from math import pi
import matplotlib.pyplot as plt
import numpy as np

import networkx as nx


def wire_mbqc(angles, shot):
    cluster = ClusterState(1)
    cluster.add_rotation_sequence(0, angles)
    graph = cluster.to_graph_state()

    graph.eliminate_pauli()
    graph.eliminate_disconnected()

    graph.draw()
    plt.title(f"Reduced linear graph state with {len(graph.geometry.nodes())} nodes")
    plt.show()

    graph.fuse_nodes()
    graph.draw()
    plt.title(f"Fused linear graph state with {len(graph.geometry.nodes())} nodes")
    # plt.show()

    return graph.run(shot)
    # graph.draw()
    # return dict()

    # circuit, creg_map = graph.compile()
    # simulator = QasmSimulator()
    # qasm_circuit = transpile(circuit, simulator)
    # job = simulator.run(qasm_circuit, shot=shot)
    # result = job.result()
    # counts = result.get_counts(qasm_circuit)
    # return process_outcomes(counts, creg_map, graph.output_layer)
    # plot_histogram(processed_counts)


def wire_qc(angles, shot):
    circuit = QuantumCircuit(1, 1)
    for angle in angles:
        circuit.rz(angle, 0)
        circuit.h(0)
    circuit.measure(0, 0)
    simulator = QasmSimulator()
    qasm_circuit = transpile(circuit, simulator)
    job = simulator.run(qasm_circuit, shot=shot)
    result = job.result()
    # circuit.draw(output="mpl")
    return result.get_counts(qasm_circuit)


angles = np.random.rand(50)
angles = [round(8 * angle - 4) * pi / 4 for angle in angles]
print(angles)
shot = 5000
mbqc_count = wire_mbqc(angles, shot)
qc_count = wire_qc(angles, shot)
plot_histogram([mbqc_count, qc_count])
plt.show()

# print(np.angle(1j))
