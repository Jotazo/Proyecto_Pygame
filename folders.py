import os

class Folders:

    def __init__(self):
        self.main_folder = os.path.dirname(__file__)

        # Resources directory
        self.resources_folder = os.path.join(self.main_folder, 'resources')

        # Resources subdirectories
        self.fonts_folder = os.path.join(self.resources_folder, 'fonts')
        self.images_folder = os.path.join(self.resources_folder, 'images')
        self.images_folder_meteors = os.path.join(self.images_folder, 'meteors')
        self.images_folder_explosion = os.path.join(self.images_folder, 'explosion')
