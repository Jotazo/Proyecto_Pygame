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

        # Planet incoming
        self.planet_img = pg.image.load(os.path.join(self.settings.folders.images_folder, 'planet2.png'))
        self.rect_planet_img = self.planet_img.get_rect()
        self.planet_x = 700

        self.x_landing_zone = -48 # For landing zone movement

        self.blink_msg = 0 # For the end message blinks

        self.background_x = 0 # For background movement
        self.ix = 0 # For speed create meteors

        self.meteors_dodged = 0
        self.score = 0

        # Instances
        self.top_level_frame = toplevelframe.TopLevelFrame(self.settings)
        self.ship = ship.Ship(2, 300, self.settings)
        self.meteors = pg.sprite.Group()
        self.clock = pg.time.Clock()

        # Starting screen and black screen Instances
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
                self.__add_meteor(self.ix, self.meteors_dodged)
                self.__update_meteors()
                self.top_level_frame.update(self.ship.lifes, self.score, self.meteors_dodged)

            self.ship.update(dt)
            self.__update_screen()
            print(self.blink_msg)
            if self.ship.lifes == 0:
                game_over = True 

            self.ix += 1

    def __add_meteor(self, timer, meteors_dodged):
        """
        This method checks, first of all, if we get the max
        meteors dodged. If not, we add a new meteor at our sprite
        group of meteors.
        When we get the max meteors dodged, we're gonna remove every
        meteor we have in screen as they reach the limit
        """
        if meteors_dodged >= self.settings.end_meteors_dodged:
            for mt in self.meteors:
                if mt.rect.right <= 0:
                    self.meteors.remove(mt)
        else:
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
                if event.key == pg.K_SPACE and self.meteors_dodged >= self.settings.end_meteors_dodged and\
                        (self.ship.rect.top >= 260 and self.ship.rect.bottom <= 320) and self.planet_x <= 400:
                    self.ship.state = self.settings.ship_states['rotating']
                if event.key == pg.K_SPACE and self.ship.state == self.settings.ship_states['disappeared']:
                    pg.quit()
                    sys.exit()
        
    def __update_meteors(self):
        """
        This method checks first of all for update method from Meteor
        Then, we check if meteor/meteors get the min width of our screen
        If True, we remove that meteor from our meteors group, we add a
        dodged meteor to our score, and we add de points of the meteor.
        When we have the max meteors dodged, then we stop to adding score
        and meteors dodged to our score box.
        """
        self.meteors.update()

        for meteor in self.meteors:
            if meteor.rect.right <= 0 and self.meteors_dodged < self.settings.end_meteors_dodged:
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

        # End Planet and land message blit
        if self.meteors_dodged >= self.settings.end_meteors_dodged:
            if self.planet_x >= 400 and self.ship.state == self.settings.ship_states['alive']:
                self.planet_x -= 2
            else:
                if self.ship.state == self.settings.ship_states['alive']:
                    self.__rotate_msg()
                    self.__rotating_zone()

            self.screen.blit(self.planet_img, (self.planet_x, 35))

        # Ship blit
        if self.ship.state == self.settings.ship_states['rotating']:
            self.screen.blit(self.ship.image, (self.ship.rect))
        else:
            self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))

        # Landing Message
        if self.ship.state == self.settings.ship_states['landing']:
            self.__landing_msg()

        # Landed Message and planet and ship disappearing
        if self.ship.state == self.settings.ship_states['landed']:
            self.__landed_msg()
            if self.planet_x <= 800:
                self.planet_x += 2
                self.ship.rect.x += 2
                self.screen.blit(self.planet_img, (self.planet_x, 35))
                self.screen.blit(self.ship.image, (self.ship.rect.x, self.ship.rect.y))
            else:
                self.ship.state = self.settings.ship_states['disappeared']

        # End Level Message
        if self.ship.state == self.settings.ship_states['disappeared']:
            self.__end_lvl_msg()

        # Top level blit
        self.screen.blit(self.top_level_frame.top_image, (0,0))
        self.screen.blit(self.top_level_frame.lifes_count_img, (50, 15))
        self.screen.blit(self.top_level_frame.dodged_meteors_img, (250, 15))
        self.screen.blit(self.top_level_frame.score_count_img, (600, 15))

        pg.display.flip()

    def __ship_meteor_colision(self):
        """
        Method that checks if ship and meteor has collided.
        When ship and meteor collides, we change ship state to
        exploding, stop background music and start explosion
        sound.
        """

        colision = pg.sprite.spritecollide(self.ship, self.meteors, False)

        if colision and self.ship.state != self.settings.ship_states['exploding']:

            self.ship.state = self.settings.ship_states['exploding']
            self.background_sound.stop()
            self.settings.ship_explosion.set_volume(0.02)
            self.settings.ship_explosion.play()

    def __reset_screen(self):
        """
        Method that reset the needed values for restart the game
        """

        self.background_x = 0
        self.ix = 0
        self.planet_x = 700
        self.meteors_dodged = 0
        self.meteors.empty()
        self.background_sound.play()

    def __rotating_zone(self):
        """
        Method that creates the landing zone on the screen
        """

        if self.x_landing_zone < 3:
            self.x_landing_zone += 1
        pg.draw.rect(self.screen, self.settings.colors['red'],[self.x_landing_zone, 276, 48, 48], 1)

    def __rotate_msg(self):
        """
        Method that blit the rotating message
        """
        land_msg = pg.font.Font(self.settings.main_game_fonts['default'], 16)
        land_msg_img = land_msg.render('Press < SPACE > for rotate the ship', True, self.settings.colors['white'])
        self.screen.blit(land_msg_img, (60, 80))

    def __landing_msg(self):
        """
        Method that blit the landing message
        """
        landing_message = pg.font.Font(self.settings.main_game_fonts['default'], 16)
        landing_message_img = landing_message.render('Landing...', True, self.settings.colors['white'])
        rect_landing_message_img = landing_message_img.get_rect()
        self.screen.blit(landing_message_img, (400-(rect_landing_message_img.w//2), 80))

    def __landed_msg(self):
        """
        Method that blit the landed message
        """
        landed_message = pg.font.Font(self.settings.main_game_fonts['default'], 16)
        landed_message_img = landed_message.render('Succesfully Landed!', True, self.settings.colors['white'])
        rect_landed_message_img = landed_message_img.get_rect()
        self.screen.blit(landed_message_img, (400-(rect_landed_message_img.w//2), 80))

    def __end_lvl_msg(self):
        """
        Method that blit the end level message
        """

        end_lvl_message = pg.font.Font(self.settings.main_game_fonts['ready'], 64)
        end_lvl_message_img = end_lvl_message.render('JUPITER CONQUERED!', True, self.settings.colors['white'])
        rect_end_lvl_message_img = end_lvl_message_img.get_rect()

        press_space_msg = pg.font.Font(self.settings.main_game_fonts['default'], 20)
        press_space_msg_img = press_space_msg.render('Press < SPACE > to continue', True, self.settings.colors['white'])
        rect_press_space_msg_img = press_space_msg_img.get_rect()

        if self.blink_msg <= 50:
            self.screen.blit(press_space_msg_img, (400-(rect_press_space_msg_img.w//2), 450))
        else:
            if self.blink_msg >= 100:
                self.blink_msg = 0

        self.screen.blit(end_lvl_message_img, (400-(rect_end_lvl_message_img.w//2), 300-(rect_end_lvl_message_img.h//2)))

        self.blink_msg += 1
        

    