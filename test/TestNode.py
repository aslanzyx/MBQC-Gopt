# import unittest
# from graphoptim.graph_state import Node, MeasurementBase
#
#
# class TestNode(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.n0 = Node(MeasurementBase([-1, 0, 0]))
#         self.n1 = Node(MeasurementBase([0, 1, 0]))
#         self.n2 = Node(MeasurementBase([1, 0, 0]))
#         self.n3 = Node(MeasurementBase([1, 1, 0]))
#         self.n0.link(self.n1)
#         self.n1.link(self.n2)
#         self.n2.link(self.n3)
#
#     def test_link(self):
#         self.assertEqual({self.n1}, self.n0.neighbours)
#         self.assertEqual({self.n0, self.n2}, self.n1.neighbours)
#         self.assertEqual({self.n1, self.n3}, self.n2.neighbours)
#         self.assertEqual({self.n2}, self.n3.neighbours)
#
#     def test_local_complement(self):
#         self.n1.local_complement()
#         self.assertEqual({self.n1, self.n2}, self.n0.neighbours)
#         self.assertEqual({self.n0, self.n2}, self.n1.neighbours)
#         self.assertEqual({self.n0, self.n1, self.n3}, self.n2.neighbours)
#         self.assertEqual({self.n2}, self.n3.neighbours)
#
#     def test_unlink(self):
#         self.n2.unlink(self.n3)
#         self.assertEqual({self.n1}, self.n0.neighbours)
#         self.assertEqual({self.n0, self.n2}, self.n1.neighbours)
#         self.assertEqual({self.n1}, self.n2.neighbours)
#         self.assertEqual(set(), self.n3.neighbours)
#
#     def test_disconnect(self):
#         self.n1.disconnect()
#         self.assertEqual(set(), self.n0.neighbours)
#         self.assertEqual(set(), self.n1.neighbours)
#         self.assertEqual({self.n3}, self.n2.neighbours)
#         self.assertEqual({self.n2}, self.n3.neighbours)
#
#     def test_x_measure(self):
#         self.n2.x_measure(1)
#         if self.n3.meas.vector == [-1, -1, 0]:
#             self.assertEqual({self.n3}, self.n0.neighbours)
#             self.assertEqual({self.n3}, self.n1.neighbours)
#             self.assertEqual(set(), self.n2.neighbours)
#             self.assertEqual({self.n0, self.n1}, self.n3.neighbours)
#             self.assertEqual([-1, 0, 0], self.n0.meas.vector)
#             self.assertEqual([0, 1, 0], self.n1.meas.vector)
#             self.assertEqual([-1, -1, 0], self.n3.meas.vector)
#         else:
#             self.assertEqual({self.n1}, self.n0.neighbours)
#             self.assertEqual({self.n0, self.n3}, self.n1.neighbours)
#             self.assertEqual(set(), self.n2.neighbours)
#             self.assertEqual({self.n1}, self.n3.neighbours)
#             self.assertEqual([-1, 0, 0], self.n0.meas.vector)
#             self.assertEqual([0, -1, 0], self.n1.meas.vector)
#             self.assertEqual([0, 1, 1], self.n3.meas.vector)
#         self.n0.x_measure(-1)
#         self.assertEqual(set(), self.n0.neighbours)
#         self.assertEqual(set(), self.n1.neighbours)
#         self.assertEqual(set(), self.n2.neighbours)
#         self.assertEqual(set(), self.n3.neighbours)
#         self.assertEqual([0, -1, 0], self.n1.meas.vector)
#         self.assertEqual([0, -1, 1], self.n3.meas.vector)
#
#     def test_y_measure(self):
#         self.n1.y_measure(1)
#         self.assertEqual({self.n2}, self.n0.neighbours)
#         self.assertEqual(set(), self.n1.neighbours)
#         self.assertEqual({self.n0, self.n3}, self.n2.neighbours)
#         self.assertEqual({self.n2}, self.n3.neighbours)
#         self.assertEqual([0, 1, 0], self.n0.meas.vector)
#         self.assertEqual([0, -1, 0], self.n2.meas.vector)
#         self.assertEqual([1, 1, 0], self.n3.meas.vector)
#         self.n2.y_measure(-1)
#         self.assertEqual({self.n3}, self.n0.neighbours)
#         self.assertEqual(set(), self.n1.neighbours)
#         self.assertEqual(set(), self.n2.neighbours)
#         self.assertEqual({self.n0}, self.n3.neighbours)
#         self.assertEqual([-1, 0, 0], self.n0.meas.vector)
#         self.assertEqual([-1, 1, 0], self.n3.meas.vector)
#
#     def test_measure(self):
#         self.n0.measure()
#         self.n1.measure()
#         self.n2.measure()
#         self.assertEqual([0, 1, 1], self.n3.meas.vector)
