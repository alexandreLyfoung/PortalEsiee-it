import pygame
import pygame.sprite
from Class import Character

class Portail(pygame.sprite.Sprite):

    def __init__(self,imagepath):

        pygame.sprite.Sprite.__init__(self)
        self.__x = 0
        self.__y = 0
        self.__id_portail = -1
        self.__image = pygame.image.load(imagepath).convert_alpha()
        self.rect = self.__image.get_rect()
        self.rect.center = (self.rect.width//2,self.rect.height//2)
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_id_portail(self):
        return self.__id_portail

    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.__image

    def set_x(self,x):
        self.__x = x

    def set_y(self,y):
        self.__y = y

    def set_id_portail(self,id_portail):
        self.__id_portail = id_portail

    def is_collide(self,character):
        return pygame.sprite.collide_rect(self, character)