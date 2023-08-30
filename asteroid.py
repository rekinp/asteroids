import random

import pygame
from pygame import Vector2
from pygame.mixer import Sound
from settings import ImageAsset

class Asteroid:
    # the higher number the smaller asteroid
    asteroid_images = {
        1: pygame.image.load(ImageAsset.asteroid1.value),
        2: pygame.image.load(ImageAsset.asteroid2.value),
        3: pygame.image.load(ImageAsset.asteroid3.value)
    }

    def __init__(self, size, pos, screen):
        self.pos = Vector2(pos)
        self.size = size
        # self.velocity = Vector2(0,0)
        x = random.randint(-self.size, self.size)
        y = random.randint(-self.size, self.size)
        while x == 0 and y == 0:
            x = random.randint(-2, 2)
            y = random.randint(-2, 2)
        self.velocity = Vector2(x, y)
        self.image = Asteroid.asteroid_images.get(self.size, Asteroid.asteroid_images[1])
        self.sound_explode = Sound("resources/sounds/explosion.flac")
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.set_hitbox()

    def set_hitbox(self):
        hitbox_ratio = (0.65+0.08*self.size)
        self.offset = (self.rect[2] * (1 - hitbox_ratio))//2
        self.hitbox = pygame.Rect(self.pos[0] + self.offset, self.pos[1] + self.offset, self.rect[2]*hitbox_ratio, self.rect[3]*hitbox_ratio)

    def decrease_asteroid_size(self):
        if self.size < 3:
            self.size += 1
            self.image = pygame.image.load(f"resources/images/asteroid{self.size}.png")
            self.rect = self.image.get_rect(center=self.pos)
            self.set_hitbox()

    def update_hitbox_position(self):
        self.hitbox[0] = self.rect[0] + self.offset
        self.hitbox[1] = self.rect[1] + self.offset

    def collides_with_asteroids(self, asteroids):
        collided_asteroids = []
        for asteroid in asteroids:
            if self.hitbox.colliderect(asteroid.hitbox):
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

    def set_velocity(self, velocity):
        self.velocity = velocity