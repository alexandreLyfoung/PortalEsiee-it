import pygame
import pygame.locals
import sys
from Class import Character
from Class import Portail
# Initialisation de Pygame

pygame.init()
screen_size = (800, 600)
pygame.display.set_caption("Portal")
window_game = pygame.display.set_mode(screen_size, pygame.locals.RESIZABLE)
#icon_game = pygame.image.load()
#pygame.display.set_icon(icon_game)

character = Character.Player()
character_position = character.rect
character_position.update(0, 0, 25, 25)

portal1 = Portail.Portail()
portal1.set_x(200)
portal1.set_y(200)
portal1.set_id_portail(0)

portal2 = Portail.Portail()
portal2.set_x(100)
portal2.set_y(300)
portal2.set_id_portail(0)

# Boucle principale du jeu
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        character.set_y(-character.get_speed())
    # if keys[pygame.K_s]:
    #    player_pos.y += 300 * dt
    if keys[pygame.K_q]:
        character.set_x(-character.get_speed())
    if keys[pygame.K_d]:
        character.set_x(character.get_speed())

    if ((portal1.rect.colliderect(character.rect) or portal2.rect.colliderect(character.rect))):
        print("collision")

    window_game.fill((255, 255, 255))
    character_position.update(character.get_x(), character.get_y(), 0, 0)
    window_game.blit(character.image, character_position)
    window_game.blit(portal1.get_image(),portal1.get_rect())
    window_game.blit(portal2.get_image(),portal2.get_rect())
    pygame.display.flip()
