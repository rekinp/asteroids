import random

import pygame
from pygame import Vector2

class Asteroid:
    def __init__(self, size, pos, screen):
        self.pos = Vector2(pos)
        self.size = size
        self.velocity = Vector2(random.randint(-3, 3)+3, random.randint(-3, 3)+3)
        if self.size in [1, 2, 3]:
            self.image = pygame.image.load(f"resources/images/asteroid{self.size}.png")
        else:
            self.image = pygame.image.load(f"resources/images/asteroid1.png")
        self.image.get_size()
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(topleft=self.pos)

    def render(self, screen):
        screen.blit(image=self.image, pos=(self.rect[0], self.rect[1]))

    def update_rect_pos(self):
        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

    def update(self, screen):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.pos = screen.wrap_position(pos=self.pos)
        self.update_rect_pos()

