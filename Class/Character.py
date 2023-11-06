import pygame
from main2 import load_sprite_sheets,SPRINT_KEY
class Character(pygame.sprite.Sprite):

    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("players","Dude_Monster",32,32,True)
    ANIMATION_DELAY = 6
    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_speed = 0
        self.y_speed = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
    def move(self, dx,dy):

        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,speed):

        self.x_speed = -speed

        if self.direction != "left":

            self.direction = "left"
            self.animation_count = 0
    def move_right(self,speed):

        self.x_speed = speed

        if self.direction != "right":

            self.direction = "right"
            self.animation_count = 0

    def landed(self):

        self.fall_count = 0
        self.y_speed = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_speed *= -1

    def jump(self):

        self.y_speed = -self.GRAVITY * 2
        self.animation_count = 0
        self.jump_count += 1

        if self.jump_count == 1:
            self.fall_count = 0

    def loop(self, fps):

        self.y_speed += min(1, (self.fall_count/fps) * self.GRAVITY)
        self.move(self.x_speed,self.y_speed)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):

        sprite_sheet = "Idle"

        if self.y_speed < 0:
            if self.jump_count == 1:
                sprite_sheet = "Jump"

        elif self.y_speed > self.GRAVITY * 2:
            sprite_sheet = "Fall"

        elif self.x_speed != 0 and pygame.key.get_pressed()[SPRINT_KEY]:
            sprite_sheet = "Run"

        elif self.x_speed != 0:
            sprite_sheet = "Walk"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):

        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self,win, offset_x):

        win.blit(self.sprite, (self.rect.x - offset_x,self.rect.y))