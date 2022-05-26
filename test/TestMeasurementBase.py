# import unittest
# from graphoptim.graph_state.MeasurementBase import MeasurementBase
#
#
# class TestMeasurementBase(unittest.TestCase):
#
#     def test_is_pauli(self):
#         self.assertTrue(not MeasurementBase([1, 1, 1]).is_pauli(),
#                         "not pauli")
#         self.assertTrue(MeasurementBase([1, 0, 0]).is_pauli(),
#                         "indeed pauli")
#         self.assertTrue(MeasurementBase([-1, 0, 0]).is_pauli(),
#                         "negative direction")
#
#     def test_to_pauli(self):
#         self.assertEqual(MeasurementBase([1, 0, 0]).to_pauli(),
#                          ("x", 1), "pauli x")
#         self.assertEqual(MeasurementBase([0, 1, 0]).to_pauli(),
#                          ("y", 1), "pauli y")
#         self.assertEqual(MeasurementBase([0, 0, 1]).to_pauli(),
#                          ("z", 1), "pauli z")
#         self.assertEqual(MeasurementBase([-1, 0, 0]).to_pauli(),
#                          ("x", -1), "negative pauli x")
