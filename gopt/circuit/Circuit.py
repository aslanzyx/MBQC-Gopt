from math import pi
import networkx as nx

from ..graph import GraphState
from ..Utils import is_pauli_angle
from ..core import BlochSphere


class Circuit:
    """
    An abstraction of the circuit model for MBQC
    """

    def __init__(self, size):
        self.size = size
        self.cluster_stacks: list[list[float]] = [[0] for _ in range(size)]
        self.stack_ptrs: list[int] = [1] * size
        self.entanglement_edges: set[((int, int), (int, int))] = set()
        self.corrections: list[dict[(int, int), BlochSphere]] = [dict() for _ in range(size)]
        self.dependencies: dict[(int, int), set[(int, int)]] = dict()

        self._finalized = False

    def add_rotation_sequence(self, wire_id: int, angles: list[float]) -> None:
        """
        Add a series of rotations, alternating in Z and X base
        wire_id: the qubit index to rotate
        angles: a list of rotation angles
        """
        for angle in angles:
            self.cluster_stacks[wire_id].append(angle)
            # Process corrections
            if is_pauli_angle(angle):
                # Propagate corrections if Pauli
                for source in self.corrections[wire_id].keys():
                    self.corrections[wire_id][source].rotate_z(-angle)
                    self.corrections[wire_id][source].rotate_h()
            else:
                # Add dependencies if non-Pauli
                for source, correction in self.corrections[wire_id].items():
                    if correction.pauli_base() != 'z':
                        self.dependencies[source].add(
                            (wire_id, self.stack_ptrs[wire_id]))
                # Add new correction source
                new_source = (wire_id, self.stack_ptrs[wire_id])
                self.corrections[wire_id][new_source] = BlochSphere('z')
                self.dependencies[new_source] = set()
                # Rotate upon Hadamard
                for source in self.corrections[wire_id].keys():
                    self.corrections[wire_id][source].rotate_h()
            # Update stack pointer
            self.stack_ptrs[wire_id] += 1

    def cnot(self, control_id: int, target_id: int) -> None:
        """
        Add CNOT gate
        """
        # Add entanglement edge
        self.entanglement_edges.add(
            ((control_id, self.stack_ptrs[control_id]),
             (target_id, self.stack_ptrs[target_id] - 1))
        )
        # Process corrections
        for source, correction in list(self.corrections[control_id].items()):
            if correction.pauli_base() != 'z':
                if source in self.corrections[target_id]:
                    if self.corrections[target_id][source].pauli_base() == 'x':
                        self.corrections[target_id].pop(source)
                    else:
                        self.corrections[target_id][source].rotate_sqrt_x(1)
                else:
                    self.corrections[target_id][source] = BlochSphere('x')
        for source, correction in list(self.corrections[target_id].items()):
            if correction.pauli_base() != 'x':
                if source in self.corrections[control_id]:
                    if self.corrections[control_id][source].pauli_base() == 'z':
                        self.corrections[control_id].pop(source)
                    else:
                        self.corrections[control_id][source].rotate_sqrt_z(1)
                else:
                    self.corrections[control_id][source] = BlochSphere('z')
        # Add margin
        self.add_rotation_sequence(target_id, [0, 0])
        self.add_rotation_sequence(control_id, [0, 0])

    def cz(self, control_id: int, target_id: int):
        """
        Add CZ gate
        """
        # Add entanglement edge
        self.entanglement_edges.add(
            ((control_id, self.stack_ptrs[control_id]),
             (target_id, self.stack_ptrs[target_id]))
        )
        # Process corrections
        for source, correction in list(self.corrections[control_id].items()):
            if correction.pauli_base() != 'z':
                if source in self.corrections[target_id]:
                    if self.corrections[target_id][source].pauli_base() == 'z':
                        self.corrections[target_id].pop(source)
                    else:
                        self.corrections[target_id][source].rotate_sqrt_z(1)
                else:
                    self.corrections[target_id][source] = BlochSphere('z')
        for source, correction in list(self.corrections[target_id].items()):
            if correction.pauli_base() != 'z':
                if source in self.corrections[control_id]:
                    if self.corrections[control_id][source].pauli_base() == 'z':
                        self.corrections[control_id].pop(source)
                    else:
                        self.corrections[control_id][source].rotate_sqrt_z(1)
                else:
                    self.corrections[control_id][source] = BlochSphere('z')

    def rx(self, wire_id: int, angle: float) -> None:
        """
        Rotate in X base
        """
        self.add_rotation_sequence(wire_id, [0, angle])

    def rz(self, wire_id: int, angle: float) -> None:
        """
        Rotate in Z base
        """
        self.add_rotation_sequence(wire_id, [angle, 0])

    def x(self, wire_id: int) -> None:
        """
        Flip in X base
        """
        self.rx(wire_id, pi)

    def z(self, wire_id: int) -> None:
        """
        Flip in Z base
        """
        self.rz(wire_id, pi)

    def s(self, wire_id: int) -> None:
        """
        S gate
        """
        self.rz(wire_id, pi / 2)

    def t(self, wire_id: int) -> None:
        """
        T gate
        """
        self.rz(wire_id, pi / 4)

    def s_dagger(self, wire_id: int) -> None:
        self.rz(wire_id, -pi / 2)

    def t_dagger(self, wire_id: int) -> None:
        self.rz(wire_id, -pi / 4)

    def h(self, wire_id: int) -> None:
        """
        Hadamard gate
        """
        self.add_rotation_sequence(wire_id, [0])

    def add_outputs(self) -> None:
        """
        Add output qubits
        """
        if self._finalized:
            # raise Exception("Output layer has already been added.")
            print("Output layer has already been added.")
        else:
            for i in range(self.size):
                # Process measurement dependencies
                for source, correction in self.corrections[i].items():
                    if correction.pauli_base() != 'z':
                        self.dependencies[source].add((i, self.stack_ptrs[i]))
                self._finalized = True

    def to_graph_state(self):
        # Create variables for constructing graph state
        geometry_graph: nx.Graph = nx.Graph()
        dependency_graph: dict[any, set[any]] = dict()
        angle_map: dict[(int, int), any] = dict()
        output_nodes: list[(int, int)] = []
        # Finalize the cluster state
        self.add_outputs()
        # Add wires
        for i in range(self.size):
            for j in range(self.stack_ptrs[i]):
                geometry_graph.add_edge((i, j), (i, j + 1))
                angle_map[(i, j)] = self.cluster_stacks[i][j]
            # Add the output qubit
            angle_map[(i, self.stack_ptrs[i])] = None
            output_nodes.append((i, self.stack_ptrs[i]))
        # Add entanglement edges
        for u, v in self.entanglement_edges:
            geometry_graph.add_edge(u, v)
        # Construct dependency graph
        for source, targets in self.dependencies.items():
            for target in targets:
                if target not in dependency_graph:
                    dependency_graph[target] = set()
                dependency_graph[target].add(source)
        return GraphState(geometry_graph, dependency_graph,
                          angle_map, output_nodes)

    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self.size) + '\n')
        for angles in self.cluster_stacks:
            file.write(','.join([str(angle) for angle in angles]) + '\n')
        for entanglement_edge in self.entanglement_edges:
            file.write(str(entanglement_edge) + '\n')
        file.close()
