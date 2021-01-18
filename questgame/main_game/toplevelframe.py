import pygame as pg
import os

class TopLevelFrame:

    def __init__(self, config):

        self.settings = config

        self.top_image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'score1.png'))
        self.top_image_rect = self.top_image.get_rect()

        self.lifes_count_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.lifes_count_img = self.lifes_count_font.render(f'Lifes - 3', True, self.settings.colors['white'])

        self.score_count_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.score_count_img = self.score_count_font.render(f'Score - 0', True, self.settings.colors['white'])

        self.dodged_meteors_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.dodged_meteors_img = self.score_count_font.render(f'Dodged Meteors - 0', True, self.settings.colors['white'])        

    def update(self, lifes, score, meteors):
        self.lifes_count_img = self.lifes_count_font.render(f'Lifes - {lifes}', True, self.settings.colors['white'])
        self.score_count_img = self.score_count_font.render(f'Score - {score}', True, self.settings.colors['white'])
        self.dodged_meteors_img = self.score_count_font.render(f'Dodged Meteors - {meteors}', True, self.settings.colors['white'])