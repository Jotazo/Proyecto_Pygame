import pygame as pg
import random
import os
import folders

class Settings:

    def __init__(self):
        """
        Class Settings for our main game
        """
        # Folders instance
        self.folders = folders.Folders()

        # Screen Settings
        self.game_dimensions = (800, 600)
        self.FPS = 60

        # Sound Settings
        pg.mixer.init()
        self.background_sound = pg.mixer.Sound(os.path.join(self.folders.sounds_folder, 'background_sound.ogg'))
        self.ship_explosion = pg.mixer.Sound(os.path.join(self.folders.sounds_folder, 'explosion.wav'))

        # Meteor Settings
        self.max_meteors = 7
        self.list_meteors = {
                1:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'small_meteor1.png')),
                'size': (35,38),
                'points':10,
            },
                2:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'small_meteor2.png')),
                'size': (40,41),
                'points':10,
            },
                3:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'medium_meteor1.png')),
                'size': (65,71),
                'points':15,
            },
                4:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'medium_meteor2.png')),
                'size': (65,66),
                'points':15,
            },
                5:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'big_meteor1.png')),
                'size': (100,111),
                'points':20,
            },
                6:{
                'image': pg.image.load(os.path.join(self.folders.images_folder_meteors, 'big_meteor2.png')),
                'size': (100,101),
                'points':20,
            }
        }

        # Ship Settings
        self.ship_speed = 7
        self.ship_lifes = 3
        self.ship_states = {
            'alive':'a',
            'exploding':'e',
            'dead':'d'
        }
        

        # RGB Colors
        self.colors = {
            'white':(255, 255, 255),
            'black':(0, 0, 0),
            'red':(255, 0, 0),
            'green':(0, 255, 0),
            'blue':(0, 0, 255)
        }