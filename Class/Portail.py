import pygame
from Class import Object
class Portail(Object):
    def __init__(self,image,x,y,id_portal):

        super().__init__(x,y,16,32)
        self.portal_id = id_portal
        portal = image
        self.image.blit(portal, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def is_collide(self,character):
        return pygame.sprite.collide_rect(self, character)