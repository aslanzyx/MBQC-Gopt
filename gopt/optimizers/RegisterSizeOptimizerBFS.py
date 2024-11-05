import json
from typing import List, Set, Dict

import networkx as nx
import numpy as np

from graphoptim.core import GeometryLayer, GraphState


class RegisterSizeOptimizerBFS:

    def __init__(self, graph_state: GraphState, max_depth: int = 5000):

        self.optimized_idx = 0
        self.minimax_degree = np.inf

        self.max_depth = max_depth
        self.depth = 0

        self.current_graph_idx = 0
        self.current_geometry = graph_state.geometry

        self.graph_traversed: List[nx.Graph] = []
        self.lc_map: List[(int, any)] = []

        self.graph_state: GraphState = graph_state
        self.minimax_size = np.inf

        self.track = []

    def has_isomorphic(self):
        for H in self.graph_traversed:
            if self.current_geometry.is_isomorphic(H):
                return True
        return False

    def execute(self):
        _, size = self.graph_state.schedule()
        lc_nodes_todo = list(self.current_geometry.nodes())
        cur_id = len(self.lc_map) - 1

        if size < self.minimax_size:
            self.optimized_idx = cur_id
            self.minimax_size = size

        # Compute metadata for LC graphs on each node
        metadata: List[(any, int)] = []
        for node in lc_nodes_todo:
            self.current_geometry.local_complement(node)
            _, size = self.graph_state.schedule()
            metadata.append((node, size))
            self.depth += 1
            self.minimax_size = min(self.minimax_size, size)
            self.track.append({
                "depth":
                self.depth,
                "reg_size":
                size,
                "max_degree":
                self.current_geometry.max_degree_nodes()[1],
                "edge_size":
                len(self.current_geometry.G.edges())
            })
            self.current_geometry.local_complement(node)

        metadata.sort(key=lambda meta: meta[1])

        for node, _ in metadata:
            self.current_geometry.local_complement(node)
            if not self.has_isomorphic():
                # DP: record current geometry
                self.lc_map.append((cur_id, node))
                self.graph_traversed.append(
                    nx.Graph.copy(self.current_geometry.G))

                # DFS recursion
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
            track = {log["depth"]: log for log in self.track}
            track["node_size"] = len(self.current_geometry.nodes())
            json.dump(track, f)
