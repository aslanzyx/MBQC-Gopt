from gopt.Utils import rotate_coordinates
from .Exceptions import BaseException
import numpy as np


class BlochSphere:
    """
    Bloch sphere object
    """

    def __init__(self, base: str = 'z', precision_digit=8):
        self._precision_digit = precision_digit
        if base == 'x':
            self.vector: np.ndarray = np.array([1., 0, 0])
        elif base == 'y':
            self.vector: np.ndarray = np.array([0, 1., 0])
        elif base == 'z':
            self.vector: np.ndarray = np.array([0, 0, 1.])
        else:
            print("not acceptable")

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
        return np.round(np.abs(np.sum(self.vector)),
                        self._precision_digit) == 1

    def plane(self) -> str:
        """
        Get the measurement plane
        return: the measurement plane
        """
        if np.round(self.vector[2], self._precision_digit) == 0:
            return "xy"
        elif np.round(self.vector[0], self._precision_digit) == 0:
            return "zy"
        elif np.round(self.vector[1], self._precision_digit) == 0:
            return "xz"
        else:
            return None

    def plane_angle(self) -> float:
        """
        Get the measurement angle
        return: measurement angle
        """
        plane = self.plane()
        if plane == "xz":
            return np.angle(self.vector[0] + self.vector[2] * 1j)
        elif plane == "zy":
            return np.angle(self.vector[2] + self.vector[1] * 1j)
        elif plane == "xy":
            return np.angle(self.vector[0] + self.vector[1] * 1j)
        else:
            return None

    def angle(self, plane: str = 'xy'):
        """
        Get the measurement angle with specified measurement plane
        plane: measurement plane
        return: measurement angle
        """
        ax0, ax1 = plane[0], plane[1]
        ax0 = self.resolve_index(ax0)
        ax1 = self.resolve_index(ax1)
        return np.angle(self.vector[ax0] + self.vector[ax1] * 1j)

    def resolve_index(self, ax: str):
        if ax == 'x':
            return 0
        elif ax == 'y':
            return 1
        elif ax == 'z':
            return 2
        else:
            return None

    def pauli_base(self):
        if abs(self.vector[0]) == 1:
            return "x"
        elif abs(self.vector[1]) == 1:
            return "y"
        elif abs(self.vector[2]) == 1:
            return "z"
        else:
            return None

    def pauli_sign(self):
        base = self.pauli_base()
        if base == 'x':
            return int(np.sign(self.vector[0]))
        elif base == 'y':
            return int(np.sign(self.vector[1]))
        elif base == 'z':
            return int(np.sign(self.vector[2]))

    def rotate_x(self, angle) -> None:
        self.vector[1], self.vector[2] = \
            rotate_coordinates(angle, self.vector[1], self.vector[2])

    def rotate_y(self, angle) -> None:
        self.vector[2], self.vector[0] = \
            rotate_coordinates(angle, self.vector[2], self.vector[0])

    def rotate_z(self, angle) -> None:
        self.vector[0], self.vector[1] = \
            rotate_coordinates(angle, self.vector[0], self.vector[1])

    def flip_x(self) -> None:
        self.vector[1], self.vector[2] = -self.vector[1], -self.vector[2]

    def flip_y(self) -> None:
        self.vector[2], self.vector[0] = -self.vector[2], -self.vector[0]

    def flip_z(self) -> None:
        self.vector[0], self.vector[1] = -self.vector[0], -self.vector[1]

    def rotate_sqrt_x(self, direction):
        self.vector[1], self.vector[2] = -direction * \
            self.vector[2], direction * self.vector[1]

    def rotate_sqrt_y(self, direction):
        self.vector[2], self.vector[0] = -direction * \
            self.vector[0], direction * self.vector[2]

    def rotate_sqrt_z(self, direction):
        self.vector[0], self.vector[1] = -direction * \
            self.vector[1], direction * self.vector[0]

    def rotate_h(self):
        self.rotate_sqrt_x(1)
        self.rotate_sqrt_z(1)
        self.rotate_sqrt_x(1)

    def __repr__(self):
        return "Bloch sphere object with vector {}".format(self.vector)
