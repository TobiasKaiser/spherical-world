import quaternion
import numpy as np

unit = np.quaternion(1, 0, 0, 0)
i = np.quaternion(0, 1, 0, 0)
j = np.quaternion(0, 0, 1, 0)
k = np.quaternion(0, 0, 0, 1)


def slerp(start, end, ratio):
    start_inv = 1.0/start
    return start*((start_inv*end)**ratio)

class SphericalTransform:
    """
    Represents translation and rotation from the sphere origin at 1 through a
    pair of quaternions. In order to apply the transformation, quaternion s
    needs to be multiplied from the left, quaternion t from the right.
    """
    def __init__(self):
        self.s = unit
        self.t = unit

    def yaw(self, alpha):
        self.rotate(alpha, j)

    def pitch(self, alpha):
        self.rotate(alpha, i)

    def roll(self, alpha):
        self.rotate(alpha, k)

    def apply_inner(self, a, b):
        self.s = a * self.s
        self.t = self.t * b

    def transform(self, point):
        return self.s*point*self.t    

    def rotate(self, alpha=np.pi/2, axis=k):
        e = alpha/np.pi
        self.apply_inner(axis**-e, (-axis)**-e)

    def translate(self, alpha=np.pi/2, axis=k):
        e = alpha/np.pi
        self.apply_inner(axis**-e, axis**-e)