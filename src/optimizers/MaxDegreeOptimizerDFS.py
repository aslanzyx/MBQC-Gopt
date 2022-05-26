import json
from typing import List, Set, Dict

import networkx as nx
import numpy as np

from graphoptim.core import GeometryLayer, GraphState


# TODO: Optimize performance
class MaxDegreeOptimizerDFS:
    def __init__(self, graph_state: GraphState, max_depth: int = 100,
                 traverse_all=False, rev: bool = False, greedy=True):

        self.current_graph_idx = 0
        self.current_geometry = graph_state.geometry
        self.graph_traversed: List[nx.Graph] = []
        self.lc_map: List[(int, any)] = []
        self.graph_state = graph_state

        self.optimized_idx = 0
        self.optimized_reg_size_idx = 0
        self.optimized_max_degree_idx = 0
        self.optimized_degree_norm_idx = 0

        self.min_edge_size = np.inf
        self.min_reg_size = np.inf
        self.minimax_degree = np.inf
        self.min_degree_norm = np.inf

        self.reg_sizes = [self.graph_state.schedule()[1]]

        self.max_depth = max_depth
        self.depth = 0

        self.track = dict()
        self.graph_reg = dict()
        self.isomorphism_reg = dict()

        self.rev = rev
        self.traverse_all = traverse_all
        self.greedy = greedy

    def has_isomorphic(self):
        for H in self.graph_traversed:
            if self.current_geometry.is_isomorphic(H):
                return True
        return False

    def find_isomorphic(self):
        for key, G in self.graph_reg.items():
            if self.current_geometry.is_isomorphic(G):
                return key
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

        if self.depth >= self.max_depth:
            return

        if not self.traverse_all:
            max_degree_nodes, max_degree = self.current_geometry.max_degree_nodes()
            lc_nodes_todo = self.current_geometry.boundary_nodes(max_degree_nodes).union(max_degree_nodes)
        else:
            lc_nodes_todo = self.current_geometry.nodes()

        cur_edge_size = len(self.current_geometry.G.edges())
        cur_id = len(self.lc_map) - 1

        # Compute metadata for LC graphs on each node
        metadata_less: List[(any, int)] = []
        metadata_more: List[(any, int)] = []
        for node in lc_nodes_todo:
            self.depth += 1

            self.current_geometry.local_complement(node)

            # compute computational resource
            _, reg_size = self.graph_state.schedule()
            degree_norm = np.linalg.norm([d for _, d in self.current_geometry.G.degree])
            minimax_degree = self.current_geometry.max_degree_nodes()[1]
            edge_size = len(self.current_geometry.G.edges())

            if edge_size < cur_edge_size:
                metadata_less.append((node, minimax_degree, int(self.depth)))
            elif edge_size > cur_edge_size:
                metadata_more.append((node, minimax_degree, int(self.depth)))

            # record log
            self.track[self.depth] = {"depth": self.depth,
                                      "reg_size": reg_size,
                                      "max_degree": minimax_degree,
                                      "degree_norm": degree_norm,
                                      "edge_size": edge_size}

            # update min edge size
            if edge_size < self.min_edge_size:
                self.optimized_idx = self.depth
                self.min_edge_size = edge_size

            # update min computational resource
            if reg_size < self.min_reg_size:
                self.optimized_reg_size_idx = self.depth
                self.min_reg_size = reg_size

            # update min max degree
            if minimax_degree < self.minimax_degree:
                self.optimized_max_degree_idx = self.depth
                self.minimax_degree = minimax_degree

            # update min degree norm
            if degree_norm < self.min_degree_norm:
                self.optimized_degree_norm_idx = self.depth
                self.min_degree_norm = degree_norm

            # restore the graph geometry
            self.current_geometry.local_complement(node)

        metadata_less.sort(key=lambda meta: meta[1])
        if self.rev:
            metadata_more.sort(key=lambda meta: meta[1], reverse=False)
        metadata = metadata_less + metadata_more

        for node, _, depth in metadata:
            self.current_geometry.local_complement(node)
            print(f"{self.depth} reached")
            iso = self.find_isomorphic()
            self.graph_reg[depth] = nx.Graph.copy(self.current_geometry.G)
            if iso is None:
                self.execute()
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
            track = self.track
            track["node_size"] = len(self.current_geometry.nodes())
            track["min_reg_size"] = self.min_reg_size
            track["min_edge_size"] = self.min_edge_size
            track["minimax_degree"] = self.minimax_degree
            track["min_degree_norm"] = self.min_degree_norm

            track["min_reg_size_idx"] = self.optimized_reg_size_idx
            track["min_edge_size_idx"] = self.optimized_idx
            track["minimax_degree_idx"] = self.optimized_max_degree_idx
            track["min_degree_norm_idx"] = self.optimized_degree_norm_idx

            track["isomorphic_track"] = {key: {id: 0 for id in ids} for key, ids in self.isomorphism_reg.items()}
            json.dump(track, f)
