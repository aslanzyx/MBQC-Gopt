# from typing import List
# import numpy as np
#
#
# def top_order(dag) -> List[int]:
#     '''
#     Return the topological order of given DAG dependencies
#     '''
#     vistied = set()
#     top_order = []
#     def helper(node: int) -> None:
#         for n in node_nexts[node]:
#             if n not in vistied:
#                 helper(n)
#         top_order.append(n)
#         # node_nexts.
#     while len(vistied) < len(node_nexts):
#         helper(node_nexts)
#
#     return NotImplementedError()
#
# def make_schedule(ordered_graph):
#     return NotImplementedError()
#
# class QASMParser:
#
#     cluster = None
#
#     @staticmethod
#     def parse(qasm_file: str):
#         with open(qasm_file, "r") as qasm_text:
#             for line in qasm_text:
#                 QASMParser.parse_instruction(line)
#         return NotImplementedError()
#
#     @staticmethod
#     def parse_instruction(instruction: str):
#         return NotImplementedError()
#
#     @staticmethod
#     def clear_cache():
#         '''
#         clear cluster cache
#         '''
#         return NotImplementedError()
