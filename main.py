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

portal1 = Portail.Portail("images/portal.png")
portal1.set_x(200)
portal1.set_y(200)
portal1.set_id_portail(0)

portal2 = Portail.Portail("images/portal2.png")
portal2.set_x(200)
portal2.set_y(400)
portal2.set_id_portail(0)


# Boucle principale du jeu
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        #character.set_y(-character.get_speed())
        character.rect.move_ip((0,-5))
    # if keys[pygame.K_s]:
    #    player_pos.y += 300 * dt
    if keys[pygame.K_q]:
        character.rect.move_ip((-5,0))
    if keys[pygame.K_d]:
        character.rect.move_ip((5,0))

    if(character.rect.colliderect(portal1.rect)):
        character.rect.x = portal2.rect.x+100
        character.rect.y = portal2.rect.y

    elif (character.rect.colliderect(portal2.rect)):ss
        character.rect.x = portal1.rect.x+100
        character.rect.y = portal1.rect.y


    portal1.rect.x = 200
    portal1.rect.y = 0
    portal2.rect.y = 400
    portal2.rect.x = 300
    window_game.fill((255, 255, 255))
    window_game.blit(character.image, character_position)
    window_game.blit(portal2.get_image(), portal2.get_rect())
    window_game.blit(portal1.get_image(),portal1.get_rect())

    pygame.display.flip()
