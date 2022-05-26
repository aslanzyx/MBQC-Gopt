from graphoptim.core import ClusterState
import unittest
from math import pi
import numpy as np


class TestClusterState(unittest.TestCase):
    def test_wire(self):
        cluster_state = ClusterState(1)
        cluster_state.add_rotation_sequence(0, [pi / 2, pi / 2])
        self.assertEqual([pi / 2, pi / 2], cluster_state.cluster_stacks[0])
        cluster_state.add_rotation_sequence(0, [pi / 4, 0])
        self.assertEqual([pi / 2, pi / 2, pi / 4, 0], cluster_state.cluster_stacks[0])
        np.testing.assert_array_equal(np.array([1, 0, 0]),
                                      list(cluster_state.corrections[0])[0][0].vector)
        cluster_state.add_rotation_sequence(0, [pi / 2, pi])
        print(cluster_state.corrections)
        print(cluster_state.dependencies)

# # # from MeasurementBase import MeasurementBase
# # # from Node import Node
# # from graphoptim.graph_state.Node import Node
# # from graphoptim.graph_state.MeasurementBase import MeasurementBase
# #
# #
# # def test_is_pauli():
# #     assert not MeasurementBase([1, 1, 1]).is_pauli()
# #     print("pass case: not pauli")
# #     assert MeasurementBase([1, 0, 0]).is_pauli()
# #     print("pass case: indeed pauli")
# #     assert MeasurementBase([-1, 0, 0]).is_pauli()
# #     print("pass case: negative direction")
# #
# #
# # def test_to_pauli_base():
# #     # assert MeasurementBase([1, 1, 1])
# #     pass
# #
# #
# # def test_rotation():
# #     measurement_base = MeasurementBase([1, 1, 1])
# #     measurement_base.rotate_x()
# #     assert measurement_base.vector == [1, -1, -1]
# #     print("pass case: x rotation")
# #     measurement_base.rotate_y()
# #     assert measurement_base.vector == [-1, -1, 1]
# #     print("pass case: y rotation")
# #     measurement_base.rotate_z()
# #     assert measurement_base.vector == [1, 1, 1]
# #     print("pass case: z rotation")
# #
# #     measurement_base.rotate_sqrt_x(1)
# #     assert measurement_base.vector == [1, 1, -1]
# #     print("pass case: positive sqrt x rotation")
# #     measurement_base.rotate_sqrt_x(-1)
# #     assert measurement_base.vector == [1, 1, 1]
# #     print("pass case: negative sqrt x rotation")
# #     measurement_base.rotate_sqrt_y(1)
# #     assert measurement_base.vector == [-1, 1, 1]
# #     print("pass case: positive sqrt y rotation")
# #     measurement_base.rotate_sqrt_y(-1)
# #     assert measurement_base.vector == [1, 1, 1]
# #     print("pass case: negative sqrt y rotation")
# #     measurement_base.rotate_sqrt_z(-1)
# #     assert measurement_base.vector == [-1, 1, 1]
# #     print("pass case: negative sqrt z rotation")
# #     measurement_base.rotate_sqrt_z(1)
# #     assert measurement_base.vector == [1, 1, 1]
# #     print("pass case: positive sqrt z rotation")
# #
# #
# #
# #
# #
# # def stabilizer_generator():
# #     links = [
# #         {1, 2},
# #         {0, 2},
# #         {0, 1}
# #     ]
# #
# #     measurements = [
# #         (1, 0, 0),
# #         (0, 1, 0),
# #         (1, 1, 0),
# #     ]
# #
# #
# #
# #
# # def main():
# #     test_is_pauli()
# #     test_rotation()
# #     test_node()
# #
# #
# # main()
# #
# # # f = open("teleportation.qasm")
# # # a = f.read().splitlines()
# # # f.close()
# # # print(a)
# # #
# # # _b = np.zeros((5, 2))
# # # _b[1, 1] += 4
# # # print(np.sign(_b))
# #
# # # from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
# # #
# # # qr = QuantumRegister(4)
# # # c0 = ClassicalRegister(1)
# # # c1 = ClassicalRegister(1)
# # # qc = QuantumCircuit(qr, c0, c1)
# # #
# # # qc.h([0, 1, 2, 3])
# # # qc.cz(0, 1)
# # # qc.cz(1, 2)
# # # qc.cz(2, 3)
# # # qc.h(0)
# # # qc.measure(0, c0[0])
# # # qc.x(qr[1]).c_if(c0, 1)
# # # qc.h(1)
# # # qc.measure(1, c1[0])
# # # qc.x(qr[2]).c_if(c1, 1)
# # # print(qc.draw())
#
# from graphoptim.graph_state import *
#
#
# def generate_h(name: str):
#     x0 = Node(MeasurementBase([1, 0, 0]))
#     y1 = Node(MeasurementBase([0, 1, 0]))
#     y2 = Node(MeasurementBase([0, 1, 0]))
#     y3 = Node(MeasurementBase([0, 1, 0]))
#     x0.link(y1)
#     y1.link(y2)
#     y2.link(y3)
#     return [x0, y1, y2, y3], [name + token for token in ['X0', 'Y1', 'Y2', 'Y3']]
#
#
# def generate_wire(name):
#     x0 = Node(MeasurementBase([1, 0, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     x0.link(x1)
#     return [x0, x1], [name + token for token in ['X0', 'X1']]
#
#
# def generate_t(name):
#     t0 = Node(MeasurementBase([1, 1, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     t0.link(x1)
#     return [t0, x1], [name + token for token in ['T0', 'X1']]
#
#
# def generate_z(name):
#     x0 = Node(MeasurementBase([-1, 0, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     x0.link(x1)
#     return [x0, x1], [name + token for token in ['-X0', 'X0']]
#
#
# def generate_x(name):
#     x0 = Node(MeasurementBase([1, 0, 0]))
#     x1 = Node(MeasurementBase([-1, 0, 0]))
#     x0.link(x1)
#     return [x0, x1], [name + token for token in ['X0', '-X1']]
#
#
# def generate_s(name):
#     y0 = Node(MeasurementBase([0, 1, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     y0.link(x1)
#     return [y0, x1], [name + token for token in ['Y0', 'X1']]
#
#
# def truncate_rotation(g0, g1):
#     g0[0][-1].link(g1[0][0])
#     return g0[0] + g1[0], g0[1] + g1[1]
#
#
# def truncate_rotation_entanglement(g0, g1, line):
#     g0[0][-1].link(g1[0][line])
#     return g0[0] + g1[0], g0[1] + g1[1]
#
#
# def truncate_entanglement_rotation(g0, g1, line):
#     g0[0][-1 - line].link(g1[0][0])
#     return g0[0] + g1[0], g0[1] + g1[1]
#
#
# def add_to_graph(graph: GraphState, line):
#     n = len(line[0])
#     for i in range(n):
#         print(line[1][i], line[0][i])
#         graph.nodes[line[1][i]] = line[0][i]
#     # return graph
#
#
# def generate_input(name):
#     i0 = Node(MeasurementBase([1, 1, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     i0.link(x1)
#     return [i0, x1], [name + token for token in ["IN", "STEP"]]
#
#
# def generate_cnot(name):
#     x0 = Node(MeasurementBase([-1, 0, 0]))
#     x1 = Node(MeasurementBase([1, 0, 0]))
#     x2 = Node(MeasurementBase([1, 0, 0]))
#     x3 = Node(MeasurementBase([1, 0, 0]))
#     x4 = Node(MeasurementBase([1, 0, 0]))
#     x5 = Node(MeasurementBase([1, 0, 0]))
#     y0 = Node(MeasurementBase([0, 1, 0]))
#     y1 = Node(MeasurementBase([0, 1, 0]))
#     y2 = Node(MeasurementBase([0, 1, 0]))
#     y3 = Node(MeasurementBase([0, 1, 0]))
#     y4 = Node(MeasurementBase([0, 1, 0]))
#     y5 = Node(MeasurementBase([0, 1, 0]))
#     y6 = Node(MeasurementBase([0, 1, 0]))
#     # -xyyyyy
#     #     y
#     #  xxxyxx
#     x0.link(y0)
#     y0.link(y1)
#     y1.link(y2)
#     y2.link(y3)
#     y2.link(y4)
#     y4.link(y5)
#     y3.link(y6)
#     x1.link(x2)
#     x2.link(x3)
#     x3.link(y6)
#     y6.link(x4)
#     x4.link(x5)
#     return [x0, x1, x2, x3, x4, y0, y1, y2, y3, y4, y6, x5, y5], \
#            [name + token for token in ["-X0", "X1", "X2", "X3", "X4", "Y0", "Y1", "Y2", "Y3", "Y4", "Y6", "X5", "Y5"]],
#
#
# output0 = ([Node(MeasurementBase([1, 1, 0]))], ["o0OUT"])
# output1 = ([Node(MeasurementBase([1, 1, 0]))], ["o1OUT"])
# # input1 = Node(MeasurementBase([1, 1, 0]))
# # output0 = Node(MeasurementBase([1, 1, 0]))
# # output1 = Node(MeasurementBase([1, 1, 0]))
# # sqrtx Z = Y sqrtx
#
#
# line0 = truncate_rotation(generate_input("i0"), generate_h("h0"))
# line0 = truncate_rotation(line0, generate_t("t0"))
# line0 = truncate_rotation(line0, generate_z("z0"))
# line0 = truncate_rotation(line0, generate_t("t1"))
# line0 = truncate_rotation(line0, generate_x("x0"))
# line0 = truncate_rotation(line0, output0)
# line1 = truncate_rotation(generate_input("i1"), generate_s("h1"))
# line1 = truncate_rotation(line1, generate_t("t2"))
# line1 = truncate_rotation(line1, generate_s("s0"))
# line1 = truncate_rotation(line1, generate_t("t3"))
# line1 = truncate_rotation(line1, generate_h("h2"))
# line1 = truncate_rotation(line1, generate_h("x1"))
# line1 = truncate_rotation(line1, output1)
# cnot0 = generate_cnot("cnot0")
# # line1[0][-1].
# # line1[-1]
# # total = truncate_entanglement_rotation(line0, cnot0, 0)
# # total = truncate_entanglement_rotation(line1, cnot0, 1)
# # total = truncate_rotation_entanglement(line0, cnot0, 0)
# # total = truncate_rotation_entanglement(line1, cnot1, 0)
#
# graph_state = GraphState()
# # add_to_graph(graph_state, line0)
# # add_to_graph(graph_state, line1)
# # add_to_graph(graph_state, cnot0)
#
# #
# # for node in graph_state.nodes.values():
# #     print(node.meas.vector, [n.meas.vector for n in node.neighbours])
#
# # h00 = Node(MeasurementBase([0, 1, 0]))
# # h01 = Node(MeasurementBase([0, 1, 0]))
# # h02 = Node(MeasurementBase([0, 1, 0]))
# # h10 = Node(MeasurementBase([0, 1, 0]))
# # h11 = Node(MeasurementBase([0, 1, 0]))
# # h12 = Node(MeasurementBase([0, 1, 0]))
# # h20 = Node(MeasurementBase([0, 1, 0]))
# # h21 = Node(MeasurementBase([0, 1, 0]))
# # h22 = Node(MeasurementBase([0, 1, 0]))
# # h30 = Node(MeasurementBase([0, 1, 0]))
# # h31 = Node(MeasurementBase([0, 1, 0]))
# # h32 = Node(MeasurementBase([0, 1, 0]))
# # t0 = Node(MeasurementBase([1, 1, 0]))
# # t1 = Node(MeasurementBase([1, 1, 0]))
# #
# # x0 = Node(MeasurementBase([1, 0, 0]))
# # x1 = Node(MeasurementBase([1, 0, 0]))
# #
# # input0.link(h00)
# # h00.link(h01)
# # h01.link(h02)
# # h02.link(t0)
# # # t0.link(h20)
# # t0.link(x0)
# # x0.link(x1)
# # x1.link(h20)
# # h20.link(h21)
# # h21.link(h22)
# # h22.link(output0)
# #
# # input1.link(h10)
# # h10.link(h11)
# # h11.link(h12)
# # h12.link(t1)
# # t1.link(h30)
# # h30.link(h31)
# # h31.link(h32)
# # h32.link(output1)
#
# # graph_state = GraphState()
#
# # nodes = [input0, input1, h00, h01, h02,
# #          h10, h11, h12, output0, output1]
# #
# # for i in range(10):
# #     graph_state.nodes[i] = nodes[i]
#
# # graph_state.nodes = {
# #     "input 0": input0,
# #     "input 1": input1,
# #     "output 0": output0,
# #     "output 1": output1,
# # }
#
# # "h00": h00,
# # "h01": h01,
# # "h02": h02,
# # "h10": h10,
# # "h11": h11,
# # "h12": h12,
# # "h20": h20,
# # "h21": h21,
# # "h22": h22,
# # "h30": h30,
# # "h31": h31,
# # "h32": h32,
# # "t0": t0,
# # "t1": t1,
# # "x0": x0,
# # "x1": x1
# # }
#
# graph_state.render("before")
# graph_state.eliminate_pauli()
# graph_state.render("after")
