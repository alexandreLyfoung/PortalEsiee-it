import pygame
import pygame.sprite
import os

class Terrain:

    def __init__(self,longeur,largeur,r,g,b):

        self.surface = pygame.display.set_mode((longeur,largeur))
        self.color = (r,g,b)
        self.image_terrain = pygame.image.load('images/terrain.png')
        