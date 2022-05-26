from graphoptim.core import BlochSphere
import unittest
from math import pi
import numpy as np


class TestBlochSphere(unittest.TestCase):
    def test_rotation(self):
        vector_after = np.array([0, -1, 0])
        bloch_sphere = BlochSphere()
        bloch_sphere.rotate_x(pi / 2)
        np.testing.assert_array_equal(vector_after, bloch_sphere.vector)
        # self.assertSequenceEqual(vector_after, bloch_sphere)
