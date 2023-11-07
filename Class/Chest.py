import pygame
from Class import Tile

class Chest(Tile.Tile):

    def __init__(self, img, x, y, size):
        super().__init__(img,x,y,size)

    def is_collide(self, character):
        return pygame.sprite.collide_rect(self, character)