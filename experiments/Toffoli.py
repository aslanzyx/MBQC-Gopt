from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

from graphoptim.core import ClusterState
from math import pi
import matplotlib.pyplot as plt


def controlled_phase(circuit: ClusterState,
                     control_id: int, target_id: int, angle: float):
    circuit.rz(target_id, angle / 2)
    circuit.cnot(control_id, target_id)
    circuit.rz(target_id, -angle / 2)
    circuit.cnot(control_id, target_id)


def toffoli_z(circuit):
    controlled_phase(circuit, 0, 2, pi / 2)
    controlled_phase(circuit, 1, 2, pi / 2)
    circuit.cnot(0, 1)
    controlled_phase(circuit, 1, 2, -pi / 2)
    circuit.cnot(0, 1)


qc = QuantumCircuit(3, 3)
qc.h(0)
qc.h(1)
qc.rx(pi/3, 0)
qc.rx(-pi/3, 1)
qc.toffoli(0, 1, 2)
qc.measure(range(3), range(3))
simulator = QasmSimulator()
qasm_circuit = transpile(qc, simulator)
job = simulator.run(qc, shot=5000)
result = job.result()
counts_qc = result.get_counts(qasm_circuit)

circuit = ClusterState(3)
circuit.h(0)
circuit.h(1)
circuit.rx(0, pi/12)
circuit.rx(1, pi/16)
circuit.h(2)
toffoli_z(circuit)
circuit.h(2)

graph = circuit.to_graph_state()
graph.eliminate_pauli()
# graph.draw()
graph.run(10000)
# plot_histogram([graph.run(10000), counts_qc])
# plt.show()
plt.savefig("../cache/demo.png")
