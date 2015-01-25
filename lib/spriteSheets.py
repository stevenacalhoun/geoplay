import pygame
from pygame.locals import *
import constants

class SpriteSheet(object):
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()


    def get_image(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Set the transparent color
        transColor = image.get_at((0,0))
        image.set_colorkey(transColor)

        # Return the image
        return image
