import pygame
import pygame.locals
import sys
import os
import random
import math
from os import listdir
from os.path import isfile,join
from Class import Character
from Class import Block
from Class import Portail

pygame.init()

WIDTH, HEIGHT = 800,600
FPS = 60
PLAYER_SPEED = 5

MOVE_KEY_LEFT = pygame.K_q
MOVE_KEY_RIGHT = pygame.K_d
JUMP_KEY = pygame.K_SPACE

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
            sprites.append(pygame.transform.scale2x(surface))

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

def draw(window,background,bg_img,player, objects):

    for tile in background:
        window.blit(bg_img,tuple(tile))

    for obj in objects:
        obj.draw(window_game)

    player.draw(window)

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

def handle_move(player, objects):

    keys = pygame.key.get_pressed()

    player.x_speed = 0

    if keys[MOVE_KEY_LEFT]:
        player.move_left(PLAYER_SPEED)
    if keys[MOVE_KEY_RIGHT]:
        player.move_right(PLAYER_SPEED)

    handle_vertical_collison(player,objects,player.y_speed)

def main(window):

    clk = pygame.time.Clock()
    background, bg_img = get_background("Blue_Sky.png")

    block_size = 90

    player = Character.Character(100,100,50,50)
    floor = [Block.Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size,WIDTH * 2
                                                                                         // block_size)]
    run = True
    while run:
        clk.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player, floor)
        draw(window_game,background, bg_img,player, floor)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window_game)
