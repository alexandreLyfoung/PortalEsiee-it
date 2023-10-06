import pygame.sprite
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.__x = 0
        self.__y = 0
        self.__speed = 5
        self.image = pygame.image.load("images/toad.png").convert_alpha()
        self.rect = self.image.get_rect()



    def get_x(self):
        return self.__x
    def set_x(self, x):
        self.__x += x
    def get_y(self):
        return self.__y
    def set_y(self, y):
        self.__y += y
    def get_speed(self):
        return self.__speed
    def set_speed(self, speed):
        self.__speed = speed
    def get_charcter(self):
        return self.__image
    def set_character(self, character):
        self.image = character
    def get_height(self):
        return self.rect.height
    def get_width(self):
        return self.rect.width
    def get_rect(self):
        return self.rect