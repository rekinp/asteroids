import pygame
import random
from pygame.key import ScancodeWrapper
from pygame import Vector2
from typing import List

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from settings import ScreenSize
from bullet import Bullet

class Game:
    NUMBER_OF_ASTEROIDS = 10
    def __init__(self):
        pygame.init()

        # clock
        self.clock = pygame.time.Clock()
        self.fps = 30

        # game controls
        self.game_over = False

        # game objects
        self.screen = Screen(screen_width=ScreenSize.WIDTH.value, screen_height=ScreenSize.HEIGHT.value)
        self.ship = Ship(pos=(100, 100))
        self.asteroids = []
        for i in range(self.NUMBER_OF_ASTEROIDS):
            self.asteroids.append(Asteroid(size=random.randint(1,3),
                                           pos=(random.randint(0, self.screen.screen_width), random.randint(0, self.screen.screen_width)),
                                           screen=self.screen))

    def destroy_asteroid(self, asteroid: Asteroid):
        self.asteroids.remove(asteroid)

    def destroy_asteroids(self, asteroids: List[Asteroid]):
        for asteroid in asteroids:
            self.destroy_asteroid(asteroid)

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
        key_pressed: ScancodeWrapper = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_SPACE]:
            self.ship.handle_event(key_pressed)
        self.ship.shooting_cooldown_reduction(self.clock.get_time())

    def update(self):
        self.ship.update(self.screen)
        for asteroid in self.asteroids:
            asteroid.update(self.screen)
            bullets_that_hit_asteroid = self.find_bullets_hitting_asteroid(asteroid)
            if len(bullets_that_hit_asteroid) > 0:
                self.ship.remove_bullets(bullets_that_hit_asteroid)
                self.destroy_asteroid(asteroid)
        for bullet in self.ship.bullets:
            if bullet.is_outside_screen(self.screen):
                self.ship.remove_bullet(bullet)
            bullet.update()
            asteroids_that_were_hit = self.find_asteroids_hit_by_bullet(bullet)
            if len(asteroids_that_were_hit) > 0:
                self.destroy_asteroids(asteroids_that_were_hit)
                self.ship.remove_bullet(bullet)

    def find_asteroids_hit_by_bullet(self, bullet:Bullet):
        asteroids = []
        for asteroid in self.asteroids:
            if asteroid.rect.colliderect(bullet.rect):
                asteroids.append(asteroid)
        return asteroids

    def find_bullets_hitting_asteroid(self, asteroid: Asteroid):
        bullets = []
        for bullet in self.ship.bullets:
            if asteroid.rect.colliderect(bullet.rect):
                bullets.append(bullet)
        return bullets

    def render(self):
        self.screen.render()
        self.ship.render(self.screen)
        for bullet in self.ship.bullets:
            bullet.render(self.screen.get_surface())
        for asteroid in self.asteroids:
            asteroid.render(self.screen)
        self.screen.update()

    def cleanup(self):
        pygame.quit()