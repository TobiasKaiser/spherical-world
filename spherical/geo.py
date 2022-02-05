import quaternion
import numpy as np

class Color:
    Blue = np.array([0.0,0.0,1.0]) # blue = 1i
    Green = np.array([0.0,1.0,0.0]) # green = 1j
    Red = np.array([1.0,0.0,0.0]) # red = 1k
    Yellow = np.array([1.0,1.0,0.0]) # yellow = ij
    Magenta = np.array([1.0,0.0,1.0]) # pink = ik
    Cyan = np.array([0.0,1.0,1.0]) # cyan = jk
    White = np.array([1.0,1.0,1.0])
    LightGray = np.array([0.6,0.6,0.6])
    DarkGray = np.array([0.4,0.4,0.4])
    Black = np.array([0.0,0.0,0.0])

unit = np.quaternion(1, 0, 0, 0)
i = np.quaternion(0, 1, 0, 0)
j = np.quaternion(0, 0, 1, 0)
k = np.quaternion(0, 0, 0, 1)


def slerp(start, end, ratio):
    start_inv = 1.0/start
    return start*((start_inv*end)**ratio)

def circle(subdivisions=128, base1=i, base2=j):
    angles = np.linspace(0, 2*np.pi, subdivisions+1)

    line_segments=[]
    for idx in range(len(angles)-1):
        line_segments+=[angles[idx], angles[idx+1]]
    line_segments = np.array(line_segments)

    pos = np.sin(line_segments)*base1 + np.cos(line_segments)*base2
    return np.array(quaternion.as_float_array(pos), dtype='f4')

def uniform_color_array(size, color=Color.White):
    data = np.full(shape=(size,3), fill_value=color)
    return np.array(data, dtype='f4')

class AxisSet:
    def __init__(self, subdivisions=128):
        self.subdivisions=subdivisions
        self.col_array_list = []
        self.pos_array_list = []

    def add_axis(self, color, base1, base2):
        self.pos_array_list.append(
            circle(self.subdivisions, base1, base2))
        self.col_array_list.append(
            uniform_color_array(self.subdivisions*2, color))

    def add_all_axes(self):
        self.add_axis(Color.Red, unit, i)
        self.add_axis(Color.Green, unit, j)
        self.add_axis(Color.Blue, unit, k)
        self.add_axis(Color.Yellow, i, j)
        self.add_axis(Color.Magenta, i, k)
        self.add_axis(Color.Cyan, j, k)

    def col_array(self):
        return np.array(np.concatenate(self.col_array_list), dtype='f4')

    def pos_array(self):
        return np.array(np.concatenate(self.pos_array_list), dtype='f4')


class QuaternionPair:
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
        self.s = self.s * a
        self.t = b * self.t

    def q1(self):
        return 1/self.s

    def q2(self):
        return 1/self.t

    def transform(self, point):
        return self.q1()*point*self.q2()
    

    def rotate(self, alpha=np.pi/2, axis=k):
        e = alpha/np.pi
        self.apply_inner(axis**e, (-axis)**e)


    def translate(self, alpha=np.pi/2, axis=k):
        e = alpha/np.pi
        self.apply_inner(axis**e, axis**e)



class Sphere:
    """Sphere tiled as octahedron with subdivided faces."""
    def color(self, odd):
        return self.color_odd if odd else self.color_even

    def __init__(self, center=QuaternionPair(), radius=np.pi, subdivisions=0, color_even=Color.DarkGray, color_odd=Color.LightGray):
        self.col_array_list = []
        self.pos_array_list = []
        self.subdivisions=subdivisions
        
        self.center = center
        self.radius = radius

        self.color_even = color_even
        self.color_odd = color_odd

        self.add_all_faces()

    def add_all_faces(self):
        e = self.radius/np.pi
        c =self.center

        right  = c.transform((+i)**e)
        left   = c.transform((-i)**e)
        top    = c.transform((+j)**e)
        bottom = c.transform((-j)**e)
        front  = c.transform((+k)**e)
        back   = c.transform((-k)**e)
        
        self.add_tiled_triangle(right, top, front, False, self.subdivisions)
        self.add_tiled_triangle(right, top, back, True, self.subdivisions)
        self.add_tiled_triangle(right, bottom, front, True, self.subdivisions)
        self.add_tiled_triangle(left, top, front, True, self.subdivisions)
        self.add_tiled_triangle(right, bottom, back, False, self.subdivisions)
        self.add_tiled_triangle(left, top, back, False, self.subdivisions)
        self.add_tiled_triangle(left, bottom, front, False, self.subdivisions)
        self.add_tiled_triangle(left, bottom, back, True, self.subdivisions)

    def add_tiled_triangle(self, p1, p2, p3, odd, subdiv):
        if subdiv == 0:
            self.add_triangle(p1, p2, p3, odd)
        else:
            mid12 = slerp(p1, p2, 0.5)
            mid13 = slerp(p1, p3, 0.5)
            mid23 = slerp(p2, p3, 0.5)
            self.add_tiled_triangle(p1, mid12, mid13, odd, subdiv-1)
            self.add_tiled_triangle(p2, mid23, mid12, odd, subdiv-1)
            self.add_tiled_triangle(p3, mid13, mid23, odd, subdiv-1)
            self.add_tiled_triangle(mid12, mid23, mid13, not odd, subdiv-1)

    def add_triangle(self, a, b, c, odd):
        pos = np.array([
            a,
            b,
            c
        ])

        self.pos_array_list.append(
            np.array(quaternion.as_float_array(pos), dtype='f4'))
        self.col_array_list.append(
            uniform_color_array(3, self.color(odd)))

    def col_array(self):
        return np.array(np.concatenate(self.col_array_list), dtype='f4')

    def pos_array(self):
        return np.array(np.concatenate(self.pos_array_list), dtype='f4')

