import pygame
from Class import Object
import main2
class Block(Object.Object):

    def __init__(self,x,y,size):
        super().__init__(x,y,size,size)
        block = main2.get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

