from settings import *
import pygame
import numpy as np
import cv2

white_np = np.array([255, 255, 255], dtype=np.uint8)
black_np = np.array([0, 0, 0], dtype=np.uint8)

class Canvas:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w = canvas_size[0]
        self.h = canvas_size[1]
        self.canvas_np = np.full((self.h, self.w, 3), 255, dtype=np.uint8)
        self.canvas = pygame.surfarray.make_surface(self.canvas_np)

    def draw_line(self, x1, y1, x2, y2):
        cv2.line(self.canvas_np, (y1, x1), (y2, x2), (0, 0, 0))
        self.canvas = pygame.surfarray.make_surface(self.canvas_np)

    def draw_circle(self, x, y, radius):
        cv2.circle(self.canvas_np, (y, x), radius, (255, 255, 255), -1)
        self.canvas = pygame.surfarray.make_surface(self.canvas_np)


    def is_valid(self, x: int, y: int):
        return 0 <= x < self.w and 0 <= y < self.h

#    def get_color(self, x: int, y: int):
#        if not self.is_valid(x, y):
#            return None
#        return tuple(self.canvas_np[y, x])

    def set_color(self, x: int, y: int, color):
        if self.is_valid(x, y):
            self.canvas_np[y, x] = color


    def fill(self, seed_point):
        x, y = seed_point[0], seed_point[1]
#        target_color = (255, 255, 255)
#        replacement_color = (0, 0, 0)

        if not self.is_valid(x, y):
            return

        if self.canvas_np[y, x][0] != 255:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            x1 = x
            while self.is_valid(x1, y) and self.canvas_np[y, x1][0] == 255:
                x1 -= 1
            x1 += 1

            x2 = x
            while self.is_valid(x2, y) and self.canvas_np[y, x2][0] == 255:
                x2 += 1
            x2 -= 1

#            cv2.line(self.canvas_np, (y, x1), (y, x2), (0, 0, 0))
            for i in range(x1, x2 + 1):
                self.set_color(i, y, (0, 0, 0))

            for i in range(x1, x2 + 1):
                if self.is_valid(i, y - 1) and self.canvas_np[y-1, i][0] == 255:
                    stack.append((i, y - 1))
                if self.is_valid(i, y + 1) and self.canvas_np[y+1, i][0] == 255:
                    stack.append((i, y + 1))


    def draw(self, x=50, y=0):
        self.screen.blit(self.canvas, (x, y))