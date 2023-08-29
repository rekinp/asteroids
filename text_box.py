import pygame
from typing import Tuple
from screen import Screen

class TextBox():
    text: str
    size: int
    TEXT_COLOR = (255, 255, 255)
    def __init__(self, text, size):
        self.text = text
        self.font = pygame.font.Font("resources/fonts/Alien.ttf", size)
        self.size = size

    def render(self, screen: Screen, pos):
        screen.blit(self.font.render(self.text, True, self.TEXT_COLOR), pos)

    def render_multiline(self, screen: Screen, pos):
        lines = self.text.split(";")
        for i, l in enumerate(lines):
            screen.blit(self.font.render(l, True, self.TEXT_COLOR), (pos[0], pos[1] + self.size*i))

    def render_multiline_center(self, screen: Screen):
        lines = self.text.split(";")
        text_start_height = (screen.screen_height - self.font.render(lines[0], True, self.TEXT_COLOR).get_height()*len(lines)) // 2
        for i, l in enumerate(lines):
            text_pos = ((screen.screen_width - self.font.render(l, True, self.TEXT_COLOR).get_width()) // 2,
                        text_start_height + i*self.font.render(lines[0], True, self.TEXT_COLOR).get_height())
            screen.blit(self.font.render(l, True, self.TEXT_COLOR), text_pos)

    def get_text_width(self):
        return self.font.render(self.text, True, (255,255,255)).get_width()

    def get_text_height(self):
        return self.font.render(self.text, True, (255,255,255)).get_height()

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text