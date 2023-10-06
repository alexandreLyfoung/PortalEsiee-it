import pygame.sprite

class Portail(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.collision = False
        self.id_portail = -1
