import pygame
from pygame.key import ScancodeWrapper

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from settings import ScreenSize

class Game:
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
        self.asteroid = Asteroid(size=10, pos=(200, 200))

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
            self.ship.update(key_pressed)


    def update(self):
        pass

    def render(self):
        self.screen.render()
        self.ship.render(self.screen)
        self.asteroid.render(self.screen)
        self.screen.update()

    def cleanup(self):
        pygame.quit()