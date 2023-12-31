import pygame
from pygame import Vector2


class Bullet:
    def __init__(self, pos, velocity):
        self.pos = Vector2(pos)
        self.velocity = velocity
        self.rect = pygame.Rect(self.pos, (5, 5))

    def update(self):
        self.pos += self.velocity
        self.rect = pygame.Rect(self.pos, (5, 5))

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def is_outside_screen(self, screen):
        if self.rect.top < 0 or self.rect.top > screen.get_height() \
                or self.rect.right < 0 or self.rect.left > screen.get_width():
            return True
        else:
            return False
