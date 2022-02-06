import numpy as np
import moderngl
from . import basic_shapes

class Scene:
    def __init__(self, ctx, prog):
        self.ctx = ctx
        self.prog = prog

    def load(self):
        self._load_axes()
        self._load_sphere()
        self._load_sphere2()

    def render(self):
        self.axes_vao.render(moderngl.LINES)
        self.sphere_vao.render(moderngl.TRIANGLES)
        self.sphere2_vao.render(moderngl.TRIANGLES)

    def _load_axes(self):
        axes = basic_shapes.AxisSet()
        axes.add_all_axes()

        circle_pos = self.ctx.buffer(axes.pos_array())
        circle_col = self.ctx.buffer(axes.col_array())

        self.axes_vao = self.ctx.vertex_array(self.prog, [
            (circle_pos, '4f', 'a_position'),
            (circle_col, '3f', 'a_color'),
        ])

    def _load_sphere(self):
        sphere = basic_shapes.Octahedron(radius=np.pi, subdivisions=6)

        sphere_pos = self.ctx.buffer(sphere.pos_array())
        sphere_col = self.ctx.buffer(sphere.col_array())

        self.sphere_vao = self.ctx.vertex_array(self.prog, [
            (sphere_pos, '4f', 'a_position'),
            (sphere_col, '3f', 'a_color'),
        ])        

    def _load_sphere2(self):
        sphere = basic_shapes.Octahedron(radius=np.pi/4, color_odd=basic_shapes.Color.Cyan, color_even=basic_shapes.Color.Red, subdivisions=0)

        sphere_pos = self.ctx.buffer(sphere.pos_array())
        sphere_col = self.ctx.buffer(sphere.col_array())

        self.sphere2_vao = self.ctx.vertex_array(self.prog, [
            (sphere_pos, '4f', 'a_position'),
            (sphere_col, '3f', 'a_color'),
        ])        
