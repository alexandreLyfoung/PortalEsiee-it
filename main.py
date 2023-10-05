import pygame
import sys
# Initialisation de Pygame

pygame.init()
screen_size = (800, 600)
pygame.display.set_caption("Portal")
window_game = pygame.display.set_mode(screen_size)
#icon_game = pygame.image.load()
#pygame.display.set_icon(icon_game)


# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()