from math import sqrt

import pygame
from pygame import Vector2
from bullet import Bullet
from typing import List
from asteroid import Asteroid
from pygame.mixer import Sound
from settings import SoundAsset, ImageAsset

class Ship():
    DRIFT = True
    ROTATION_SPEED = 3
    SPEED = 2
    STARTING_VECTOR = Vector2(0, -1*SPEED)
    SHOOTING_COOLDOWN = 300
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.forward = self.STARTING_VECTOR
        self.set_angle()
        self.can_shoot = 0
        self.bullets = []
        self.drift = (0, 0)
        self.image = pygame.image.load(ImageAsset.ship.value)
        self.rotated_image = self.image
        # sounds
        self.sound_shoot = Sound(SoundAsset.shoot.value)
        self.sound_shoot.set_volume(0.1)
        self.sound_explosion = Sound(SoundAsset.explosion.value)
        self.sound_explosion.set_volume(0.5)
        self.rect = self.image.get_rect(center=self.pos)
        self.set_hitbox()

    def handle_event(self, key_pressed):
        if key_pressed[pygame.K_UP]:
            self.move_forward()
        if key_pressed[pygame.K_DOWN]:
            self.move_backward()
        if key_pressed[pygame.K_LEFT]:
            self.turn_left()
        if key_pressed[pygame.K_RIGHT]:
            self.turn_right()
        if key_pressed[pygame.K_SPACE] and self.can_shoot == 0:
            self.shoot()

    def set_hitbox(self):
        hitbox_ratio = 0.8
        self.offset = (self.rect[2] * (1 - hitbox_ratio))//2
        self.hitbox = pygame.Rect(self.rect[0], self.rect[1], self.rect[2]*hitbox_ratio, self.rect[3]*hitbox_ratio)

    def update_hitbox_position(self):
        self.hitbox[0] = self.rect[0] + self.offset
        self.hitbox[1] = self.rect[1] + self.offset

    def update(self, screen):
        self.pos += self.drift
        self.pos = screen.wrap_position(pos=self.pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.update_hitbox_position()
        self.set_rotated_image()

    def collides_with_asteroid(self, asteroid: Asteroid):
        return self.hitbox.colliderect(asteroid.hitbox)

    def shooting_cooldown_reduction(self, time):
        if self.can_shoot > 0:
            self.can_shoot -= time
        else:
            self.can_shoot = 0

    def cooldown_shooting(self):
        self.can_shoot = self.SHOOTING_COOLDOWN

    def move_forward(self):
        DRIFTING_FACTOR = 0.6
        self.pos += self.forward
        if self.DRIFT:
            self.drift = (self.drift + self.forward) * DRIFTING_FACTOR

    def move_backward(self):
        self.pos -= self.forward

    def turn_left(self):
        self.forward = self.forward.rotate(-self.ROTATION_SPEED)
        self.set_angle()

    def turn_right(self):
        self.forward = self.forward.rotate(self.ROTATION_SPEED)
        self.set_angle()

    def shoot(self):
        BULLET_SPEED = 5
        bullet = Bullet(pos=Vector2(self.pos), velocity=self.forward * BULLET_SPEED)
        self.sound_shoot.play()
        self.cooldown_shooting()
        self.bullets.append(bullet)

    def remove_bullet(self, bullet: Bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def remove_bullets(self, bullets: List[Bullet]):
        for bullet in bullets:
            self.remove_bullet(bullet)

    def set_angle(self):
        self.angle = self.forward.angle_to(self.STARTING_VECTOR)

    def set_rotated_image(self):
        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)

    def render(self, screen):
        blit_pos = self.pos - Vector2(self.rotated_image.get_size()) // 2
        screen.blit(self.rotated_image, blit_pos)