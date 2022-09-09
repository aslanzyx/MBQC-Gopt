import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from gopt.graph import ZXGraph

# Create a graph
g = nx.Graph()
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)
g.add_edge(3, 5)
g.add_edge(5, 6)

# Construct ZX-graph-state object
zx = ZXGraph(
    g, {
        0: np.pi / 4,
        1: np.pi / 4,
        2: np.pi / 4,
        3: np.pi / 4,
        4: np.pi / 4,
        5: 0,
        6: np.pi / 4
    },
    [5]
)

# Call eliminate_clifford to remove all Clifford parts
# TODO: Implement the angle transformations in gopt.graph.ZXGraph before you run this
zx.eliminate_clifford()

# Call bss_decomp to apply a single-round BSS decomposition
# TODO: Implement the BSS decomposition in gopt.graph.ZXGraph before you run this
zx.bss_decomp()

# Call query_prob_with_decomp to recursively apply BSS decomposition and compute the probability
# TODO: Implement query_prob and query_prob_with_decomp in gopt.graph.ZXGraph before you run this
zx.query_prob_with_decomp()

# Render to visualize the ZX-diagram
zx.render()
plt.show()
