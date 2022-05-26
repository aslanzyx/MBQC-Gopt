from qiskit.visualization import plot_histogram

from graphoptim.core import ClusterState
from graphoptim.core.BlochSphere import BlochSphere
from math import pi
import matplotlib.pyplot as plt


def general_controlled_z_rotation(angle0: float, angle1: float):
    cluster = ClusterState(2)
    cluster.h(0)
    # cluster.x(1)
    cluster.rz(1, (angle0 + angle1) / 2)
    cluster.cnot(0, 1)
    cluster.rz(1, (angle0 - angle1) / 2)
    cluster.cnot(0, 1)
    graph = cluster.to_graph_state()

    # removal procedure
    graph.eliminate_pauli()
    plot_histogram(graph.run(5000))
    graph.draw()
    print(graph.schedule())
    plt.show()


def general_controlled_x_rotation(angle0: float, angle1: float):
    cluster = ClusterState(2)
    cluster.h(0)
    cluster.rx(1, (angle0 + angle1) / 2)
    cluster.cz(0, 1)
    cluster.rx(1, (angle0 - angle1) / 2)
    cluster.cz(0, 1)
    graph = cluster.to_graph_state()

    # removal procedure
    graph.eliminate_pauli()
    graph.draw()
    # plt.show()


general_controlled_z_rotation(0, pi / 2)
general_controlled_x_rotation(0, pi / 2)
