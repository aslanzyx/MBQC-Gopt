import matplotlib.pyplot as plt
import networkx as nx
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram

from graphoptim.core import ClusterState, GeometryLayer
from graphoptim.optimizers import GeometryOptimizer
from math import pi


def controlled_phase(circuit: ClusterState,
                     control_id: int, target_id: int, angle: float):
    circuit.rz(target_id, angle / 2)
    circuit.cnot(control_id, target_id)
    circuit.rz(target_id, -angle / 2)
    circuit.cnot(control_id, target_id)


def transform_iteration(circuit: ClusterState,
                        target_id: int):
    it = 0
    for i in range(target_id + 1, circuit.size):
        controlled_phase(circuit, i, target_id,
                         -pi / (4 * 2 ** it))
        it += 1


def qft(n):
    circuit = ClusterState(n)
    for i in range(circuit.size):
        circuit.rx(i, pi / 4)
    circuit.h(0)
    for i in range(0, circuit.size - 1):
        transform_iteration(circuit, i)
        circuit.h(i + 1)
    graph = circuit.to_graph_state()
    graph.eliminate_pauli()
    graph.local_complement((0, 24))
    graph.schedule()
    # graph.draw()
    # plt.show()

    print(graph.geometry.max_degree_nodes())
    go = GeometryOptimizer(graph.geometry)
    go.execute()
    print(go.minimax_degree)

    lc_sequence = go.optimized_lc_sequence()
    for node in lc_sequence:
        graph.local_complement(node)

    print(graph.geometry.max_degree_nodes())
    graph.draw_cluster()
    plt.show()
    graph.schedule()


qft(5)
