import copy
import json
from typing import List, Set, Dict

import networkx as nx
import numpy as np

from graphoptim.core import GeometryLayer, GraphState


# TODO: Optimize performance
class EdgeOptimizerBFS:
    def __init__(self, graph_state: GraphState, max_depth: int = 100, traverse_all=False, rev: bool = False):

        self.optimized_idx = 0
        self.minimax_edge_size = np.inf

        self.max_depth = max_depth
        self.depth = 0

        self.current_graph_idx = 0
        self.current_geometry = graph_state.geometry

        self.graph_traversed: List[nx.Graph] = []
        self.lc_map: List[(int, any)] = []

        self.graph_state = graph_state
        self.reg_sizes = [self.graph_state.schedule()[1]]
        self.min_reg_size = np.inf
        self.track = []
        self.rev = rev
        self.traverse_all = traverse_all

        self.queue = []

    def has_isomorphic(self):
        for H in self.graph_traversed:
            if self.current_geometry.is_isomorphic(H):
                return True
        return False

    def find_isomorphic(self):
        for i in range(len(self.graph_traversed)):
            if self.current_geometry.is_isomorphic(self.graph_traversed[i]):
                return i
        return None

    def lc_delta(self, node: any) -> (Dict[any, int], Set[any], int):

        search_set = self.current_geometry.neighbours(node)
        delta: Dict[any, int] = {node: degree for node, degree in
                                 self.current_geometry.nodes(search_set)}
        self.current_geometry.local_complement(node)
        for node, degree in self.current_geometry.nodes(search_set):
            delta[node] = degree - delta[node]
        self.current_geometry.local_complement(node)

        return delta, self.current_geometry.max_degree_nodes(self.current_geometry.G, search_set)

    def execute(self):
        """
        Traverse through nodes
        :return:
        """
        l1_traversed_nodes = [None]
        l2_traversed_nodes = []

        self.queue.append(copy.deepcopy(self.graph_state))

        while len(self.queue) > 0 and self.depth < self.max_depth:
            H: GraphState = self.queue.pop(0)
            parent_lc_node = l1_traversed_nodes.pop(0)
            if not self.traverse_all:
                max_degree_nodes, max_degree = H.geometry.max_degree_nodes()
                lc_nodes_todo = H.geometry.boundary_nodes(max_degree_nodes)
            else:
                lc_nodes_todo = list(H.geometry.nodes())

            cur_edge_size = len(H.geometry.G.edges())
            # Compute metadata for LC graphs on each node
            metadata_less: List[(any, int)] = []
            metadata_more: List[(any, int)] = []
            for node in lc_nodes_todo:
                H.local_complement(node)
                edge_size = len(H.geometry.G.edges())
                if edge_size < cur_edge_size:
                    metadata_less.append((node, edge_size))
                elif edge_size > cur_edge_size:
                    metadata_more.append((node, edge_size))
                self.depth += 1
                _, reg_size = H.schedule()
                self.track.append({"depth": self.depth,
                                   "reg_size": reg_size,
                                   "max_degree": H.geometry.max_degree_nodes()[1],
                                   "edge_size": len(H.geometry.G.edges())})
                self.min_reg_size = min(self.min_reg_size, reg_size)
                self.minimax_edge_size = min(self.minimax_edge_size, len(H.geometry.G.edges()))
                H.local_complement(node)

            metadata_less.sort(key=lambda meta: meta[1])
            if self.rev:
                metadata_more.sort(key=lambda meta: meta[1], reverse=True)
            metadata = metadata_less + metadata_more

            for node, _ in metadata:
                if node != parent_lc_node:
                    H.local_complement(node)
                    self.queue.append(copy.deepcopy(H))
                    H.local_complement(node)

            l2_traversed_nodes += [node for node, _ in metadata]

            if len(l1_traversed_nodes) == 0:
                l1_traversed_nodes = [node for node in l2_traversed_nodes]
                l2_traversed_nodes = []
            print(f"depth {self.depth} reached")

    def optimized_lc_sequence(self) -> List[any]:
        ptr: int = self.optimized_idx
        sequence: List[any] = []

        while ptr >= 0:
            ptr, node = self.lc_map[ptr]
            sequence.append(node)

        return sequence[::-1]

    def save_track(self, filename):
        with open(filename, 'w') as f:
            track = {log["depth"]: log for log in self.track}
            track["node_size"] = len(self.current_geometry.nodes())
            json.dump(track, f)
