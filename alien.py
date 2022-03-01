import pygame
from pygame.sprite import Sprite

# class for single alien
class Alien(Sprite):

    # initialize alien and set start post.
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # load alien image and set its rect attribute
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # start each new alien in top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the aliens' exact horz. post.
        self.x = float(self.rect.x)
