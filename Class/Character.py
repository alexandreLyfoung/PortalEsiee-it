import pygame.sprite
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.speed = 5
        self.image = pygame.image.load("images/toad.png").convert_alpha()
        self.rect = self.image.get_rect()



    def get_x(self):
        return self.x
    def set_x(self, x):
        self.x = x
    def get_y(self):
        return self.y
    def set_y(self, y):
        self.y = y
    def get_speed(self):
        return self.speed
    def set_speed(self, speed):
        self.speed = speed
    def get_charcter(self):
        return self.image
    def set_character(self, character):
        self.image = character
    def get_height(self):
        return self.rect.height
    def get_width(self):
        return self.rect.width