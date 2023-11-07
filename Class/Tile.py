import pygame
from Class import Object

#Classe representant les tuiles du jeu
class Tile(Object.Object):

    def __init__(self,img,x,y,size):

        super().__init__(x,y,size,size)
        self.image = img
        self.image.blit(self.image, (0,0))
        self.mask = pygame.mask.from_surface(self.image)