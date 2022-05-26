from typing import Dict, Set
from graphoptim.core.BlochSphere import BlochSphere
import networkx as nx
import matplotlib.pyplot as plt


class MeasurementDependencyLayer:
    def __init__(self, dependency_map: Dict[any, Set[any]]):
        self.dep_map: Dict[any, Set[any]] = dependency_map
        self.correction: Dict[any, BlochSphere] = {node: BlochSphere('x') for node in self.dep_map.keys()}

    def correction_base(self, node):
        if node in self.correction:
            return self.correction[node].pauli_base()
        else:
            return ""

    def is_measurable(self, node):
        return node in self.dep_map.keys()

    def rotate_sqrt_x(self, node, direction):
        if node in self.correction:
            self.correction[node].rotate_sqrt_x(direction)

    def rotate_sqrt_z(self, node, direction):
        if node in self.correction:
            self.correction[node].rotate_sqrt_z(direction)

    def cutoff(self, node):
        if node in self.correction.keys():
            self.correction.pop(node)
        if node in self.dep_map.keys():
            self.dep_map.pop(node)
        for target, sources in self.dep_map.items():
            if node in sources:
                self.dep_map[target].remove(node)

    def to_dag(self):
        dag = nx.DiGraph()
        for node, sources in self.dep_map.items():
            for source in sources:
                dag.add_edge(source, node)
        return dag
