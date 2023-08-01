import pygame
from pygame import Vector2
from bullet import Bullet
from typing import List

class Ship():
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
        self.image = pygame.image.load("resources/images/ship.png")
        self.rotated_image = self.image
        self.rect = self.image.get_rect(topleft=self.pos)

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

    def update(self, screen):
        self.pos += self.drift
        self.pos = screen.wrap_position(pos=self.pos)


    def shooting_cooldown_reduction(self, time):
        if self.can_shoot > 0:
            self.can_shoot -= time
        else:
            self.can_shoot = 0

    def cooldown_shooting(self):
        self.can_shoot = self.SHOOTING_COOLDOWN

    def move_forward(self):
        self.pos += self.forward
        self.drift = (self.drift + self.forward)*0.6

    def move_backward(self):
        self.pos -= self.forward

    def turn_left(self):
        self.forward = self.forward.rotate(-1*self.ROTATION_SPEED)
        self.set_angle()
        self.set_rotated_image()

    def turn_right(self):
        self.forward = self.forward.rotate(1*self.ROTATION_SPEED)
        self.set_angle()
        self.set_rotated_image()

    def shoot(self):
        bullet = Bullet(pos=Vector2(self.pos), velocity=self.forward * 5)
        self.cooldown_shooting()
        self.bullets.append(bullet)

    def remove_bullet(self, bullet: Bullet):
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