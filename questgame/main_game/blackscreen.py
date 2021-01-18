import pygame as pg
import sys
import os

class BlackScreen:

    def __init__(self, screen, config):

        self.screen = screen
        self.settings = config
        self.clock = pg.time.Clock()

        self.screen_rect = self.screen.get_rect()

        self.level_font = pg.font.Font(self.settings.main_game_fonts['black screen']['source'], self.settings.main_game_fonts['black screen']['size'])
        self.level_txt = self.level_font.render(f'Level: 1 - 1', True, self.settings.colors['white'])
        self.rect_level_txt = self.level_txt.get_rect()

        self.msg_lifes_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.msg_lifes_txt = self.msg_lifes_font.render(f'Lifes - ', True, self.settings.colors['white'])
        self.rect_msg_lifes_txt = self.msg_lifes_txt.get_rect()

        self.lifes_img = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.rect_lifes_img = self.lifes_img.get_rect()

        self.msg_start_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.msg_start_txt = self.msg_start_font.render('Press < SPACE > to start', True, self.settings.colors['white'])
        self.rect_msg_start_txt = self.msg_start_txt.get_rect()


        self.ticks = 0

        self.start = False

    def show_black_screen(self, lifes):
        while not self.start:
            dt = self.clock.tick(self.settings.FPS)
            self.__handle_events()
            self.__update_screen(dt, lifes)
        self.start = False

    def __handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.start = True

    def __update_screen(self, dt, lifes):
        self.ticks += dt

        self.screen.fill(self.settings.colors['black'])
        self.screen.blit(self.level_txt, (self.screen_rect.center[0]-self.rect_level_txt.center[0], 200))
        self.screen.blit(self.msg_lifes_txt, (270, 300))
        t = 372
        for life in range(lifes):
            self.screen.blit(self.lifes_img, (t, 282))
            t+=48
        t = 372
        if self.ticks <= 500:
            self.screen.blit(self.msg_start_txt, (self.screen_rect.center[0]-self.rect_msg_start_txt.center[0], 400))
        elif self.ticks <=1000:
            pass
        else:
            self.ticks = 0
        
        pg.display.flip()