import pygame
import pygame.sprite
import os, csv
import main2
from os.path import isfile,join
from Class import Tile
from Class import Portail
class Terrain():

    def __init__(self,filepath):

        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.tiles,self.portals = self.load_tiles(filepath)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        #self.load_map()
    def read_csv(self, filepath):

        map = []

        with open(os.path.join(filepath)) as data:
            data = csv.reader(data, delimiter = ",")

            for row in data:
                map.append(list(row))

        return map

    def draw_map(self, surface):

        for tile in self.tiles:
            tile.draw(surface,0)

    def load_map(self):

        for tile in self.tiles:
            tile.draw(self.map_surface,0)

    def split_sprite_sheet(self,filename,sprite_width,sprite_height):

        spritesheet = pygame.image.load(join("images","terrains",filename))
        test_width,test_height = spritesheet.get_size()

        if (test_width%32!=0) and (test_height%32!=0):

            rows = spritesheet.get_height() // sprite_height
            columns = spritesheet.get_width() // sprite_width

            spritesheet = pygame.Surface((32 * columns, 32 * rows),
                                                pygame.SRCALPHA)

        sprites = []
        width,height = spritesheet.get_size()
        rows = height // sprite_height
        columns = width // sprite_width

        for row in range(rows):
            row_sprites = []

            for col in range(columns):

                rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
                sprite = pygame.Surface((sprite_width, sprite_height),pygame.SRCALPHA)
                sprite.blit(spritesheet,(0,0),rect)
                row_sprites.append(sprite)

            sprites += row_sprites

        return sprites

    def load_tiles(self,filepathcsv):

        all_sprites = self.split_sprite_sheet("spritesheet.png", self.tile_size, self.tile_size)
        portal1 = self.split_sprite_sheet("portal1.png",16,32)
        portal2 = self.split_sprite_sheet("portal2.png",16,32)
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA, 32)

        tiles = []
        portals = []
        map = self.read_csv(filepathcsv)
        x,y = 0,0
        id_portal = 0

        for row in map:

            x = 0
            for tile in row:

                if tile == '3':
                    self.start_x, self.start_y = x * self.tile_size, main2.HEIGHT//2 + y * self.tile_size
                elif tile == '0':
                    rect = pygame.Rect(x * 16, y * 32, 16, 32)
                    surface.blit(portal1[0], (0, 0), rect)
                    portals.append(Portail.Portail(portal1[0], x * 16, y * 16,id_portal))
                elif tile == '1':
                    rect = pygame.Rect(x * 16, y * 32, 16, 32)
                    surface.blit(portal2[0], (0, 0), rect)
                    portals.append(Portail.Portail(portal2[0], x * 16, y * 16,id_portal))
                    id_portal+=1
                else:
                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    surface.blit(all_sprites[int(tile)], (0, 0), rect)
                    tiles.append(Tile.Tile(all_sprites[int(tile)], x * self.tile_size,main2.HEIGHT//2 + y * self.tile_size,16))

                x += 1

            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

        return tiles,portals


