import pygame
from typing import Tuple
from screen import Screen

class TextBox():
    text: str
    size: int
    def __init__(self, text, size):
        self.text = text
        self.font = pygame.font.Font("resources/fonts/Alien.ttf", size)

    def render(self, screen: Screen, pos):
        screen.blit(self.font.render(self.text, True, (255,255,255)), pos)

    def get_text_width(self):
        return self.font.render(self.text, True, (255,255,255)).get_width()

    def get_text_height(self):
        return self.font.render(self.text, True, (255,255,255)).get_height()

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text