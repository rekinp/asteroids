from enum import Enum
import pygame


class ScreenSize(Enum):
    WIDTH = 800
    HEIGHT = 800

class SoundAsset(Enum):
    explosion = "resources/sounds/explosion.flac"
    shoot = "resources/sounds/shoot.mp3"
    theme = "resources/sounds/theme.wav"

class ImageAsset(Enum):
    asteroid1 = "resources/images/asteroid1.png"
    asteroid2 = "resources/images/asteroid1.png"
    asteroid3 = "resources/images/asteroid1.png"
    ship = "resources/images/ship.png"
    space = "resources/images/space.png"
    explosion = "resources/images/explosion.png"