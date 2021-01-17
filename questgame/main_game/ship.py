import pygame as pg
from pygame.locals import *
import os

class Ship(pg.sprite.Sprite):

    _img_size = 72

    def __init__(self, x, y, config):
        super().__init__()

        self.settings = config

        self.y_speed = self.settings.ship_speed
        self.state = self.settings.ship_states['alive']

        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.explosion_animation_image = self.__load_explosion_images()
        self.rect = self.image.get_rect(x=x, y=y)

        self.ix_explosion = 0
        self.delay_animation = 6
        self.ticks = 0
        self.ticks_animation = 1000//self.settings.FPS * self.delay_animation
        

    def update(self, dt):
        """
        The update method from Ship where we check if the top of ship
        get the min screen size or 0 and if the bottom of the ship get
        the max size screen and stops the ship. Then we check the
        moving ship method.
        """
        if self.state == self.settings.ship_states['exploding']:
            return self.__exploding(dt)

        elif self.state == self.settings.ship_states['dead']:
            self.reset()

        else:
            self.rect.y += self.y_speed

            if self.rect.top <= 50:
                self.rect.top = 50
            if self.rect.bottom >= self.settings.game_dimensions[1]:
                self.rect.bottom = self.settings.game_dimensions[1]

            self.__moving_ship()

    def __moving_ship(self):
        """
        Method that checks wich keys get pressed and move the ship
        in the correct direction.
        """

        key_pressed = pg.key.get_pressed()
        
        if key_pressed[K_UP]:
            self.y_speed = -self.settings.ship_speed
        elif key_pressed[K_DOWN]:
            self.y_speed = self.settings.ship_speed
        else:
            self.y_speed = 0

    def __load_explosion_images(self):
        return [pg.image.load(os.path.join(self.settings.folders.images_folder_explosion, f'explosion_{x}.xcf')) for x in range(8)]
    
    def __exploding(self, dt):
        if self.ix_explosion >= len(self.explosion_animation_image):
            self.state = self.settings.ship_states['dead']
            return

        self.image = self.explosion_animation_image[self.ix_explosion]

        self.ticks += dt
        if self.ticks >= self.ticks_animation:
            self.ix_explosion +=1
            self.ticks = 0

    def reset(self):
        self.state = self.settings.ship_states['alive']
        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.ix_explosion = 0
        self.delay_animation = 6
        self.ticks = 0