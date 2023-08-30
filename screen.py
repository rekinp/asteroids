import pygame
from pygame import Vector2
from settings import ImageAsset

class Screen:
    TITLE = "asteroid"
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.background = pygame.image.load(ImageAsset.space.value)
        pygame.display.set_caption(self.TITLE)

    def blit(self, image, pos):
        self.screen.blit(image, pos)

    def render_background(self):
        self.screen.blit(self.background, (0, 0))

    def wrap_position(self, pos):
        return Vector2(pos[0] % self.screen_width, pos[1] % self.screen_height)

    def update(self):
        pygame.display.update()

    def get_height(self):
        return self.screen_height

    def get_width(self):
        return self.screen_width

    def get_size(self):
        return self.screen_width, self.screen_height

    def get_surface(self):
        return self.screen