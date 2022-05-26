from typing import Dict, Set, List

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator

from .GeometryLayer import GeometryLayer
from .MeasurementBaseLayer import MeasurementBaseLayer
from .DependencyLayer import MeasurementDependencyLayer
import networkx as nx
from math import pi


class GraphState:
    def __init__(self,
                 geometry_graph: nx.Graph,
                 dependency_map: Dict[any, Set[any]],
                 angle_map: Dict[any, float], output: List[any],
                 verbose: int = 0):
        self.geometry = GeometryLayer(geometry_graph)
        self.dependency: MeasurementDependencyLayer = MeasurementDependencyLayer(dependency_map)
        self.bases: MeasurementBaseLayer = MeasurementBaseLayer(angle_map)
        self.output_layer = output

        self._verbose = verbose
        self._reduced = False

    def local_complement(self, label, direction=1):
        neighbours = self.geometry.neighbours(label)
        self.geometry.local_complement(label)

        # Corrections on bases and corrections
        self.bases.rotate_sqrt_x(label, direction)
        self.dependency.rotate_sqrt_x(label, direction)
        for node in neighbours:
            self.bases.rotate_sqrt_z(node, -direction)
            self.dependency.rotate_sqrt_z(node, -direction)

    def z_measurement(self, label):
        direction = self.bases.pauli_sign(label)
        neighbours = self.geometry.neighbours(label)
        self.geometry.cutoff(label)
        self.dependency.cutoff(label)
        self.bases.cutoff(label)
        if direction == -1:
            for node in neighbours:
                self.bases.rotate(node, pi, 'z')

        self._reduced = True

    def y_measurement(self, label):
        self.local_complement(label)

        if self._verbose >= 1:
            print(f"reduced {label} to {self.bases.pauli_base(label)}")

        self.measure(label)

    def x_measurement(self, label, b=None):
        if self.geometry.degree(label) == 0:
            if self._verbose >= 3:
                print(f"simulating in sign {self.bases.pauli_sign(label)}")
            self.z_measurement(label)
        else:
            if b is None:
                b = self.geometry.neighbours(label).pop()
                if self._verbose >= 1:
                    print(f"{b} is selected to perform LC")
            self.local_complement(b, -1)

            if self._verbose >= 1:
                print(f"reduced {label} to {self.bases.pauli_base(label)}")

            self.measure(label)
            self.local_complement(b)

    def measure(self, label):
        if label not in self.output_layer:
            base = self.bases.pauli_base(label)
            direction = self.bases.pauli_sign(label)

            if self._verbose >= 2:
                print(f"simulating qubit {label} in base {base} with direction {direction}")
            if base == 'x':
                self.x_measurement(label)
            elif base == 'y':
                self.y_measurement(label)
            elif base == 'z':
                self.z_measurement(label)
            else:
                return False
            return True
        return False

    def eliminate_clifford(self):
        # succeed = True
        # while succeed:
        succeed = self.eliminate_pauli()
        self.eliminate_disconnected()
        self.fuse_nodes()

    def eliminate_pauli(self):
        # self.draw()
        # plt.title(f"Initial graph state with {len(self.geometry.nodes())} nodes")
        # plt.show()

        flag = False
        # Step 1 eliminate pauli
        for node in self.geometry.nodes():
            f = self.measure(node)
            flag = flag or f

        # self.draw()
        # plt.title(f"Reduced linear graph state consist {len(self.geometry.nodes())} nodes")
        # plt.show()

        return flag

    def eliminate_disconnected(self):

        # step 2 remove isolated nodes
        for node in self.geometry.nodes():
            if self.geometry.isolated(node) and node not in self.output_layer:
                self.bases.cutoff(node)
                self.geometry.cutoff(node)
                self.dependency.cutoff(node)

        # self.draw()
        # plt.title(f"Graph state after disconnected nodes removed consist {len(self.geometry.nodes())} nodes")
        # plt.show()

    def fuse_nodes(self):

        for node in self.geometry.nodes():
            # print(f"{node} is measured in {self.bases.measurement_plane(node)} plane "
            #       f"dependent on nodes {self.dependency.dep_map[node]}")
            # If it is a non-output leaf node and measured in ZY-plane
            if self.geometry.degree(node) == 1 and \
                    self.bases.measurement_plane(node) == 'zy' and \
                    node not in self.output_layer and \
                    self.bases.measurement_plane(list(self.geometry.neighbours(node))[0]) == 'xy':

                center = list(self.geometry.neighbours(node))[0]

                if self.dependency.correction_base(node) != 'z':
                    self.local_complement(node)
                # Update the angle on the center node
                # print(f"{center} has angle {self.bases.angle(center)}")
                self.bases.rotate(center, -self.bases.angle(node), 'z')
                # print(f"{center} is rotated by {self.bases.angle(node)} rad")
                # print(f"{center} has angle {self.bases.angle(center)} after the rotation")
                # Cutoff the leaf node
                self.dependency.cutoff(node)
                self.geometry.cutoff(node)
                self.bases.cutoff(node)
                # print(f"{node} is fused")

        # self.draw()
        # plt.title(f"graph state with nodes fused consist{len(self.geometry.nodes())} nodes")
        # plt.show()

    def schedule(self) -> (List[any], int):
        """
        Schedule an optimized measurement sequence
        :return: a queue of nodes as measurement sequence and the size of register required
        """
        # Allocate space for helper data
        geometry: nx.Graph = nx.Graph.copy(self.geometry.G)
        dep_map: Dict[any, Set[any]] = {node: self.dependency.dep_map[node].copy() for node in
                                        self.dependency.dep_map.keys()}
        qreg: Set[any] = set()  # virtual register
        queue: Set[any] = set()  # measurable queue
        sequence: List[any] = []  # measurement sequence
        size: int = 0  # qubits required

        # loop until everything is measured
        while len(geometry.nodes()) > 0:
            # Search for all measurable qubit
            for node in geometry.nodes():
                if node not in dep_map or len(dep_map[node]) == 0:
                    queue.add(node)

            # Search for the qubit to measure
            delta: int = np.inf
            node_min: any = None
            delta_set_min: Set[any] = set()
            for node in queue:
                delta_set = set(geometry.neighbors(node))
                delta_set.add(node)
                delta_set = delta_set.difference(qreg)
                # CASE 1: delta = 0
                if len(delta_set) == 0 and (node_min is None or geometry.degree(node) > geometry.degree(node_min)):
                    node_min = node
                    delta = 0

                elif len(delta_set) < delta:
                    delta = len(delta_set)
                    node_min = node
                    delta_set_min = delta_set

            # Compute the resource required
            size = max(size, len(qreg) + delta)
            # print(f"{node_min} is measured with delta={delta} and register size {size}")

            # Add the node and neighbours to the virtual register
            for node in delta_set_min:
                qreg.add(node)
            for node in geometry.nodes():
                if node in dep_map:
                    if node_min in dep_map[node]:
                        dep_map[node].remove(node_min)

            # Remove node from graph and push the node to the measurement sequence
            geometry.remove_node(node_min)
            qreg.remove(node_min)
            queue.remove(node_min)
            sequence.append(node_min)

        # Verify sequence
        for i in range(len(sequence)):
            if sequence[i] in dep_map:
                for source in dep_map[sequence[i]]:
                    if source in sequence[i:]:
                        print(f"error: {sequence[i]} measured before {source}")
                        break

        # print(f"scheduled with size {size}")

        return sequence, size

    def schedule_2(self) -> (List[any], int):
        """
        Schedule an optimized measurement sequence
        :return: a queue of nodes as measurement sequence and the size of register required
        """
        # Allocate space for helper data
        geometry: nx.Graph = nx.Graph.copy(self.geometry.G)
        dep_map: Dict[any, Set[any]] = {node: self.dependency.dep_map[node].copy() for node in
                                        self.dependency.dep_map.keys()}
        qreg: Set[any] = set()  # virtual register
        queue: Set[any] = set()  # measurable queue
        sequence: List[any] = []  # measurement sequence
        size: int = 0  # qubits required

        # loop until everything is measured
        while len(geometry.nodes()) > 0:
            # Search for all measurable qubit
            for node in geometry.nodes():
                if node not in dep_map or len(dep_map[node]) == 0:
                    queue.add(node)

            # Search for the qubit to measure
            delta: int = np.inf
            node_min: any = None
            delta_set_min: Set[any] = set()
            for node in queue:
                delta_set = set(geometry.neighbors(node))
                delta_set.add(node)
                delta_set = delta_set.difference(qreg)
                # CASE 1: delta = 0
                if len(delta_set) == 0 and (node_min is None or geometry.degree(node) > geometry.degree(node_min)):
                    node_min = node
                    delta = 0

                # TEST: choose the option closest to current register size
                elif len(delta_set) < size:
                    if len(delta_set) > delta or node_min is None:
                        delta = len(delta_set)
                        node_min = node
                        delta_set_min = delta_set

                elif len(delta_set) < delta:
                    delta = len(delta_set)
                    node_min = node
                    delta_set_min = delta_set

            # Compute the resource required
            size = max(size, len(qreg) + delta)
            # print(f"{node_min} is measured with delta={delta} and register size {size}")

            # Add the node and neighbours to the virtual register
            for node in delta_set_min:
                qreg.add(node)
            for node in geometry.nodes():
                if node in dep_map:
                    if node_min in dep_map[node]:
                        dep_map[node].remove(node_min)

            # Remove node from graph and push the node to the measurement sequence
            geometry.remove_node(node_min)
            qreg.remove(node_min)
            queue.remove(node_min)
            sequence.append(node_min)

        # Verify sequence
        for i in range(len(sequence)):
            if sequence[i] in dep_map:
                for source in dep_map[sequence[i]]:
                    if source in sequence[i:]:
                        print(f"error: {sequence[i]} measured before {source}")
                        break

        print(f"scheduled with size {size}")

        return sequence, size

    def compile(self) -> (QuantumCircuit, Dict[any, int]):
        """
        Compile measurement sequence into measurement-based quantum circuit
        :return:
        """

        nodes = self.geometry.nodes()
        graph_size = len(nodes)
        geometry = nx.Graph.copy(self.geometry.G)

        measurement_angles = {node: self.bases.angle(node) for node in nodes}
        measurement_planes = {node: self.bases.measurement_plane(node) for node in nodes}
        correction_bases = {node: self.dependency.correction_base(node) for node in nodes}
        correction_mask = self.dependency.dep_map

        sequence, reg_size = self.schedule()

        circuit = QuantumCircuit(reg_size, graph_size)
        qreg_map = dict()
        creg_map = {sequence[i]: i for i in range(graph_size)}
        free_qubit = set(range(reg_size))

        for node in sequence:
            # Allocate memory
            if node not in qreg_map:
                qreg_map[node] = free_qubit.pop()
                circuit.reset(qreg_map[node])
                circuit.h(qreg_map[node])

            # Construct partial graph state
            for next_node in geometry.neighbors(node):
                if next_node not in qreg_map:
                    qreg_map[next_node] = free_qubit.pop()
                    circuit.reset(qreg_map[next_node])
                    circuit.h(qreg_map[next_node])
                circuit.cz(qreg_map[node], qreg_map[next_node])

            # Process correction
            correction = circuit.x if correction_bases[node] == 'x' \
                else circuit.y if correction_bases[node] == 'y' else circuit.z
            if node in correction_mask:
                for prev_node in correction_mask[node]:
                    correction(qreg_map[node]).c_if(creg_map[prev_node], 1)

            # Measure node
            if measurement_planes[node] == "xy":
                circuit.rz(-measurement_angles[node], qreg_map[node])
                circuit.h(qreg_map[node])
            elif measurement_planes[node] == "zy":
                circuit.rx(measurement_angles[node], qreg_map[node])
            else:
                circuit.ry(measurement_angles[node], qreg_map[node])
                circuit.h(qreg_map[node])
            circuit.measure(qreg_map[node], creg_map[node])

            # Deallocate memory
            reg_id = qreg_map.pop(node)
            free_qubit.add(reg_id)
            circuit.barrier()
            geometry.remove_node(node)

        return circuit, creg_map

    def process_outcomes(self,
                         outome_counts: Dict[str, int],
                         creg_map: Dict[any, int]):
        output_reg = [creg_map[node] for node in self.output_layer]
        processed_counts: Dict[str, int] = dict()
        for word, count in outome_counts.items():
            word = word[::-1]
            masked_word = ''
            for reg_id in output_reg:
                masked_word += word[reg_id]
            masked_word = masked_word[::-1]
            if masked_word in processed_counts:
                processed_counts[masked_word] += count
            else:
                processed_counts[masked_word] = count
        return processed_counts

    def run(self, shot):
        circuit, creg_map = self.compile()
        simulator = QasmSimulator()
        qasm_circuit = transpile(circuit, simulator)
        job = simulator.run(qasm_circuit, shot=shot)
        result = job.result()
        counts = result.get_counts(qasm_circuit)
        return self.process_outcomes(counts, creg_map)

    def draw_cluster(self, ax=None) -> None:
        """
        Draw the graph state on a grid lattice
        """
        pos = {node: (node[1], node[0]) for node in self.geometry.nodes()}
        # pos = nx.circular_layout(self.geometry.G)
        nx.draw_networkx_nodes(self.geometry.G, pos,
                               node_color=[
                                   'r' if self.bases.measurement_plane(node) == 'zy'
                                   else 'b' if self.bases.measurement_plane(node) == 'xz'
                                   else 'w'
                                   for node in self.geometry.nodes()],
                               edgecolors='k',
                               node_size=[
                                   200 if node in self.output_layer
                                   else 200
                                   for node in self.geometry.nodes()], ax=ax)
        nx.draw_networkx_labels(self.geometry.G, pos,
                                labels={label:
                                            f"{self.bases.pauli_base(label)}" if label in self.output_layer
                                            else f"{self.bases.pauli_base(label)}"
                                        for label in self.geometry.nodes()})
        nx.draw_networkx_edges(self.dependency.to_dag(), pos,
                               edge_color='c', connectionstyle="arc3,rad=0.1", arrows=True)
        nx.draw_networkx_edges(self.geometry.G, pos, arrows=False)

    def draw_graph(self, ax=None) -> None:
        """
        Draw the graph state on a ring
        """
        pos = nx.spring_layout(self.geometry.G)
        nx.draw_networkx_nodes(self.geometry.G, pos,
                               node_color=[
                                   'r' if self.bases.measurement_plane(node) == 'zy'
                                   else 'b' if self.bases.measurement_plane(node) == 'xz'
                                   else 'w'
                                   for node in self.geometry.nodes()],
                               edgecolors='k',
                               node_size=[
                                   60 if node in self.output_layer
                                   else 50
                                   for node in self.geometry.nodes()], ax=ax)
        # nx.draw_networkx_labels(self.geometry.G, pos,
        #                         labels={
        #                             label: f"{self.dependency.correction_base(label)}"
        #                             for label in self.geometry.nodes()})
        # nx.draw_networkx_edges(self.dependency.to_dag(), pos,
        #                        edge_color='c', connectionstyle="arc3,rad=0.1", arrows=True)
        nx.draw_networkx_edges(self.geometry.G, pos, arrows=False)

    def draw(self, ax=None) -> None:
        """
        Draw the graph state accordingly.
        """
        if self._reduced:
            self.draw_graph(ax)
        else:
            self.draw_cluster(ax)

    # Other stuff for assertion
    # Assert measurement dependencies on fusion nodes
    def assert_fusion_nodes(self):
        for node in self.geometry.nodes():
            if self.geometry.degree(node) == 1 and \
                    self.bases.measurement_plane(node) == 'zy' and \
                    node not in self.output_layer:
                if node in self.dependency.dep_map:
                    center = list(self.geometry.neighbours(node))[0]
                    # print(f"{node} is to be fused into with dependencies {graph.dependency.dep_map[node]}")
                    # print(f"{center} is dependent on {graph.dependency.dep_map[center]}")
                    # print(graph.dependency.dep_map[node] == graph.dependency.dep_map[center])
                    if center in self.dependency.dep_map:
                        if not self.dependency.dep_map[node] == self.dependency.dep_map[center]:
                            print(f"center dependencies on node {center} does not agree"
                                  f"measured in {self.bases.measurement_plane(center)} plane")
                    else:
                        print(
                            f"no center dependencies on node {center} "
                            f"measured in {self.bases.measurement_plane(center)} plane")
