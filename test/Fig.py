import matplotlib.pyplot as plt
import networkx as nx
from qiskit.circuit.quantumcircuit import QuantumCircuit
from graphoptim.graph_state import ClusterState
import qiskit

h = ['x', 'y', 'y', 'y']
t = ['t', 'x']
x = ['x', '-x']
z = ['-x', 'x']
s = ['y', 'y']
th = ['-t', 'x']


# Motivation
# fsize = 16
# plt.figure(figsize=(8, 6), dpi=100)
# g = nx.DiGraph()
# g.add_edge(0, 1)
# g.add_edge(1, 2)
# g.add_edge(2, 3)
# g.add_edge(3, 4)
# g.add_edge(4, 5)
# pos = {p: (p, 0) for p in g.nodes()}
# plt.subplot(221)
# nx.draw(g, pos, width=2, node_size=200, node_color='k')
# plt.title("1.1 MBQC on a chain", fontsize=fsize)
# plt.subplot(222)
# g = nx.MultiDiGraph()
# g.add_node(0)
# g.add_node(1)
# g.add_edge(0, 1, length=2)
# g.add_edge(1, 0, length=3)
# pos = {0: (0, 0), 1: (1, 0)}
# nx.draw(g, pos, width=2, node_size=200, node_color='k',
#         connectionstyle='arc3, rad = 0.1')
# plt.title("1.2 Implementing the chain on 2 nodes", fontsize=fsize)
# plt.subplot(223)
# g = nx.complete_graph(6)
# pos = nx.circular_layout(g)
# g.remove_edge(1, 2)
# nx.draw_circular(g, width=2, node_size=200, node_color='k')
# plt.title("2.1 A complex graph", fontsize=fsize)
# plt.subplot(224)
# g = nx.DiGraph()
# g.add_edge(0, 1)
# g.add_edge(1, 2)
# g.add_edge(3, 0)
# g.add_edge(4, 0)
# g.add_edge(5, 0)
# nx.draw(g, pos, width=2, node_size=200, node_color='k')
# plt.title("2.2 Equivalent graph under L.C.", fontsize=fsize)
# plt.tight_layout()
# plt.show()

# method
c = ClusterState(9)
c.add_h(0)
c.add_h(1)
c.add_h(2)
c.add_h(3)
c.add_h(4)
c.add_h(5)
c.add_h(6)
c.add_h(7)
c.add_h(8)

c.add_h(0)
c.add_t(1)
c.add_h(2)
c.add_h(3)
c.add_h(4)
c.add_t(5)
c.add_h(6)
c.add_h(7)
c.add_h(8)
c.add_cz(0, 1)
c.add_cz(2, 3)
c.add_cz(4, 5)
c.add_cz(6, 7)
c.add_t(0)
c.add_h(1)
c.add_h(2)
c.add_h(3)
c.add_h(4)
c.add_h(5)
c.add_h(6)
c.add_t(7)
c.add_h(8)
c.add_cz(1, 2)
c.add_cz(3, 4)
c.add_cz(5, 6)
c.add_cz(7, 8)
c.add_h(0)
c.add_h(1)
c.add_h(2)
c.add_t(3)
c.add_h(4)
c.add_t(5)
c.add_h(6)
c.add_h(7)
c.add_h(8)
c.add_cz(0, 1)
c.add_cz(2, 3)
c.add_cz(4, 5)
c.add_cz(6, 7)
c.add_h(0)
c.add_h(1)
c.add_t(2)
c.add_h(3)
c.add_h(4)
c.add_h(5)
c.add_t(6)
c.add_h(7)
c.add_h(8)
g = c.to_graph_state()
g.eliminate_pauli()
plt.subplot(222)
plt.title("Remove Pauli measurements")
G = g.render()
nx.draw_circular(G, node_color='k', node_size=100,
                 connectionstyle='arc3, rad = 0.1')
plt.subplot(223)
plt.title("3 Obtain temperal order")
G = g.render_temporal_order()
nx.draw_circular(G, node_color='k', node_size=100,
                 connectionstyle='arc3, rad = 0.1')
g.local_complement(181, 1)
g.local_complement(83, 1)
g.local_complement(377, 1)
g.local_complement(347, 1)
g.local_complement(259, 1)
g.local_complement(228, 1)
plt.subplot(224)
G = g.render()
nx.draw_circular(G, node_color='k', node_size=100,
                 connectionstyle='arc3, rad = 0.1')
plt.title("4. Reduce the circuit via local complementation")

G = nx.grid_2d_graph(14, 4)
plt.subplot(221)
nx.draw(G, node_color='k', node_size=100,
        pos={p: p for p in G.nodes()},
        connectionstyle='arc3, rad = 0.1')
plt.title("1. Translate the unitary circuit to MBQC")
plt.tight_layout()
plt.show()


# MBQC
# qc = qiskit.QuantumCircuit(4)
# qc.h(0)
# qc.h(1)
# qc.t(2)
# qc.t(3)
# qc.cnot(0, 1)
# qc.cnot(2, 3)
# qc.h(0)
# qc.t(1)
# qc.h(2)
# qc.t(3)
# qc.barrier(0)
# qc.barrier(3)
# qc.cnot(1, 2)
# qc.t(0)
# qc.h(1)
# qc.h(2)
# qc.t(3)
# qc.cnot(0, 1)
# qc.cnot(2, 3)
# qc.h(0)
# qc.t(1)
# qc.h(2)
# qc.t(3)
# qc.measure_all()
# qc.draw(output='mpl')
# # plt.title("Unitary circuit model")
# plt.show()
# qc.h(1)

# h = ['x', 'y', 'y', 'y']
# t = ['t', 'x']
# x = ['x', '-x']
# z = ['-x', 'x']
# s = ['y', 'y']
# th = ['-t', 'x']

# c = ClusterState(4)
# c.add_rotation_sequence(0, h)
# c.add_rotation_sequence(1, h)
# c.add_rotation_sequence(2, t)
# c.add_rotation_sequence(3, t)
# c.add_entanglement(0, 1)
# c.add_entanglement(2, 3)
# c.add_rotation_sequence(0, h)
# c.add_rotation_sequence(1, t)
# c.add_rotation_sequence(2, h)
# c.add_rotation_sequence(3, t)
# c.add_entanglement(1, 2)
# c.add_rotation_sequence(0, t)
# c.add_rotation_sequence(1, h)
# c.add_rotation_sequence(2, h)
# c.add_rotation_sequence(3, t)
# c.add_entanglement(0, 1)
# c.add_entanglement(2, 3)
# c.add_rotation_sequence(0, h + ['z'])
# c.add_rotation_sequence(1, t + ['z'])
# c.add_rotation_sequence(2, h + ['z'])
# c.add_rotation_sequence(3, t + ['z'])
# plt.tight_layout()
# # plt.title("MBQC model")
# c.to_graph()

# Local complementation
# g = nx.grid_2d_graph(2, 2)
# g.add_edge((0, 0), (1, 1))
# plt.subplot(121)
# nx.draw(g,
#         pos={(x, y): (x, y) for x, y in g.nodes()},
# 		node_size=200,
#         width=2,
#         node_color=['lightgreen', 'lightgrey', 'lightgrey', 'lightgrey'],
#         labels={(x, y): 'Y' for x, y in g.nodes()}
#         )
# plt.title("Before")

# g.add_edge((0, 1), (1, 0))
# g.remove_edge((0, 1), (1, 1))
# g.remove_edge((1, 0), (1, 1))

# plt.subplot(122)

# nx.draw(g,
#         pos={(x, y): (x, y) for x, y in g.nodes()},
# 		node_color='lightgrey',
# 		node_size=200,
#         width=2,
#         labels={
#             (0, 0): '-Z',
#             (1, 0): 'X',
#             (0, 1): 'X',
#             (1, 1): 'X',
#         }
#         )
# plt.title("After")
# plt.tight_layout()
# plt.show()
