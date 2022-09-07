from math import pi, sin, cos
from typing import Dict, List, Set


def rotate_coordinates(angle: float, rx: float, ry: float):
    return cos(angle) * rx - sin(angle) * ry, \
           sin(angle) * rx + cos(angle) * ry


def is_pauli_angle(angle: float):
    return angle % (pi / 2) == 0


def process_outcomes(outome_counts: Dict[str, int],
                     creg_map: Dict[any, int],
                     outputs: List[any]):
    output_reg = [creg_map[node] for node in outputs]
    processed_counts: Dict[str, int] = dict()
    for word, count in outome_counts.items():
        masked_word = ''
        for reg_id in output_reg:
            masked_word += word[::-1][reg_id]
        if masked_word in processed_counts:
            processed_counts[masked_word] += count
        else:
            processed_counts[masked_word] = count
    return processed_counts


def dependency_map(dependency_graph) -> Dict[any, Set[any]]:
    """
    Obtain the measurement dependencies.
    :return: a mapping from a node to the nodes whose measurement outcomes affect the measurement basis
    """
    dep_map: Dict[any, Set[any]] = dict()
    for source, target in dependency_graph.edges():
        if target not in dep_map:
            dep_map[target] = set()
        dep_map[target].add(source)
    return dep_map
