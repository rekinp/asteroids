import random

import pygame
from pygame import Vector2

class Asteroid:
    def __init__(self, size, pos, screen):
        self.pos = Vector2(pos)
        self.size = size
        self.velocity = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        if self.size in [1, 2, 3]:
            self.image = pygame.image.load(f"resources/images/asteroid{self.size}.png")
        else:
            self.image = pygame.image.load(f"resources/images/asteroid1.png")
        self.image.get_size()
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.set_hitbox()

    def set_hitbox(self):
        hitbox_ratio = (0.65+0.08*self.size)
        self.offset = (self.rect[2] * (1 - hitbox_ratio))//2
        self.hitbox = pygame.Rect(self.rect[0] + self.offset, self.rect[1] + self.offset, self.rect[2]*hitbox_ratio, self.rect[3]*hitbox_ratio)

    def update_hitbox_position(self):
        self.hitbox[0] = self.rect[0] + self.offset
        self.hitbox[1] = self.rect[1] + self.offset

    def render(self, screen):
        screen.blit(image=self.image, pos=(self.rect[0], self.rect[1]))
        # pygame.draw.rect(screen.get_surface(), (0, 255, 0), self.rect)
        # pygame.draw.rect(screen.get_surface(), (0, 0, 255), self.hitbox)

    def update_rect_pos(self):
        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

    def update(self, screen):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.pos = screen.wrap_position(pos=self.pos)
        self.update_rect_pos()
        self.update_hitbox_position()

