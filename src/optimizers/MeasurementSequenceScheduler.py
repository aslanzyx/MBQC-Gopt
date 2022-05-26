from typing import Dict, List, Set
import networkx as nx
import numpy as np


class MeasurementSequenceScheduler:
    def __init__(self, geometry: nx.Graph, dep_map: Dict[any, Set[any]]):
        self.geometry: nx.Graph = nx.Graph.copy(geometry)
        self.dep_map: Dict[any, Set[any]] = {node: dep_map[node].copy() for node in
                                             dep_map.keys()}
        self.qreg: Set[any] = set()     # virtual register
        self.queue: Set[any] = set()    # measurable queue
        self.sequence: List[any] = []   # measurement sequence
        self.size: int = 0              # qubits required

    def schedule(self) -> (List[any], int):
        """
        Schedule an optimized measurement sequence
        :return: a queue of nodes as measurement sequence and the size of register required
        """

        # Loop until everything is measured
        while len(self.geometry.nodes()) > 0:
            # Search for all measurable qubit
            for node in self.geometry.nodes():
                if node not in self.dep_map or len(self.dep_map[node]) == 0:
                    self.queue.add(node)

            # Search for the qubit to measure
            delta: int = np.inf
            node_min: any = None
            delta_set_min: Set[any] = set()
            for node in self.queue:
                delta_set = set(self.geometry.neighbors(node))
                delta_set.add(node)
                delta_set = delta_set.difference(self.qreg)
                if len(delta_set) < delta:
                    delta = len(delta_set)
                    node_min = node
                    delta_set_min = delta_set

            # Compute the resource required
            self.size = max(self.size, len(self.qreg) + delta)
            print(f"{node_min} is measured with delta={delta} and register size {self.size}")

            # Add the node and neighbours to the virtual register
            for node in delta_set_min:
                self.qreg.add(node)
            for node in self.geometry.nodes():
                if node in self.dep_map:
                    if node_min in self.dep_map[node]:
                        self.dep_map[node].remove(node_min)

            # Remove node from graph and push the node to the measurement sequence
            self.geometry.remove_node(node_min)
            self.qreg.remove(node_min)
            self.queue.remove(node_min)
            self.sequence.append(node_min)

        # Verify sequence
        for i in range(len(self.sequence)):
            if self.sequence[i] in self.dep_map:
                for source in self.dep_map[self.sequence[i]]:
                    if source in self.sequence[i:]:
                        print(f"error: {self.sequence[i]} measured before {source}")
                        break

        print(f"scheduled with size {self.size}")
