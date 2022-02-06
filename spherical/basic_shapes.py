from . import geo
import numpy as np
import quaternion

def quaternions_to_vertices(quaternions):
    reorder_to_xyzw=np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ])
    array_wxyz = quaternion.as_float_array(quaternions)
    return np.array(
        np.matmul(array_wxyz, reorder_to_xyzw),
        dtype="f4")

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

def circle(subdivisions=128, base1=geo.i, base2=geo.j):
    angles = np.linspace(0, 2*np.pi, subdivisions+1)

    line_segments=[]
    for idx in range(len(angles)-1):
        line_segments+=[angles[idx], angles[idx+1]]
    line_segments = np.array(line_segments)

    pos = np.sin(line_segments)*base1 + np.cos(line_segments)*base2
    return quaternions_to_vertices(pos)

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
        self.add_axis(Color.Red, geo.unit, geo.i)
        self.add_axis(Color.Green, geo.unit, geo.j)
        self.add_axis(Color.Blue, geo.unit, geo.k)
        self.add_axis(Color.Yellow, geo.i, geo.j)
        self.add_axis(Color.Magenta, geo.i, geo.k)
        self.add_axis(Color.Cyan, geo.j, geo.k)

    def col_array(self):
        return np.array(np.concatenate(self.col_array_list), dtype='f4')

    def pos_array(self):
        return np.array(np.concatenate(self.pos_array_list), dtype='f4')

class Octahedron:
    """Sphere tiled as octahedron with subdivided faces."""
    def color(self, odd):
        return self.color_odd if odd else self.color_even

    def __init__(self, center=geo.SphericalTransform(), radius=np.pi, subdivisions=0, color_even=Color.DarkGray, color_odd=Color.LightGray):
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

        for i_sign in (+1, -1):
            for j_sign in (+1, -1):
                for k_sign in (+1, -1):
                    p1 = c.transform((i_sign*geo.i)**e)
                    p2 = c.transform((j_sign*geo.j)**e)
                    p3 = c.transform((k_sign*geo.k)**e)
                    odd = i_sign*j_sign*k_sign < 0
                    self.add_tiled_triangle(p1, p2, p3, odd, self.subdivisions)

    def add_tiled_triangle(self, p1, p2, p3, odd, subdiv):
        if subdiv == 0:
            self.add_triangle(p1, p2, p3, odd)
        else:
            mid12 = geo.slerp(p1, p2, 0.5)
            mid13 = geo.slerp(p1, p3, 0.5)
            mid23 = geo.slerp(p2, p3, 0.5)
            self.add_tiled_triangle(p1, mid12, mid13, odd, subdiv-1)
            self.add_tiled_triangle(p2, mid23, mid12, odd, subdiv-1)
            self.add_tiled_triangle(p3, mid13, mid23, odd, subdiv-1)
            self.add_tiled_triangle(mid12, mid23, mid13, not odd, subdiv-1)

    def add_triangle(self, a, b, c, odd):
        pos = np.array([a, b, c])
        self.pos_array_list.append(quaternions_to_vertices(pos))
        self.col_array_list.append(uniform_color_array(3, self.color(odd)))

    def col_array(self):
        return np.array(np.concatenate(self.col_array_list), dtype='f4')

    def pos_array(self):
        return np.array(np.concatenate(self.pos_array_list), dtype='f4')

