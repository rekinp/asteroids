import random

import pygame
from pygame import Vector2
from pygame.mixer import Sound
from typing import List

class Asteroid:
    def __init__(self, size, pos, screen):
        self.pos = Vector2(pos)
        self.size = size
        # self.velocity = Vector2(0,0)
        self.velocity = Vector2(random.randint(-1, 1)*2, random.randint(-1, 1)*2)
        if self.size in [1, 2, 3]:
            self.image = pygame.image.load(f"resources/images/asteroid{self.size}.png")
        else:
            self.image = pygame.image.load(f"resources/images/asteroid1.png")
        self.sound_explode = Sound("resources/sounds/explosion.flac")
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.set_hitbox()

    def set_hitbox(self):
        hitbox_ratio = (0.65+0.08*self.size)
        self.offset = (self.rect[2] * (1 - hitbox_ratio))//2
        self.hitbox = pygame.Rect(self.rect[0] + self.offset, self.rect[1] + self.offset, self.rect[2]*hitbox_ratio, self.rect[3]*hitbox_ratio)

    def update_hitbox_position(self):
        self.hitbox[0] = self.rect[0] + self.offset
        self.hitbox[1] = self.rect[1] + self.offset

    def collides_with_asteroids(self, asteroids):
        collided_asteroids = []
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                collided_asteroids.append(asteroid)
        return collided_asteroids

    def render(self, screen):
        screen.blit(image=self.image, pos=(self.rect[0], self.rect[1]))
        # pygame.draw.rect(screen.get_surface(), (0, 255, 0), self.rect)
        # pygame.draw.rect(screen.get_surface(), (0, 0, 255), self.hitbox)

    def update(self, screen):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.update_hitbox_position()

