import pygame
import moderngl
import pkg_resources
import numpy as np
from . import geo
from .scene import Scene


class Camera:
    def __init__(self, tick_ms, angle_per_second=np.pi/4,distance_per_second=np.pi/10):
        self.qp = geo.SphericalTransform()
        self.input={
            "roll":0.0,
            "yaw":0.0,
            "pitch":0.0,
            "ahead":0.0
        }

        self.angle_per_tick = angle_per_second*tick_ms/1000.0
        self.distance_per_tick = distance_per_second*tick_ms/1000.0

    def tick(self):
        self.qp.yaw      (self.input["yaw"]  *self.angle_per_tick)
        self.qp.pitch    (self.input["pitch"]*self.angle_per_tick)
        self.qp.roll     (self.input["roll"] *self.angle_per_tick)
        self.qp.translate(self.input["ahead"]*self.distance_per_tick)

    def update_input(self, input, direction, reset):
        if self.input[input] == direction:
            if reset:
                self.input[input]=0
        else:
            if not reset:
                self.input[input]=direction

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN:
            reset = False
        elif ev.type == pygame.KEYUP:
            reset = True
        else:
            return

        if ev.key == pygame.K_w:
            self.update_input("pitch",+1,reset)
        elif ev.key == pygame.K_s:
            self.update_input("pitch",-1,reset)
        elif ev.key == pygame.K_a:
            self.update_input("yaw",+1,reset)
        elif ev.key == pygame.K_d:
            self.update_input("yaw",-1,reset)
        elif ev.key == pygame.K_q:
            self.update_input("roll",+1,reset)
        elif ev.key == pygame.K_e:
            self.update_input("roll",-1,reset)
        elif ev.key == pygame.K_UP:
            self.update_input("ahead",+1,reset)
        elif ev.key == pygame.K_DOWN:
            self.update_input("ahead",-1,reset)

def projection_matrix():
    #return np.identity(4)
    #return frustum(-0.0002, 0.0002, -0.0002, 0.0002, -0.0002, -1000.0)
    return frustum(0.0002, -0.0002, 0.0002, -0.0002, 0.0002, 5000.0)

def frustum(left, right, bottom, top, nearVal, farVal):
    """works like glFrustum"""
    A=(right+left)/(right-left)
    B=(top+bottom)/(top-bottom)
    C=-(farVal+nearVal)/(farVal-nearVal)
    D=-(2*farVal*nearVal)/(farVal-nearVal)
    return np.array([
        [2*nearVal/(right-left), 0, -A, 0],
        [0, 2*nearVal/(top-bottom), -B, 0],
        [0, 0, -C, D], # reverse Z??
        [0, 0, 1, 0], # <-- differs from OpenGL standard here: w is not reversed
    ])


class Game:
    def __init__(self):
        self.running = True
        self.last_tick = 0
        self.tick_ms = 10
        self.camera = Camera(self.tick_ms)

    def init_pygame(self):
        pygame.init()
        resolution = (1080, 720)
        pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.OPENGL)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.line_width = 3

        vert_shader_str = pkg_resources.resource_string(__name__, "shaders/demo.vert")
        frag_shader_str = pkg_resources.resource_string(__name__, "shaders/demo.frag")
        self.prog = self.ctx.program(
            vertex_shader=vert_shader_str.decode("utf8"),
            fragment_shader=frag_shader_str.decode("utf8"))

        self.prog["proj"] = tuple(projection_matrix().T.flatten())

        self.scene = Scene(self.ctx, prog)

    def handle_event(self, ev):
        if ev.type == pygame.QUIT:
            self.running=False
        elif ev.type == pygame.KEYDOWN or ev.type == pygame.KEYUP:
            self.camera.handle_event(ev)

    def tick(self):
        self.camera.tick()

    def run(self):
        self.init_pygame()

        while self.running:
            for ev in pygame.event.get():
                self.handle_event(ev)

            now = pygame.time.get_ticks()
            while self.last_tick + self.tick_ms < now:
                self.tick()
                self.last_tick+=self.tick_ms

            self.ctx.clear(0.0, 0.0, 0.0, 0.0)
            
            view_s = self.camera.qp.s
            view_t = self.camera.qp.t
            self.prog["view_s"] = (view_s.x, view_s.y, view_s.z, view_s.w)
            self.prog["view_t"] = (view_t.x, view_t.y, view_t.z, view_t.w)
            self.scene.render()

            pygame.display.flip()

def main():
    g=Game()
    g.run()

