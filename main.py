import pygame
import pygame.locals
import sys
from Class import Character
# Initialisation de Pygame

pygame.init()
screen_size = (800, 600)
pygame.display.set_caption("Portal")
window_game = pygame.display.set_mode(screen_size, pygame.locals.RESIZABLE)
#icon_game = pygame.image.load()
#pygame.display.set_icon(icon_game)

character = Character.Player()
character_position = character.rect
character_position.update(0, 251, 0, 0)
window_game.blit(character.image, character_position)
pygame.display.flip()


# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window_game.blit(character.image, character_position)
    pygame.display.flip()
