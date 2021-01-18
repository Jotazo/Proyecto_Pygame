import pygame as pg
import sys
import random
import os

from questgame.main_game import ship, meteor, config, toplevelframe, initial_screen, blackscreen

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

        self.planet_img = pg.image.load(os.path.join(self.settings.folders.images_folder, 'planet2.png'))
        self.rect_planet_img = self.planet_img.get_rect()
        self.planet_x = 700

        self.background_x = 0 # For background movement
        self.ix = 0 # For speed create meteors

        self.meteors_dodged = 0
        self.score = 0

        # Instances
        self.top_level_frame = toplevelframe.TopLevelFrame(self.settings)
        self.ship = ship.Ship(2, 300, self.settings)
        self.meteors = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.initial_screen = initial_screen.InitialScreen(self.screen, self.image, self.ship, self.top_level_frame, self.settings, self.clock)
        self.black_screen = blackscreen.BlackScreen(self.screen, self.settings)

        # Sounds Configuration
        self.background_sound = self.settings.background_sound
        self.background_sound.set_volume(0.02)
        self.background_sound.play(-1)

    def game_screen(self):
        # TODO: INTRO SCREEN
        self.initial_screen.starting_screen()
        self.playing_screen()
        # TODO: RECORDS SCREEN

    def playing_screen(self):
        """
        The playing screen game.
        """
        game_over = False
        while not game_over:
            dt = self.clock.tick(self.settings.FPS)
            self.__handle_events()
            # Check for ship states
            
            if self.ship.state == self.settings.ship_states['dead']:
                self.black_screen.show_black_screen(self.ship.lifes)
                self.__reset_screen()

            else:
                self.__ship_meteor_colision()
                self.__add_meteor(self.ix)
                self.__update_meteors()
                self.top_level_frame.update(self.ship.lifes, self.score, self.meteors_dodged)
            
            self.ship.update(dt)
            self.__update_screen()

            if self.ship.lifes == 0:
                game_over = True 

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

    def __update_screen(self):
        """
        Method that blit all the needed for our screen.
        """

        # Background blit
        x_rel = self.background_x % self.rect.width
        self.screen.blit(self.image, (x_rel - self.rect.width ,0))
        if x_rel < self.settings.game_dimensions[0]:
            self.screen.blit(self.image, (x_rel,0))

        self.background_x -= 1

        # Meteors blit
        for meteor in self.meteors:
            self.screen.blit(meteor.image, (meteor.rect.x, meteor.rect.y))

        # Ship blit
        self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))

        # Top level blit
        self.screen.blit(self.top_level_frame.top_image, (0,0))
        self.screen.blit(self.top_level_frame.lifes_count_img, (50, 15))
        self.screen.blit(self.top_level_frame.dodged_meteors_img, (250, 15))
        self.screen.blit(self.top_level_frame.score_count_img, (600, 15))

        if self.meteors_dodged >= 10:
            if self.planet_x >= 400:
                self.screen.blit(self.planet_img, (self.planet_x, 35))
                self.planet_x -= 1
            else:
                self.screen.blit(self.planet_img, (self.planet_x, 35))
                
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

    def __reset_screen(self):
        self.background_x = 0
        self.ix = 0
        self.planet_x = 700
        self.meteors_dodged = 0
        self.meteors.empty()
        self.background_sound.play()
