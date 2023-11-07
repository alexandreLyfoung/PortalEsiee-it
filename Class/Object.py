import pygame

#Classe representant les objets du jeu
class Object(pygame.sprite.Sprite):

    def __init__(self,x ,y ,width, height, name=None):

        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    #fonction affichage de l'objet
    def draw(self,win, offset_x,offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))


