# Written by Curtis Newton

try: import pygame as pg, random, sys, sprites
except ImportError: raise SystemExit("Sorry, can´t find required libraries")

pg.init()
pg.mixer.init()

class Game:
    def __init__(self) -> None:
        self.SCREENRECT = pg.Rect(0, 0, 126 * 5, 480)
        self.GAME_STATE = False

        self.screen = pg.display.set_mode(self.SCREENRECT.size)
        pg.display.set_caption("Shoot´em up v2.0")
        icon = pg.image.load("assets/alien1.png")
        pg.display.set_icon(icon)

        self.bg = pg.image.load("assets/background.gif")
        self.player = sprites.Player(self.SCREENRECT)
        self.enemies, self.bullets, self.explosions = [], [], []
        self.create_enemy_list()

        self.score_font, self.credits_font = pg.font.Font(None, 30), pg.font.Font(None, 20)

    def draw_texts(self) -> None:
        score = self.score_font.render(f"Score : {self.player.score}", 0, [255, 255, 255])
        self.screen.blit(score, (10, self.SCREENRECT.height - 50))
        credits = self.credits_font.render("Written by Curtis Newton, v2.0, inspired from the ´pygame.examples.aliens´ shooter.", 0, [255, 255, 255])
        self.screen.blit(credits, (5, 5))


    def draw_menu(self) -> None:
        big_title = self.score_font.render("Shoot´em up v2.0, by Curtis Newton", 0, [255, 255, 255])
        big_title_rect = big_title.get_rect()
        start_text = self.credits_font.render("Press Space Key to start", 0, [255, 255, 255])
        start_text_rect = start_text.get_rect()
        self.screen.blit(big_title, (self.SCREENRECT.width / 2 - big_title_rect.width / 2, 10))
        self.screen.blit(start_text, (self.SCREENRECT.width / 2 - start_text_rect.width / 2, self.SCREENRECT.height / 2 - start_text_rect.height / 2))

        for evt in pg.event.get():
            if evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE:
                pg.quit()
                break
                quit()
            elif evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE: self.GAME_STATE = True


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
        sprite_index = 0
        for bullet in self.bullets:
            for enemy in self.enemies:

                if bullet.rect.colliderect(enemy.rect):

                    try: del self.bullets[sprite_index]
                    except IndexError: continue

                    self.create_new_explosion(enemy)
                    enemy.respawn()
                    self.player.score += 1

                elif bullet.rect.y == 0 - bullet.rect.height:
                    try: del self.bullets[sprite_index]
                    except IndexError: continue

        sprite_index += 1

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

            if not self.GAME_STATE: self.draw_menu()

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
                    if evt.type == pg.QUIT or evt.type == pg.KEYDOWN and evt.key == pg.K_ESCAPE: self.GAME_STATE = False
                    if evt.type == pg.KEYDOWN and evt.key == pg.K_SPACE: self.bullets.append(sprites.Bullet(self.player.rect))

                clock.tick(25)

            pg.display.flip()


if __name__ == "__main__":
    app = Game()
    app.run()