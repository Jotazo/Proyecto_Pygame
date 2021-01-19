import pygame as pg
from pygame.locals import *
import os

class Ship(pg.sprite.Sprite):

    def __init__(self, x, y, config):
        super().__init__()

        self.settings = config

        self.lifes = self.settings.ship_lifes
        self.y_speed = self.settings.ship_speed
        self.state = self.settings.ship_states['alive']

        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.explosion_animation_image = self.__load_explosion_images()
        self.rect = self.image.get_rect(x=x, y=y)

        self.image2 = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.rotated_image = None
        self.rect_rotated_image = None

        self.angle = 0

        self.ix_explosion = 0
        self.delay_animation = 6
        self.ticks = 0
        self.ticks_animation = 1000//self.settings.FPS * self.delay_animation

    def update(self, dt):
        """
        The update method from Ship where we check, first of all, the
        state of our ship, 'alive', 'exploding' and 'dead'. 
        If the ship is alive, we check the top and bottom margin and
        we call to moving_ship()
        If the ship is exploding, we return the animation exploding()
        And, if the ship is dead, we take off a ship life and call
        reset()
        """
        if self.state == self.settings.ship_states['exploding']:
            return self.__exploding(dt)

        elif self.state == self.settings.ship_states['dead']:
            self.__reset()

        elif self.state == self.settings.ship_states['rotating']:
            self.__rotate()

        elif self.state == self.settings.ship_states['landing']:
            self.__landing()

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
        in that direction.
        """
        key_pressed = pg.key.get_pressed()
        
        if key_pressed[K_UP]:
            self.y_speed = -self.settings.ship_speed
        elif key_pressed[K_DOWN]:
            self.y_speed = self.settings.ship_speed
        else:
            self.y_speed = 0

    def __load_explosion_images(self):
        """
        Method that returns a list with all the explosion images
        """
        return [pg.image.load(os.path.join(self.settings.folders.images_folder_explosion, f'explosion_{x}.xcf')) for x in range(8)]

    def __exploding(self, dt):
        """
        Method that shows the explosion animation
        """
        if self.ix_explosion >= len(self.explosion_animation_image):
            self.state = self.settings.ship_states['dead']
            self.lifes -= 1
            return

        self.image = self.explosion_animation_image[self.ix_explosion]

        self.ticks += dt
        if self.ticks >= self.ticks_animation:
            self.ix_explosion +=1
            self.ticks = 0

    def __reset(self):
        """
        Method that reset the ship state and image, and de vars for the
        explosion animation
        """
        self.state = self.settings.ship_states['alive']
        self.image = pg.image.load(os.path.join(self.settings.folders.images_folder, 'ship_1_48x48.xcf'))
        self.ix_explosion = 0
        self.delay_animation = 6
        self.ticks = 0

    def __rotate(self):

        if self.angle <= 180:
            self.rotated_image = pg.transform.rotozoom(self.image2, self.angle, 1)
            self.rect_rotated_image = self.rotated_image.get_rect(center = (26, 300))
            self.image = self.rotated_image
            self.rect = self.rect_rotated_image
            self.angle += 1
        else:
            self.state = self.settings.ship_states['landing']

    def __landing(self):
        if self.rect.x < 525:
            self.rect.x += 2.5
        else:
            self.state = self.settings.ship_states['landed']
