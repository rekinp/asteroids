import pygame
from pygame import Vector2

class Ship():
    ROTATION_SPEED = 2
    SPEED = 2
    STARTING_VECTOR = Vector2(0, -1*SPEED)
    def __init__(self, pos):
        self.pos = Vector2(pos)
        self.forward = self.STARTING_VECTOR
        self.set_angle()
        self.image = pygame.image.load("resources/images/ship.png")
        self.rotated_image = self.image
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, key_pressed):
        if key_pressed[pygame.K_UP]:
            self.move_forward()
        elif key_pressed[pygame.K_DOWN]:
            self.move_backward()
        elif key_pressed[pygame.K_LEFT]:
            self.turn_left()
        elif key_pressed[pygame.K_RIGHT]:
            self.turn_right()
        elif key_pressed[pygame.K_SPACE]:
            self.shoot()

    def move_forward(self):
        self.pos += self.forward

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
        pass

    def set_angle(self):
        self.angle = self.forward.angle_to(self.STARTING_VECTOR)

    def set_rotated_image(self):
        self.rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)


    def render(self, screen):
        blit_pos = self.pos - Vector2(self.rotated_image.get_size()) // 2
        screen.blit(self.rotated_image, blit_pos)

