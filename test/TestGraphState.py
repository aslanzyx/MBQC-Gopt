import unittest
from graphoptim.core import ClusterState


class TestGraphState(unittest.TestCase):

    def setUp(self) -> None:
        c = ClusterState(2)
        c.t(0)
        c.t(1)
        c.cnot(0, 1)
        g = c.to_graph_state()
