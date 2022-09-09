import networkx as nx
import numpy as np

from gopt.graph.GeometryLayer import GeometryLayer


class ZXGraph:
    def __init__(self, graph: nx.Graph, angle_map: dict[any, float], output_nodes: list[any], multiplier: float = 1):
        """
        Create a graph state in ZX-diagram
        graph: a networkx object describing the geometry
        angle_map: a diction of angles for each node
        output_nodes: the output node labels
        """
        self.geometry = GeometryLayer(graph)
        self.angle_map = angle_map
        self.output_nodes = output_nodes
        self.outcome_to_query = 0
        self.multiplier = multiplier
        pass

    def _local_comp(self, node: any):
        """
        Perform local complementation about the given node
        """
        # Cache partial graph node labels
        neighbours = self.geometry.neighbours(node)

        # Graph transformations
        self.geometry.local_complement(node)
        self._cut_node(node)

        # TODO: Angle transformations
        raise NotImplementedError("Angle transformation haven't been implemented")

    def _pivot(self, edge: (any, any)):
        """
        Perform pivoting about the given edge
        """
        # Cache partial graph node labels
        node_u, node_v = edge
        neighbours = self.geometry.neighbours(node_u).union(self.geometry.neighbours(node_v)).difference(
            {node_u, node_v})

        # Graph transformations
        self.geometry.local_complement(node_u)
        self.geometry.local_complement(node_v)
        self.geometry.local_complement(node_u)
        self._cut_node(node_u)
        self._cut_node(node_v)

        # TODO: Angle transformations
        raise NotImplementedError("Angle transformation haven't been implemented")

    def _cut_node(self, node: any):
        """
        Cut a node away from the graph
        """
        self.geometry.cutoff(node)
        self.angle_map.pop(node)

    def _fuse_2nary_identity(self, node: any):
        # Cache partial graph node labels
        node_u, node_v = self.geometry.neighbours(node)
        exclusive_neighbours = self.geometry.neighbours(node_u).difference(self.geometry.neighbours(node_v)).difference(
            {node})
        common_neighbours = self.geometry.neighbours(node_u).difference(exclusive_neighbours).difference({node})
        # Graph transformations
        self.geometry.cutoff(node)
        self.geometry.cutoff(node_u)
        for exclusive_neighbour in exclusive_neighbours:
            self.geometry.G.add_edge(exclusive_neighbour, node_v)
        for common_neighbour in common_neighbours:
            self.geometry.G.remove_edge(common_neighbour, node_v)
        if self.geometry.G.has_edge(node_v, node_v):
            self.geometry.G.remove_edge(node_v, node_v)
        # Angle transformations
        self._add_radius(node_v, self.angle_map.pop(node_u))
        self.angle_map.pop(node)
        return node_u

    def _add_radius(self, node: any, angle: float):
        """
        Helper function to add a certain radius to some angle without overflowing
        """
        self.angle_map[node] = (self.angle_map[node] + angle) % (2 * np.pi)

    def _apply_stabilizer(self, node: any):
        self.angle_map[node] = -self.angle_map[node]
        self._add_radius(node, 2 * np.pi)
        for neighbour in self.geometry.neighbours(node):
            self._add_radius(neighbour, np.pi)

    def _on_outcome_set(self):
        """
        Helper function to update the outcome info
        """
        mask = 1
        for i in range(len(self.output_nodes)):
            if self.outcome_to_query & mask:
                self._add_radius(self.output_nodes[i], np.pi)
            mask = mask << 1

    def _scan_to_elim(self):
        """
        Scan all nodes to eliminate
        """
        to_elim = set()
        for node, angle in self.angle_map.items():
            if angle % (np.pi / 2) == 0:
                to_elim.add(node)
        return to_elim

    def _reduce_by_fusion(self, to_elim: set[any]):
        """
        Reduce spider number by fusion
        """
        fused = set()
        for node in to_elim:
            if len(self.geometry.neighbours(node)) == 2:
                category = self.angle_map[node] // (np.pi / 2)
                if category % 2 == 0:
                    if category == 2:
                        self._apply_stabilizer(self.geometry.neighbours(node).pop())
                    removed_node = self._fuse_2nary_identity(node)
                    fused.add(node)
                    fused.add(removed_node)

        to_elim = to_elim.difference(fused)

        return to_elim

    def set_outcome_to_query(self, outcome: int):
        """
        Set outcome to current diagram
        Be sure to set that up before any reduction
        """
        self.outcome_to_query = outcome
        self._on_outcome_set()

    def eliminate_clifford(self):
        """
        Iteratively remove all Clifford parts in ths ZX-diagram
        """
        to_elim = self._scan_to_elim()
        to_elim = self._reduce_by_fusion(to_elim)
        flag = True
        while flag:
            eliminated = set()
            for node in to_elim:
                if node not in eliminated:
                    category = self.angle_map[node] // (np.pi / 2)
                    if category % 2 == 1:
                        if category == 3:
                            self._apply_stabilizer(node)
                        self._local_comp(node)
                        eliminated.add(node)
                    else:
                        if category % 2 == 0:
                            for neighbour in self.geometry.neighbours(node).intersection(to_elim):
                                neighbour_category = self.angle_map[neighbour] // (np.pi / 2)
                                if neighbour_category % 2 == 0:
                                    if category == 2:
                                        self._apply_stabilizer(neighbour)
                                    if neighbour_category == 2:
                                        self._apply_stabilizer(node)
                                    self._pivot((node, neighbour))
                                    eliminated.add(node)
                                    eliminated.add(neighbour)

                to_elim = to_elim.difference(eliminated)
                to_elim = self._reduce_by_fusion(to_elim)
            flag = len(eliminated) > 0

    def query_prob(self) -> float:
        # TODO: Hard compute the probability
        # TODO: Simply construct a graph state, apply rotation of given angles and project in <+| base

        # The self.geometry.G object is essentially the graph object you passed in
        # You obtain graph metadata directly as bellow to construct the graph state
        self.geometry.G.nodes()
        self.geometry.G.edges()

        # TASK 1: Create graph state
        # You could use any backend API as prefer.
        # I would suggest qiskit by IBM

        # TASK 2: Apply rotations
        # Think about the rotation direction!
        # Should they be of the same direction as indicated on the ZX-diagram?

        # TASK 3: Perform the projection and return the probability

        # Remove this line when you are done
        raise NotImplementedError("Method hasn't been implemented!")

    def bss_decomp(self) -> list[any]:
        # TODO: Perform BSS decompositions and return 7 graphs
        # TODO: Remember to update the multiplier variable

        # Remove this line when you are done
        raise NotImplementedError("Method hasn't been implemented!")

    def query_prob_with_decomp(self) -> float:
        # TODO: Simulate the the probability using BSS decomposition
        # TODO: You might want to use DFS for memory efficiency

        # Remove this line when you are done
        raise NotImplementedError("Method hasn't been implemented!")

    # The below ones are challenging to implement
    # Try to finish the above tasks before implement anything below
    def eliminate_clifford_multithread(self):
        # TODO: Here's a challenge to check your understanding
        # TODO: How to run the elimination process on a multicore system?

        # Remove this line when you are done
        raise NotImplementedError("Method hasn't been implemented!")

    def query_prob_with_decomp_multithread(self):
        # TODO: Here's another challenge
        # TODO: Try to implement the above method on a multicore system!

        # Remove this line when you are done
        raise NotImplementedError("Method hasn't been implemented!")

    def render(self):
        nx.draw(self.geometry.G,
                labels={node: f"{round(self.angle_map[node], 2)}" for node in self.angle_map},
                node_color='w',
                node_size=1000,
                edgecolors='k')
