from gopt.circuit import Circuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Construct MBQC circuit on cluster state and implement it in unitary circuit model
circuit = Circuit(2)
circuit.h(0)
circuit.cnot(0, 1)

# The circuit is by default measured in Z-bases without calling the measure_all method
# but for sure you can do that manually
circuit.add_outputs()

# Perform pauli_eliminations
graph = circuit.to_graph_state()
graph.eliminate_pauli()

# Draw the graph state using matplotlib
graph.draw()
plt.show()

# Run the MBQC circuit in 5000 shots
counts = graph.run(5000)

# Plot the result stats using the qiskit package
plot_histogram(counts)
plt.show()
