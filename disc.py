
import pygame
from constants import DISC_RADIUS, SCREEN

class Disc:
    def draw(color: tuple, center_x: int, center_y: int):
        pygame.draw.circle(
            surface=SCREEN,
            color=color,
            center=(center_x, center_y),
            radius=DISC_RADIUS
        )
