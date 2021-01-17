import pygame as pg
import random

class Meteor(pg.sprite.Sprite):

    def __init__(self, config, group):
        super().__init__(group)    
        self.meteor_selected = random.randrange(1, len(config.list_meteors))

        self.x = config.game_dimensions[0]
        self.y = random.randint(50, config.game_dimensions[1]-config.list_meteors[self.meteor_selected]['size'][1])

        self.meteor_speed = random.randint(5,7)

        self.image = config.list_meteors[self.meteor_selected]['image']
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def update(self):
        """
        The update method from Meteor
        """

        self.rect.x -= self.meteor_speed