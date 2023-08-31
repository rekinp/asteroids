import pygame
import random
from pygame.key import ScancodeWrapper
from typing import List, Tuple
from text_box import TextBox

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from collision_controller import CollisionController
from settings import ScreenSize, ImageAsset, SoundAsset
from pygame.mixer import Sound
from bullet import Bullet


class Game:
    NUMBER_OF_ASTEROIDS = 8
    LOG = True

    def __init__(self):
        pygame.init()

        # clock
        self.clock = pygame.time.Clock()
        self.fps = 30

        # sounds
        self.sound_theme = Sound(SoundAsset.theme.value)
        self.sound_theme_duration = 30

        # game controls
        self.game_over = False
        self.pause_game = False

        # game objects
        self.screen = Screen(screen_width=ScreenSize.WIDTH.value, screen_height=ScreenSize.HEIGHT.value)
        self.timer = TextBox(text='23', size=80)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.game_controls = TextBox(text=f"arrows - move;space - shoot;p - pause;r - restart", size=20)
        # ship
        self.ship = Ship(pos=(400, 400))
        safe_distance = 200
        self.ship_start_rect = pygame.Rect(self.ship.pos[0] - safe_distance / 2, self.ship.pos[1] - safe_distance / 2,
                                           safe_distance, safe_distance)
        # asteroids
        self.asteroids: List[Asteroid] = []
        self.asteroids_that_were_hit: List[Asteroid] = []
        self.bullets_that_hit_asteroids: List[Bullet] = []
        self.generate_asteroids()

    def generate_asteroids(self):
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
        if asteroid.size >= 3:
            self.asteroids.remove(asteroid)
        else:
            asteroid.decrease_asteroid_size()
            new_asteroid = Asteroid(size=asteroid.size,
                                    pos=asteroid.pos,
                                    screen=self.screen)
            new_asteroid.set_velocity(asteroid.velocity.rotate(30)*1.3)
            asteroid.set_velocity(asteroid.velocity.rotate(-30)*1.3)
            self.asteroids.append(new_asteroid)

    def destroy_asteroids(self, asteroids: List[Asteroid]):
        for asteroid in asteroids:
            self.destroy_asteroid(asteroid)

    def run(self):
        self.sound_theme.play(0)
        self.sound_theme_start_time = pygame.time.get_ticks()
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
            if event.type == pygame.USEREVENT and self.asteroids and self.ship is not None:
                counter = max(int(self.timer.get_text()) - 1, 0)
                self.timer.set_text(text=str(counter))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_game = not (self.pause_game)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()
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
            self.asteroids_that_were_hit, self.bullets_that_hit_asteroids = CollisionController.detect_asteroid_bullet_collisions(asteroids=self.asteroids,
                                                                                                                                  bullets=self.ship.bullets)
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

    def render_exploded_object(self, pos):
        img = pygame.image.load(ImageAsset.explosion.value)
        self.screen.blit(img, img.get_rect(center=pos))

    def render(self):
        TEXT_SIZE = 80
        timer_position_ratio = (0.85, 0.02)
        game_controls_position_ratio = (0.75, 0.87)
        self.screen.render_background()
        self.timer.render(screen=self.screen, pos=(self.screen.screen_width * timer_position_ratio[0],
                                                   self.screen.screen_height * timer_position_ratio[1]))
        self.game_controls.render_multiline(screen=self.screen, pos=(self.screen.screen_width * game_controls_position_ratio[0],
                                                                     self.screen.screen_height * game_controls_position_ratio[1]))
        for asteroid in self.asteroids:
            asteroid.render(self.screen)
        for asteroid in self.asteroids_that_were_hit:
            self.render_exploded_object(pos=asteroid.pos)
        if self.ship is not None:
            self.ship.render(self.screen)
            for bullet in self.ship.bullets:
                bullet.render(self.screen.get_surface())
        else:
            self.render_exploded_object(self.ship_last_position)
            # render game over text
            game_over_lost = TextBox(text="You lost!", size=TEXT_SIZE)
            game_over_lost.render_multiline_center(screen=self.screen)
        if int(self.timer.get_text()) <= 0:
            # render game over text
            game_over_lost = TextBox(text="You lost!;Time is out", size=TEXT_SIZE)
            game_over_lost.render_multiline_center(screen=self.screen)
            self.pause_game = True
        if not(self.asteroids):
            seconds = self.timer.get_text()
            game_over_win = TextBox(text=f"You won!;Result: {seconds}!", size=TEXT_SIZE)
            game_over_win.render_multiline_center(screen=self.screen)
        self.screen.update()

    def restart(self):
        self.__init__()
        if pygame.mixer.get_busy():
            elapsed_time = pygame.time.get_ticks() - self.sound_theme_start_time
            if elapsed_time > self.sound_theme_duration * 1000:
                pygame.mixer.stop()
                self.sound_theme.play(0)
                self.sound_theme_start_time = pygame.time.get_ticks()


    def cleanup(self):
        pygame.mixer.stop()
        pygame.quit()
