import pygame
import pygame.sprite
import os, csv
import main2
from os.path import join
from Class import Tile
#from Class import Portail

#Classe permettant la creation de la tilesmaps
class Terrain():

    def __init__(self,filepath):

        self.tile_size = 16   #taille des tuiles 16x16
        self.start_x, self.start_y = 0, 0   #coordonne d'initilisation du joueur sur la map
        self.tiles,self.portals = self.load_tiles(filepath) #chargement de la map

    #lecture de la couche du niveau de la tilemaps depuis un fichier csv contenant les donnees de la map et
    # traduire dans un tableau de valeurs contenant les ID's des sprites du spritesheet
    # (creation de niveau a l'aide du logiciel Tiles)
    def read_csv(self, filepath):

        map = []

        with open(os.path.join(filepath)) as data:
            data = csv.reader(data, delimiter = ",")

            for row in data:
                map.append(list(row))

        return map

    #affichage des elements de la layer de la map
    def draw_map(self, surface,offset_x,offset_y):

        for tile in self.tiles:
            tile.draw(surface,offset_x,offset_y)

    #separation des textures de la map depuis un spritesheet contenant des tuiles 16x16
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

    #Creation de la map pour le jeu et en associant les textures a leur ID's respectifs du csv
    def load_tiles(self,filepathcsv):

        all_sprites = self.split_sprite_sheet("spritesheet.png", self.tile_size, self.tile_size)
        portal1 = self.split_sprite_sheet("portal1.png",16,32)
        portal2 = self.split_sprite_sheet("portal2.png",16,32)
        surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA, 32)

        tiles = []
        portals = []
        layer_map = self.read_csv(filepathcsv)
        x,y = 0,0
        id_portal = 0

        #Creation de la map ligne par ligne
        for row in layer_map:

            x = 0
            for tile in row:

                #Si detection de tile ID 3 (non utilise dans les objets ou elements du jeu) alors association coordonnee
                #de ce tile sur la map a celui de la position initiale du joueur au lancement de la map
                if tile == '3':
                    self.start_x, self.start_y = x * self.tile_size, main2.HEIGHT//2 + y * self.tile_size
                #sinon creation des autres elements du jeu en associant texture, dimension et coordonnee
                else:
                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    surface.blit(all_sprites[int(tile)], (0, 0), rect)
                    tiles.append(Tile.Tile(all_sprites[int(tile)], x * self.tile_size,main2.HEIGHT//2
                                           + y * self.tile_size,16))

                """elif tile == '0':
                    rect = pygame.Rect(x * 16, y * 32, 16, 32)
                    surface.blit(portal1[0], (0, 0), rect)
                    portals.append(Portail.Portail(portal1[0], x * 16, y * 16,id_portal))
                elif tile == '1':
                    rect = pygame.Rect(x * 16, y * 32, 16, 32)
                    surface.blit(portal2[0], (0, 0), rect)
                    portals.append(Portail.Portail(portal2[0], x * 16, y * 16,id_portal))
                    id_portal+=1"""

                x += 1

            y += 1

        return tiles,portals


