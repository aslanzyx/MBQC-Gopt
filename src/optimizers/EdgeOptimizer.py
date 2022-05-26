import json
from typing import List, Set, Dict

import networkx as nx
import numpy as np

from graphoptim.core import GeometryLayer, GraphState


# TODO: Optimize performance
class EdgeOptimizer:
    def __init__(self, graph_state: GraphState, max_depth: int = 100, traverse_all=False, rev=False):

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
        """

        max_degree_nodes, max_degree = self.current_geometry.max_degree_nodes()
        if not self.traverse_all:
            lc_nodes_todo = self.current_geometry.boundary_nodes(max_degree_nodes)
        else:
            lc_nodes_todo = list(self.current_geometry.nodes())
        cur_edge_size = len(self.current_geometry.G.edges())
        cur_id = len(self.lc_map) - 1

        if cur_edge_size < self.minimax_edge_size:
            self.optimized_idx = cur_id
            self.minimax_edge_size = cur_edge_size

        # Compute metadata for LC graphs on each node
        metadata_less: List[(any, int)] = []
        metadata_more: List[(any, int)] = []
        for node in lc_nodes_todo:
            self.current_geometry.local_complement(node)
            edge_size = len(self.current_geometry.G.edges())
            self.current_geometry.local_complement(node)
            if edge_size < cur_edge_size:
                metadata_less.append((node, edge_size))
            elif edge_size > cur_edge_size:
                metadata_more.append((node, edge_size))

        metadata_less.sort(key=lambda meta: meta[1])
        if self.rev:
            metadata_more.sort(key=lambda meta: meta[1], reverse=True)
        metadata = metadata_less + metadata_more

        self.depth += 1

        # print(f"depth {self.depth} reached "
        #       f"degree of current graphs recorded {self.current_geometry.max_degree_nodes()[1]} "
        #       f"reg size required {self.reg_sizes[cur_id]}")

        for node, _ in metadata:
            self.current_geometry.local_complement(node)
            if not self.has_isomorphic():
                # DP: record current geometry
                self.lc_map.append((cur_id, node))
                self.graph_traversed.append(nx.Graph.copy(self.current_geometry.G))
                reg_size = self.graph_state.schedule()[1]
                self.min_reg_size = min(self.min_reg_size, reg_size)
                self.reg_sizes.append(reg_size)
                self.track.append({"depth": self.depth,
                                   "reg_size": reg_size,
                                   "max_degree": self.current_geometry.max_degree_nodes()[1],
                                   "edge_size": len(self.current_geometry.G.edges())})

                # DFS recursion
                self.execute()
            else:
                _, reg_size = self.graph_state.schedule()
                isomorphic_idx = self.find_isomorphic()
                if reg_size < self.reg_sizes[isomorphic_idx]:
                    self.lc_map[isomorphic_idx] = (cur_id, node)
                    self.reg_sizes[isomorphic_idx] = reg_size
                    self.min_reg_size = min(self.min_reg_size, reg_size)
                # print(f"Isomorphism "
                #       f"degree of current graphs recorded {self.current_geometry.max_degree_nodes()[1]} "
                #       f"reg size required {self.reg_sizes[cur_id]}")
                self.track.append({"depth": self.depth,
                                   "reg_size": reg_size,
                                   "max_degree": self.current_geometry.max_degree_nodes()[1],
                                   "edge_size": len(self.current_geometry.G.edges())})

            self.current_geometry.local_complement(node)

            if self.depth >= self.max_depth:
                break

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
