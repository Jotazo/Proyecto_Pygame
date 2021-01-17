import pygame as pg
import sys
import random
import os

from questgame.main_game import ship, meteor, config

class Game:

    pg.init()

    def __init__(self):
        # Settings instance
        self.settings = config.Settings()

        # Instances
        self.ship = ship.Ship(2, 284, self.settings)
        self.meteors = pg.sprite.Group()
        self.clock = pg.time.Clock()

        # Game Screen Configuration
        self.screen = pg.display.set_mode(self.settings.game_dimensions)
        pg.display.set_caption("The Quest")
        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'background.xcf'))
        self.rect = self.image.get_rect()

        self.background_x = 0 # For background movement
        self.ix = 0 # For speed create meteors

        self.meteors_dodged = 0
        self.score = 0

        # Other config
        self.lifes = self.settings.ship_lifes
        self.__top_level_frame()
        

    def main_loop(self):
        """
        The main loop game.
        """
        # TODO: End Level
        while self.lifes > 0:
            dt = self.clock.tick(self.settings.FPS)
            # Events    
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            # Check for ship states
            if self.ship.state == self.settings.ship_states['dead']:
                self.__reset_screen()
            else:
                self.__ship_meteor_colision()
                self.__add_meteor(self.ix)
                self.__update_meteors()
                self.__update_top_level(self.lifes, self.score, self.meteors_dodged)
            
            self.ship.update(dt)
            self.__update_screen(self.background_x)
                
            self.background_x -= 1
            self.ix += 1

    def __add_meteor(self, timer):
        """
        This method checks if our meteors group is lower than max_meteors and
        if True then we add a new meteor to our meteors group
        """
        if timer % 20 == 0:
            if len(self.meteors) < self.settings.max_meteors:
                self.meteors.add(meteor.Meteor(self.settings, self.meteors))

    def __update_meteors(self):
        """
        This method checks first of all for update method from Meteor
        Then, we check if meteor/meteors get the min width of our screen
        If True, we remove that meteor from our meteors group, we add a
        dodged meteor to our score, and we add de points of the meteor.
        """
        self.meteors.update()

        for meteor in self.meteors:
            if meteor.rect.right <= 0:
                self.meteors.remove(meteor)
                self.meteors_dodged += 1
                self.score += self.settings.list_meteors[meteor.meteor_selected]['points']

    def __update_screen(self, x):
        """
        Method that blit all the needed for our screen.
        """

        # Background blit
        x_rel = x % self.rect.width
        self.screen.blit(self.image, (x_rel - self.rect.width ,0))
        if x_rel < self.settings.game_dimensions[0]:
            self.screen.blit(self.image, (x_rel,0))

        # Meteors blit
        for meteor in self.meteors:
            self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

        # Ship blit
        self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))

        # Top level blit
        self.screen.blit(self.top_level_image, (0,0))
        self.screen.blit(self.lifes_count_img, (50, 12))
        self.screen.blit(self.dodged_meteors_img, (250, 12))
        self.screen.blit(self.score_count_img, (600, 12))

        pg.display.flip()

    def __ship_meteor_colision(self):
        """
        Method that checks if ship and meteor has collided.
        """
        colision = pg.sprite.spritecollide(self.ship, self.meteors, False)
        if colision:
            self.ship.state = self.settings.ship_states['exploding']
            # TODO: parar pantalla y mostrar animación

    def __top_level_frame(self):
        # Top level
        self.top_level_image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'score1.png'))
        self.top_level_rect = self.image.get_rect()

        # Top level lifes
        self.lifes_count_font = pg.font.Font(os.path.join(self.settings.folders.fonts_folder, 'FastHand-lgBMV.ttf'), 24)
        self.lifes_count_img = self.lifes_count_font.render(f'Lifes - {self.lifes}', True, self.settings.colors['white'])

        # Top level score
        self.score_count_font = pg.font.Font(os.path.join(self.settings.folders.fonts_folder, 'FastHand-lgBMV.ttf'), 24)
        self.score_count_img = self.score_count_font.render(f'Score - {self.score}', True, self.settings.colors['white'])

        # Top level dodged meteors
        self.dodged_meteors_font = pg.font.Font(os.path.join(self.settings.folders.fonts_folder, 'FastHand-lgBMV.ttf'), 24)
        self.dodged_meteors_img = self.score_count_font.render(f'Dodged Meteors - {self.meteors_dodged}', True, self.settings.colors['white'])

    def __update_top_level(self, lifes, score, meteors):
        self.lifes_count_img = self.lifes_count_font.render(f'Lifes - {lifes}', True, self.settings.colors['white'])
        self.score_count_img = self.score_count_font.render(f'Score - {score}', True, self.settings.colors['white'])
        self.dodged_meteors_img = self.score_count_font.render(f'Dodged Meteors - {meteors}', True, self.settings.colors['white'])

    def __reset_screen(self):
        self.background_x = 0
        self.ix = 0
        self.meteors_dodged = 0
        self.meteors.empty()
        self.lifes -= 1
        
