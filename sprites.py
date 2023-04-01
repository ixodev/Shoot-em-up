# Written by Curtis Newton

import pygame as pg, random


class Player:
    def __init__(self, screenrect: pg.Rect) -> None:
        self.screenrect = screenrect
        self.image = pg.image.load("assets/player1.gif")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.screenrect.width / 2 - self.rect.width / 2, self.screenrect.height - self.rect.height * 1.5
        self.speed, self.score = 8, 0

    def handle_inputs(self) -> None:
        key = pg.key.get_pressed()
        if key[pg.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        elif key[pg.K_RIGHT] and self.rect.x <= self.screenrect.width - self.rect.width:
            self.rect.x += self.speed

    def draw_on_screen(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)


class Enemy:
    def __init__(self, screenrect: pg.Rect) -> None:
        self.speed = 15
        self.image = pg.image.load("assets/alien1.png")
        self.rect = self.image.get_rect()
        self.direction, self.screenrect = None, screenrect
        self.choose_randomly_direction()

    def choose_randomly_direction(self) -> None:
        if random.randint(0, 1): self.direction, self.rect.x = "right", 1
        else: self.direction, self.rect.x = "left", self.screenrect.width - 1

    def move(self, direction) -> None:
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        self.check_if_out_of_screen()

    def check_if_out_of_screen(self) -> None:
        if self.rect.x < 0 - self.rect.width:
            self.respawn()
        elif self.rect.x > self.screenrect.width:
            self.respawn()
        if self.rect.y == self.rect.height * 5: self.rect.y = 0

    def respawn(self) -> None:
        self.choose_randomly_direction()
        self.rect.y += self.rect.height

    def draw_on_screen(self, surface: pg.Surface) -> None: surface.blit(self.image, self.rect)


class Bullet:
    def __init__(self, player_rect: pg.Rect) -> None:
        self.speed = 15
        self.player_rect = player_rect
        self.image = pg.image.load("assets/shot.gif")
        self.rect = self.image.get_rect()
        self.rect.center = self.player_rect.midtop

    def update(self) -> None: self.rect.y -= self.speed

    def draw_on_screen(self, surface: pg.Surface) -> None:
        self.image = pg.transform.scale(self.image, (self.rect.width * 1.5, self.rect.height * 1.5))
        surface.blit(self.image, self.rect)


class Explosion:
    def __init__(self, rect: pg.Rect) -> None:
        self.image = pg.image.load("assets/explosion1.gif")
        self.rect = self.image.get_rect()
        self.rect.center = rect.center
        self.index = 0

    def play_explosion_sound(self) -> None:
        sound = pg.mixer.Sound("assets/boom.wav")
        sound.play()

    def draw_on_screen(self, surface: pg.Surface) -> None: surface.blit(self.image, self.rect)