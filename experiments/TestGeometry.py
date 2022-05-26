from graphoptim.core import ClusterState
import matplotlib.pyplot as plt

c = ClusterState(1)
c.add_rotation_sequence(0, [0, 0, 0, 0])
g = c.to_graph_state()
g.local_complement((0, 1))
g.draw_cluster(None)
print([g.measurement_bases.pauli_sign(node) for node in g.geometry.nodes()])
print([g.geometry.neighbours(node) for node in g.geometry.nodes()])
plt.show()
