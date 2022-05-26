from typing import Dict

from .BlochSphere import BlochSphere


class MeasurementBaseLayer:
    def __init__(self, angle_map: Dict[any, float]) -> None:
        self.bases: Dict[(int, int), BlochSphere] = dict()
        for label, angle in angle_map.items():
            if angle is None:
                self.bases[label] = BlochSphere()
            else:
                self.bases[label] = BlochSphere('x')
                self.bases[label].rotate_z(-angle)

    def rotate(self, label: (int, int), angle: float, base: str) -> None:
        self.bases[label].rotate(angle, base)

    def flip_z(self, label: (int, int)) -> None:
        self.bases[label].flip_z()

    def rotate_sqrt_x(self, label: (int, int), direction: int):
        self.bases[label].rotate_sqrt_x(direction)

    def rotate_sqrt_z(self, label: (int, int), direction: int):
        self.bases[label].rotate_sqrt_z(direction)

    def cutoff(self, label: (int, int)):
        self.bases.pop(label)

    def pauli_base(self, label):
        base = self.bases[label].pauli_base()
        if base:
            return base
        else:
            return "t"

    def pauli_sign(self, label):
        return self.bases[label].pauli_sign()

    def angle(self, label):
        return self.bases[label].plane_angle()

    def measurement_plane(self, label):
        return self.bases[label].plane()
