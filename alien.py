from pickle import TRUE
import pygame
from pygame.sprite import Sprite

# class for single alien
class Alien(Sprite):

    # initialize alien and set start post.
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load alien image and set its rect attribute
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        # start each new alien in top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the aliens' exact horz. post.
        self.x = float(self.rect.x)

    # move alien to the right or left
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    # return true if alien is at the edge of screen
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return TRUE
