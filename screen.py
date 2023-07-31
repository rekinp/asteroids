import pygame

class Screen:
    TITLE = "asteroid"
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.background = pygame.image.load("resources/images/space.png")
        pygame.display.set_caption(self.TITLE)

    def blit(self, image, pos):
        self.screen.blit(image, pos)

    def render(self):
        self.screen.blit(self.background, (0, 0))

    def update(self):
        pygame.display.update()

    def get_size(self):
        return self.screen_width, self.screen_height

    def get_surface(self):
        return self.screen