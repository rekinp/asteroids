import pygame
import random
from pygame.key import ScancodeWrapper
from typing import List, Tuple

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from settings import ScreenSize, ImageAsset
from bullet import Bullet


class Game:
    NUMBER_OF_ASTEROIDS = 10
    LOG = True

    def __init__(self):
        pygame.init()

        # clock
        self.clock = pygame.time.Clock()
        self.fps = 30

        # game controls
        self.game_over = False
        self.pause_game = False

        # game objects
        self.screen = Screen(screen_width=ScreenSize.WIDTH.value, screen_height=ScreenSize.HEIGHT.value)
        self.ship = Ship(pos=(400, 400))
        safe_distance = 200
        self.ship_start_rect = pygame.Rect(self.ship.pos[0] - safe_distance / 2, self.ship.pos[1] - safe_distance / 2,
                                           safe_distance, safe_distance)
        self.asteroids: List[Asteroid] = []
        self.asteroids_that_were_hit: List[Asteroid] = []
        self.bullets_that_hit_asteroids: List[Bullet] = []
        for i in range(self.NUMBER_OF_ASTEROIDS):
            # self.asteroids.append(Asteroid(size=1, pos=(64, 64), screen=self.screen))
            asteroid = Asteroid(size=random.randint(1, 3),
                                pos=(random.randint(0, self.screen.screen_width),
                                     random.randint(0, self.screen.screen_width)),
                                screen=self.screen)
            while asteroid.rect.colliderect(self.ship_start_rect) or len(
                    asteroid.collides_with_asteroids(self.asteroids)) > 0:
                asteroid = Asteroid(size=random.randint(1, 3),
                                    pos=(random.randint(0, self.screen.screen_width),
                                         random.randint(0, self.screen.screen_width)),
                                    screen=self.screen)
            self.asteroids.append(asteroid)

    def destroy_asteroid(self, asteroid: Asteroid):
        self.asteroids.remove(asteroid)

    def destroy_asteroids(self, asteroids: List[Asteroid]):
        for asteroid in asteroids:
            self.destroy_asteroid(asteroid)

    def run(self):
        while not self.game_over:
            self.handle_events()
            if not self.pause_game:
                self.update()
                self.render()
                self.clock.tick(self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_game = not (self.pause_game)
        if not (self.pause_game) and not (self.ship is None):
            key_pressed: ScancodeWrapper = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP] or key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] or key_pressed[
                pygame.K_RIGHT] or key_pressed[pygame.K_SPACE]:
                self.ship.handle_event(key_pressed)
            self.ship.shooting_cooldown_reduction(self.clock.get_time())
            # logging
            if key_pressed[pygame.K_l]:
                print(f"ship_pos: {self.ship.pos}\n"
                      f"ship_rect: {self.ship.rect}\n"
                      f"ship_hitbox: {self.ship.hitbox}\n"
                      f"asteroid_pos: {self.asteroids[0].pos}\n"
                      f"asteroid_rect: {self.asteroids[0].rect}\n"
                      f"asteroid_hitbox: {self.asteroids[0].hitbox}")

    def update(self):
        if self.ship is not None:
            # bullets
            for bullet in self.ship.bullets:
                if bullet.is_outside_screen(self.screen):
                    self.ship.remove_bullet(bullet)
                bullet.update()

            # asteroid-bullet
            self.detect_asteroid_bullet_collisions()
            for asteroid in self.asteroids_that_were_hit:
                self.destroy_asteroid(asteroid)
                asteroid.sound_explode.play()
            for bullet in self.bullets_that_hit_asteroids:
                self.ship.remove_bullet(bullet)

            # asteroids
            for asteroid in self.asteroids:
                asteroid.update(self.screen)

            # ship
            self.ship.update(self.screen)
            for asteroid in self.asteroids:
                if self.ship.collides_with_asteroid(asteroid):
                    self.ship.sound_explosion.play()
                    self.ship_last_position = self.ship.pos
                    self.ship = None
                    break

    def detect_asteroid_bullet_collisions(self):
        asteroids = []
        bullets = []
        asteroids_hit = 0
        for b in self.ship.bullets:
            asteroids_hit_by_bullet = self.find_asteroids_hit_by_bullet(b)
            if asteroids_hit_by_bullet:
                asteroids.extend(asteroids_hit_by_bullet)
            if len(asteroids) > asteroids_hit:
                bullets.append(b)
                asteroids_hit += len(asteroids_hit_by_bullet)
        self.asteroids_that_were_hit = asteroids
        self.bullets_that_hit_asteroids = bullets

    def find_asteroids_hit_by_bullet(self, bullet: Bullet):
        asteroids = []
        for asteroid in self.asteroids:
            if asteroid.hitbox.colliderect(bullet.rect):
                asteroids.append(asteroid)
        return asteroids

    def find_bullets_hitting_asteroid(self, asteroid: Asteroid):
        bullets = []
        for bullet in self.ship.bullets:
            if asteroid.hitbox.colliderect(bullet.rect):
                bullets.append(bullet)
        return bullets

    def render_exploded_object(self, pos):
        img = pygame.image.load(ImageAsset.explosion.value)
        self.screen.blit(img, img.get_rect(center=pos))

    def render(self):
        self.screen.render()
        if self.ship is not None:
            self.ship.render(self.screen)
            for bullet in self.ship.bullets:
                bullet.render(self.screen.get_surface())
        else:
            self.render_exploded_object(self.ship_last_position)
        for asteroid in self.asteroids:
            asteroid.render(self.screen)
        for asteroid in self.asteroids_that_were_hit:
            self.render_exploded_object(pos=asteroid.pos)
        self.screen.update()

    def cleanup(self):
        pygame.quit()
