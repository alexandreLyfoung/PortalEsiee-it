import pygame
import pygame.locals
import sys
import os
import random
import math
from os import listdir
from os.path import isfile,join
from Class import Character
from Class import Terrain
from Class import Block
from Class import Portail

pygame.init()

WIDTH, HEIGHT = 800,600
FPS = 60
PLAYER_SPEED = 3

MOVE_KEY_LEFT = pygame.K_q
MOVE_KEY_RIGHT = pygame.K_d
JUMP_KEY = pygame.K_SPACE
SPRINT_KEY = pygame.K_LSHIFT
#ATTACK_KEY = pygame.K_f

screen_size = (WIDTH, HEIGHT)
pygame.display.set_caption("Portal")
window_game = pygame.display.set_mode(screen_size, pygame.locals.RESIZABLE)


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width,height, direction=False):

    path = join("images",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites = []
        for j in range(sprite_sheet.get_width() // width):

            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect = pygame.Rect(j * width, 0, width, height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(surface)

        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_background(name):

    img = pygame.image.load(join("images","backgrounds",name))
    _,_,width,height = img.get_rect()
    tiles = []

    for x in range(WIDTH // width +1):
        for y in range(HEIGHT // height +1):

            pos = (x * width, y * height)
            tiles.append(pos)

    return tiles,img

def get_block(size):

    path = join("images","terrains","sheet1.png")
    img = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(176,104,size,size)
    surface.blit(img, (0,0),rect)

    return pygame.transform.scale2x(surface)

def draw(window,background,bg_img,player, objects, offset_x,maps):

    for tile in background:
        window.blit(bg_img,tuple(tile))

    for obj in objects:
        obj.draw(window_game,offset_x)

    #for elem in maps:)
    #    elem.draw_map(window_game)

    player.draw(window,offset_x)

    pygame.display.update()

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

def collide(player, objects, dx):

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


def handle_move(player, objects):

    keys = pygame.key.get_pressed()

    player.x_speed = 0
    collide_left = collide(player,objects, -PLAYER_SPEED * 2)
    collide_right = collide(player, objects, PLAYER_SPEED * 2)

    if keys[MOVE_KEY_LEFT] and not collide_left and keys[SPRINT_KEY]:
        player.move_left(PLAYER_SPEED + 2)

    elif keys[MOVE_KEY_LEFT] and not collide_left:
        player.move_left(PLAYER_SPEED)

    if keys[MOVE_KEY_RIGHT] and not collide_right and keys[SPRINT_KEY]:
        player.move_right(PLAYER_SPEED + 2)

    elif keys[MOVE_KEY_RIGHT] and not collide_right:
        player.move_right(PLAYER_SPEED)

    handle_vertical_collison(player,objects,player.y_speed)

def main(window):

    clk = pygame.time.Clock()
    background, bg_img = get_background("Blue_Sky.png")

    #map_foreground = Terrain.Terrain("./level/level1/level1_ForeGround.csv")
    #map_background = Terrain.Terrain("./level/level1/level1_Background.csv")
    #map_wall = Terrain.Terrain("./level/level1/level1_Wall.csv")
    maps_bg = None
    #maps_bg = [map_foreground] + [map_background]
    #print(maps_bg)

    map = Terrain.Terrain("./level/lvl3.csv")

    player = Character.Character(100,100,50,50)
    player.rect.x = map.start_x
    player.rect.y = map.start_y

    #objects = [*map_wall.tiles,*map_background.tiles,*map_wall.tiles]
    objects = [*map.tiles]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clk.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY and player.jump_count < 1:

                    player.jump()

        player.loop(FPS)
        handle_move(player, objects)
        draw(window_game,background, bg_img,player, objects ,offset_x,maps_bg)

        if (((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_speed > 0)
                or ((player.rect.left - offset_x <= scroll_area_width) and player.x_speed < 0)):

            offset_x += player.x_speed

        if (player.rect.colliderect(map.portals[0].rect)):
            player.rect.x = map.portals[1].rect.x + 5
            player.rect.y = map.portals[1].rect.y

        elif (player.rect.colliderect(map.portals[1].rect)):
            player.rect.x = map.portals[0].rect.x - 5
            player.rect.y = map.portals[0].rect.y

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window_game)
