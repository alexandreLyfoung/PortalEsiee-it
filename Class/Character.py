import pygame.sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/toad.png").convert_alpha()
        self.rect = self.image.get_rect()
