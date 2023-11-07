import pygame
import pygame.locals
from os import listdir
from os.path import isfile,join
from Class import Character
from Class import Terrain
#from Class import Portail

#INITIALISATION DE LA PYGAME
pygame.init()

#PARAMETRES DU JEU (IMPLEMENTATION D'UN MENU POSSIBLE)
WIDTH, HEIGHT = 800,600
FPS = 60
PLAYER_SPEED = 3

#CONFIGURATIONS DE TOUCHES (DEPLACEMENT,SAUT,ETC)
MOVE_KEY_LEFT = pygame.K_q
MOVE_KEY_RIGHT = pygame.K_d
JUMP_KEY = pygame.K_SPACE
SPRINT_KEY = pygame.K_LSHIFT
#ATTACK_KEY = pygame.K_f

#CREATION DE LA FENETRE DE JEU
screen_size = (WIDTH, HEIGHT)
pygame.display.set_caption("Portal")
window_game = pygame.display.set_mode(screen_size, pygame.locals.RESIZABLE)

#fonction permettant de flip une image pour les animations de sprites
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

#fonction permettant le chargement des feuilles de sprites pour les textures du jeu pour les animations
def load_sprite_sheets(dir1, dir2, width,height, direction=False):

    path = join("images",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))] # recuperation de tous les images du dossier path

    all_sprites = {} #dictionnaire contenant tous les sprites du dossier pour les animations

    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()


        #recuperation des sprites et realisation des flips de sprites y compris pour le deplacement à gauche
        sprites = []

        for j in range(sprite_sheet.get_width() // width):

            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(j * width, 0, width, height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(surface)

        # si  sprite contient une direction creation de sprites "droite" et "gauche" (inverse) ex: joueur
        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        #tous les autres sprites sans influence de la direction ex:objets
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

#fonction permettant le chargement d'un background de jeu
def get_background(name):

    img = pygame.image.load(join("images","backgrounds",name))
    _,_,width,height = img.get_rect()
    tiles = []

    for x in range(WIDTH // width +1):
        for y in range(HEIGHT // height +1):

            pos = (x * width, y * height)
            tiles.append(pos)

    return tiles,img

#affichage des elements graphique de jeu, background sur la fenetre de jeu
def draw(window,background,bg_img,player, objects,offset_x,offset_y,maps):

    #gestion affichage background
    for tile in background:
        window.blit(bg_img,tuple(tile))

    #gestion affichage des objets
    for obj in objects:
        obj.draw(window_game,offset_x,offset_y)

    for tile in maps.tiles:
        tile.draw(window_game,offset_x,offset_y)

    #gestion affichage du joueur
    player.draw(window,offset_x,offset_y)

    #mise à jour de l'affichage
    pygame.display.update()

#fonction gerant la collision vertical entre le joueurs et les objects
def handle_vertical_collison(player, objects, dy):

    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):

            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)

    return collided_objects

#fonction retournant les objets en collision à l'horizontale
def handle_horizontal_collide(player, objects, dx):

    player.move(dx, 0)
    player.update()
    collide_objects = None

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):

            collide_objects = obj
            break

    player.move(-dx, 0)
    player.update()

    return collide_objects

#fonction gerant le deplacement du joueur selon les touches parametrer
def handle_move(player, objects):

    keys = pygame.key.get_pressed()

    player.x_speed = 0

    #detection de collission horizontal
    collide_left = handle_horizontal_collide(player,objects, -PLAYER_SPEED * 3)
    collide_right = handle_horizontal_collide(player, objects, PLAYER_SPEED * 3)

    #deplacement à gauche avec sprint
    if keys[MOVE_KEY_LEFT] and not collide_left and keys[SPRINT_KEY]:
        player.move_left(PLAYER_SPEED + 2)

    #deplacement à gauche
    elif keys[MOVE_KEY_LEFT] and not collide_left:
        player.move_left(PLAYER_SPEED)

    #deplacement à droite avec sprint
    if keys[MOVE_KEY_RIGHT] and not collide_right and keys[SPRINT_KEY]:
        player.move_right(PLAYER_SPEED + 2)

    #deplacement à droite
    elif keys[MOVE_KEY_RIGHT] and not collide_right:
        player.move_right(PLAYER_SPEED)

    handle_vertical_collison(player,objects,player.y_speed)

def main(window):

    #HORLOGE DU JEU
    clk = pygame.time.Clock()

    #CHARGEMENT DU SPRITE BACKGROUND
    background, bg_img = get_background("Blue_Sky.png")


    #CHARGEMENT DE LA MAP 1

    #map_portals = Terrain.Terrain("./levels/level_test/level_test_portals.csv")
    map_background = Terrain.Terrain("./levels/level_test/level_test_background.csv")
    map_wall = Terrain.Terrain("./levels/level_test/level_test_walls.csv")

    #map = Terrain.Terrain("./level/lvl3.csv")

    #INITIALISATION DU JOUEUR ET PLACEMENT SUR LA MAP LEVEL1 OU LEVEL_TEST
    player = Character.Character(100,100,50,50)
    player.rect.x = map_wall.start_x
    player.rect.y = map_wall.start_y

    #CHARGEMENT DES OBJETS A COLLISIONS
    #objects = [*map_wall.tiles,*map_background.tiles,*map_wall.tiles]
    objects = [*map_wall.tiles]

    #PARAMETRES POUR LA CAMERA JOUEUR
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200

    #LOOP DU JEU
    run = True
    while run:

        #FPS DU JEU
        clk.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

            #DETECTION DE LA REALISATION DU SAUT PAR LE JOUEUR
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY and player.jump_count < 1:
                    player.jump()

        #MISE A JOUR DU JOUEUR
        player.loop(FPS)
        handle_move(player, objects)

        #AFFICHAGE DES ELEMENTS DU JEU
        draw(window_game,background, bg_img,player,objects,offset_x,offset_y,map_background)

        #GESTION DE LA CAMERA DU JOUEUR ET TRACKING DE LA CAMERA SUR LE JOUEUR
        if (((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_speed > 0)
                or ((player.rect.left - offset_x <= scroll_area_width) and player.x_speed < 0)):

            offset_x += player.x_speed

        if (((player.rect.top - offset_y >= HEIGHT - scroll_area_height) and player.y_speed > 0)
                or ((player.rect.bottom - offset_y <= scroll_area_height) and player.y_speed < 0)):

            offset_y += player.y_speed

        """
        if (player.rect.colliderect(map.portals[0].rect)):
            player.rect.x = map.portals[1].rect.x + 5
            player.rect.y = map.portals[1].rect.y

        elif (player.rect.colliderect(map.portals[1].rect)):
            player.rect.x = map.portals[0].rect.x - 5
            player.rect.y = map.portals[0].rect.y
        """

    pygame.quit()
    quit()

#LANCEMENT DU JEU
if __name__ == "__main__":
    main(window_game)
