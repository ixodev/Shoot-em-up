# Written by Curtis Newton and Younès B.

try: import pygame as pg, sys, sprites
except ImportError: print("Sorry, can't find required libraries.", file=sys.stderr)

pg.init()
pg.display.init()
pg.font.init()
pg.mixer.init()



class Game:
    def __init__(self) -> None:
        self.SCREENRECT = pg.Rect(0, 0, 126 * 5, 480)

        self.screen = pg.display.set_mode(self.SCREENRECT.size)
        pg.display.set_caption("Shoot´em up v2.0")
        pg.display.set_icon(pg.image.load("assets/alien1.png"))

        self.bg = pg.image.load("assets/background.gif")
        self.menu = Menu(self.screen)
        self.player = sprites.Player(self.SCREENRECT)
        self.enemies, self.bullets, self.explosions = [], [], []
        self.create_enemy_list()

        self.score_font, self.credits_font = pg.font.Font(None, 30), pg.font.Font(None, 20)

    def draw_texts(self) -> None:
        self.screen.blit(self.score_font.render(f"Score : {self.player.score}", 0, [255, 255, 255]), (10, self.SCREENRECT.height - 50))
        credits = self.credits_font.render("Written by Curtis Newton and Younès B., v2.0, inspired from the 'pygame.examples.aliens' shooter.", 0, [255, 255, 255])
        self.screen.blit(credits, (5, 5))

    def create_enemy_list(self) -> None:
        for i in range(5): self.enemies.append(sprites.Enemy(self.SCREENRECT))

    def iterate_on_sprites_lists(self) -> None:
        for enemy in self.enemies:
            enemy.move(enemy.direction)
            enemy.draw_on_screen(self.screen)
        for bullet in self.bullets:
            bullet.update()
            bullet.draw_on_screen(self.screen)
        self.check_sprite_collisions()

    def draw_background(self) -> None:
        for i in range(0, 5 * 126, 126): self.screen.blit(self.bg, (i, 0))

    def check_sprite_collisions(self) -> None:
        bullet_index = 0
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):

                    try: del self.bullets[bullet_index]
                    except IndexError: continue

                    self.create_new_explosion(enemy)
                    enemy.respawn()
                    self.player.score += 1

                elif bullet.rect.y == 0 - bullet.rect.height:
                    try: del self.bullets[bullet_index]
                    except IndexError: continue

            bullet_index += 1

    def create_new_explosion(self, enemy: sprites.Enemy) -> None:
        explosion = sprites.Explosion(enemy.rect)
        explosion.play_explosion_sound()
        self.explosions.append(explosion)

    def play_music(self) -> None:
        music = pg.mixer.music.load("assets/house_lo.ogg")
        pg.mixer.music.play(-1, 0.0, 0)

    def run(self) -> None:
        clock = pg.time.Clock()
        self.play_music()

        while True:
            self.draw_background()

            if not self.menu.GAME_STATE: self.menu.update()

            else:
                self.player.handle_inputs()
                self.player.draw_on_screen(self.screen)
                self.iterate_on_sprites_lists()
                self.draw_texts()

                try:
                    explosions_index = 0
                    for explosion in self.explosions:
                        explosion.draw_on_screen(self.screen)
                        explosion.index += 1
                        if explosion.index == 20: del self.explosions[explosions_index]
                        explosions_index += 1
                except IndexError: continue

                for evt in pg.event.get():
                    if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE: self.menu.GAME_STATE = False
                    if evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE: self.bullets.append(sprites.Bullet(self.player.rect))

                clock.tick(25)

            pg.display.flip()




class Menu:
    def __init__(self, screen: pg.Surface) -> None:
        self.GAME_STATE = False
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.button = pg.Rect(self.screen.get_width() / 2 - 30, self.screen.get_height() / 2 - 15, 60, 30)
        self.title = self.font.render("Shoot'em up v2.0, written by Y.B. and C.N.", 0, pg.Color("white"))
        self.buttontext = self.font.render("Play!", 0, pg.Color("black"))

    def update(self) -> None:
        self.screen.blit(self.title, (self.screen.get_width() / 2 - self.title.get_width() / 2, 50))
        pg.draw.rect(self.screen, pg.Color("yellow"), self.button)
        self.screen.blit(self.buttontext, self.button)

        pg.display.flip()

        for evt in pg.event.get():

            if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE:
                pg.quit()
                quit(0)

            elif evt.type == pg.MOUSEBUTTONDOWN:
                if self.button.collidepoint(evt.pos): self.GAME_STATE = True




if __name__ == "__main__":
    app = Game()
    app.run()