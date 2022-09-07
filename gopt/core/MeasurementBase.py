from .Exceptions import BaseException
import numpy as np
from math import pi
from .Plane import Plane

from enum import Enum


class Pauli(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'
    INVALID = None


class MeasurementBase:
    """
    Measurement base
    """

    def __init__(self, angle: float = 0, plane: Plane = Plane.XY, precision_digit: int = 8):
        self._precision_digit: int = precision_digit
        self.plane: Plane = plane
        self.angle: float = angle

    def rotate(self, angle: float, base: str) -> None:
        """
        Rotate the state on bloch sphere
        angle: rotation angle
        base: rotation base
        """
        if base == 'x':
            self.rotate_x(angle)
        elif base == 'y':
            self.rotate_y(angle)
        elif base == 'z':
            self.rotate_z(angle)
        else:
            raise BaseException("Invalid base")

    def is_pauli(self) -> bool:
        """
        Check if the state is Pauli
        return: true if the state is Pauli
        """
        return np.round(self.angle % pi / 2, self._precision_digit) == 0

    def pauli_base(self) -> Pauli:
        """
        Return the Pauli base
        return: Pauli base
        """
        if self.is_pauli():
            angle_parity = np.round(self.angle / pi / 2) % 2
            if angle_parity:
                return {
                    Plane.XY: Pauli.X,
                    Plane.YZ: Pauli.Y,
                    Plane.ZX: Pauli.Z,
                    Plane.INVALID: Pauli.INVALID
                }[self.plane]
            else:
                return {
                    Plane.XY: Pauli.Y,
                    Plane.YZ: Pauli.Z,
                    Plane.ZX: Pauli.X,
                    Plane.INVALID: Pauli.INVALID
                }[self.plane]
        else:
            return Pauli.INVALID

    def sign(self) -> int:
        """
        """
        return -1 if 1 < np.round(self.angle / pi / 2) < 4 else 1

    def rotate(self, angle: float) -> None:
        """
        Rotate the angle
        """
        self.angle = (self.angle + angle) % (2 * pi)

    def negate(self) -> None:
        """
        Negate the angle
        """
        self.angle = (-self.angle) % (2 * pi)

    def image(self) -> None:
        """
        Image the angle
        """
        self.rotate(-pi / 2)
        self.negate()
        self.rotate(pi / 2)

    def _flip(self, case_rotate, case_image, case_negate):
        """
        Helper function for flipping
        """
        if self.plane == case_rotate:
            self.rotate(pi)
        elif self.plane == case_image:
            self.image()
        elif self.plane == case_negate:
            self.negate()

    def flip_x(self) -> None:
        """
        Flip about the X axis
        """
        self._flip(Plane.YZ, Plane.ZX, Plane.XY)

    def flip_y(self) -> None:
        """
        Flip about the Y axis
        """
        self._flip(Plane.ZX, Plane.XY, Plane.YZ)

    def flip_z(self) -> None:
        """
        Flip about the Z axis
        """
        self._flip(Plane.XY, Plane.YZ, Plane.ZX)

    def _rotate_sqrt(self, direction, case_rotate, case_image, case_negate):
        """
        Helper function for one-quater rotation
        """
        if self.plane == case_rotate:
            self.rotate(direction * pi / 2)
        elif self.plane == case_image:
            self.image()
        elif self.plane == case_negate:
            self.negate()
            self.rotate(direction * pi / 2)

    def rotate_sqrt_x(self, direction):
        if self.plane == Plane.XY:
            self.rotate(direction * pi / 2)
        elif self.plane == Plane.ZX:
            self.negate()
        elif self.plane == Plane.YZ:
            self.image()

    def rotate_sqrt_y(self, direction):
        if self.plane == Plane.XY:
            self.rotate(pi)
        elif self.plane == Plane.ZX:
            self.negate()
        elif self.plane == Plane.YZ:
            self.image()

    def rotate_sqrt_z(self, direction):
        if self.plane == Plane.XY:
            self.rotate(direction * pi / 2)
        elif self.plane == Plane.ZX:
            self.plane = Plane.YZ
        elif self.plane == Plane.YZ:
            self.image()

    def rotate_h(self):
        self.rotate_sqrt_x(1)
        self.rotate_sqrt_z(1)
        self.rotate_sqrt_x(1)

    def __repr__(self):
        return "Meaurement Plane {} with angle {}".format(self.plane, self.angle)
