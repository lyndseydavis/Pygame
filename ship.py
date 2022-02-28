import pygame

# a class to manage the ship
class Ship:
    # initialize ship and start position
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.scren_rect = ai_game.screen.get_rect()

        # load the ship image and get its rect
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # start each new ship in bottom center screen
        self.rect.midbottom = self.screen_rect.midbottom

    # draw the ship at its current locations
    def blitme(self):
        self.screen.blit(self.image, self.rect)
