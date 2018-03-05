import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import glfw


import os


class Display:

    def __init__(self):
        cwd = os.getcwd()

        if not glfw.init():
            return

        os.chdir(cwd)

        glfw.window_hint(glfw.VERSION_MAJOR, 3)
        glfw.window_hint(glfw.VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.width, self.height = 640, 480
        self.window = glfw.create_window(self.width, self.height,
                                         "Simple Window", None, None)

        glfw.make_context_current(self.window)

        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.5, 0.5, 1)

        glfw.set_key_callback(self.window, self._key_press_callback)
        glfw.set_mouse_button_callback(self.window, self._mouse_press_callback)
        glfw.set_window_size_callback(self.window, self._window_resize_callback)

    def _mouse_press_callback(self):
        pass

    def _key_press_callback(self, win, key, scancode, action, mods):
        pass

    def _window_resize_callback(self):
        pass


