import pygame as pg
import sys

class InitialScreen:

    def __init__(self, screen, bg_image, ship, toplevelframe, config, clock):
        # Dependences
        self.screen = screen
        self.ship = ship
        self.top_level_frame = toplevelframe
        self.settings = config
        self.bg_image = bg_image
        self.clock = clock

        self.screen_rect = self.screen.get_rect()

        # Animation
        self.y = -50
        self.delay_animation = 6
        self.ticks = 0
        self.ticks_animation = 1000//self.settings.FPS * self.delay_animation

        # Ready and start message
        self.ready_font = pg.font.Font(self.settings.main_game_fonts['ready']['source'], self.settings.main_game_fonts['ready']['size'])
        self.ready_img = self.ready_font.render(f'READY?', True, self.settings.colors['white'])

        self.msg_start_font = pg.font.Font(self.settings.main_game_fonts['default']['source'], self.settings.main_game_fonts['default']['size'])
        self.msg_start_img = self.msg_start_font.render('Press < SPACE > to start', True, self.settings.colors['white'])
        self.rect_msg_start_img = self.msg_start_img.get_rect()

        # Variables
        self.start = False

    def starting_screen(self):
        while not self.start:
            dt = self.clock.tick(self.settings.FPS)
            self.__handle_events()
            self.__update(self.y, dt)
            self.__top_level_animation(dt)

    def __handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and self.y == 0:
                    self.start = True

    def __update(self, y, dt):
        """
        Update method that blits the screen.
        If the top level frame and ship are in the right position, 
        it is when 'y' == 0, then we show the ready message
        """

        self.screen.blit(self.bg_image, (0,0))

        self.screen.blit(self.top_level_frame.top_image, (0, y))
        self.screen.blit(self.top_level_frame.lifes_count_img, (50, y+15))
        self.screen.blit(self.top_level_frame.dodged_meteors_img, (250, y+15))
        self.screen.blit(self.top_level_frame.score_count_img, (600, y+15))

        self.screen.blit(self.ship.image, (y+2, 307))
        if y == 0:
            self.__ready_start_msg(dt)

        pg.display.flip()

    def __top_level_animation(self, dt):
        """
        Method for show the top level frame and ship at the same
        time.
        """
        if self.y == 0:
            return
            
        self.ticks += dt
        if self.ticks >= self.ticks_animation:
            self.y += 1
            self.ticks = 0

    def __ready_start_msg(self, dt):
        """
        Method that shows the ready message and a blink 
        'Press <SPACE> button to start'
        """
        self.ticks += dt

        self.screen.blit(self.ready_img, (300, 200))

        if self.ticks <= 1000:
            self.screen.blit(self.msg_start_img, (self.screen_rect.center[0]-self.rect_msg_start_img.center[0], 300))
        elif self.ticks <=1500:
            pass
        else:
            self.ticks = 0