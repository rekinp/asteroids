import pygame
from pygame import Vector2

class Asteroid:
    def __init__(self, size, pos):
        self.pos = Vector2(pos)
        self.size = size
        if self.size in [1, 2, 3]:
            self.image = pygame.image.load(f"resources/images/asteroid{self.size}.png")
        else:
            self.image = pygame.image.load(f"resources/images/asteroid1.png")
        self.rect = self.image.get_rect(topleft=self.pos)

    def render(self, screen):
        screen.blit(image=self.image, pos=self.pos)

    def update(self):
        pass

