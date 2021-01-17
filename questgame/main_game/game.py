import pygame as pg
import sys
import random
import os

from questgame.main_game import ship, meteor, config, toplevelframe

class Game:

    pg.init()

    def __init__(self):
        # Settings instance
        self.settings = config.Settings()

        # Game Screen Configuration
        self.screen = pg.display.set_mode(self.settings.game_dimensions)
        pg.display.set_caption("The Quest")
        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'background.xcf'))
        self.rect = self.image.get_rect()

        self.background_x = 0 # For background movement
        self.ix = 0 # For speed create meteors

        self.meteors_dodged = 0
        self.score = 0

        # Instances
        self.top_label_frame = toplevelframe.TopLevelFrame(self.settings)
        self.ship = ship.Ship(2, 300, self.settings)
        self.meteors = pg.sprite.Group()
        self.clock = pg.time.Clock()

        # Sounds Configuration
        self.background_sound = self.settings.background_sound
        self.background_sound.set_volume(0.02)
        self.background_sound.play(-1)
        
    def main_loop(self):
        """
        The main loop game.
        """
        # TODO: End Level
        self.initial_screen()
        while self.ship.lifes > 0:
            dt = self.clock.tick(self.settings.FPS)
            self.__handle_events()
            # Check for ship states
            if self.ship.state == self.settings.ship_states['dead']:
                self.__reset_screen()
            else:
                self.__ship_meteor_colision()
                self.__add_meteor(self.ix)
                self.__update_meteors()
                self.top_label_frame.update(self.ship.lifes, self.score, self.meteors_dodged)
            
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

    def __handle_events(self):
        # Events    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
        
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
        self.screen.blit(self.top_label_frame.top_image, (0,0))
        self.screen.blit(self.top_label_frame.lifes_count_img, (50, 12))
        self.screen.blit(self.top_label_frame.dodged_meteors_img, (250, 12))
        self.screen.blit(self.top_label_frame.score_count_img, (600, 12))

        pg.display.flip()

    def __ship_meteor_colision(self):
        """
        Method that checks if ship and meteor has collided.
        """
        colision = pg.sprite.spritecollide(self.ship, self.meteors, False)

        if colision and self.ship.state != self.settings.ship_states['exploding']:

            self.ship.state = self.settings.ship_states['exploding']
            self.background_sound.stop()
            self.settings.ship_explosion.set_volume(0.02)
            self.settings.ship_explosion.play()
            # TODO: parar pantalla

    def __reset_screen(self):
        self.background_x = 0
        self.ix = 0
        self.meteors_dodged = 0
        self.meteors.empty()
        # self.lifes -= 1
        self.background_sound.play()
        
    def initial_screen(self):
        # TODO: Class for initial screen?
        start = False
        x = 0
        y = -50
        while not start:
            dt = pg.time.Clock()
            dt.tick(self.settings.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        start = True
            
            self.screen.blit(self.image, (0,0))
            self.screen.blit(self.top_label_frame.top_image, (0, y))
            self.screen.blit(self.top_label_frame.lifes_count_img, (50, y+12))
            self.screen.blit(self.top_label_frame.dodged_meteors_img, (250, y+12))
            self.screen.blit(self.top_label_frame.score_count_img, (600, y+12))
            self.screen.blit(self.ship.image, (y+2, 307))
            x += 1
            if x % 5 == 0 and y < 0:
                y += 1
            pg.display.flip()
            
