from settings import *
import pygame

class Canvas:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w = canvas_size[0]
        self.h = canvas_size[1]
        self.canvas = pygame.Surface(canvas_size)
        self.canvas.fill('white')

    def draw(self, x=50, y=0):
        self.screen.blit(self.canvas, (x, y))