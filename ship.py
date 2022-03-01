import pygame

# a class to manage the ship
class Ship:
    # initialize ship and start position
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship image and get its rect
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()

        # start each new ship in bottom center screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's horizontal post.
        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    # update the ship's position based on movement flag
    # update the x value and not rect
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    # draw the ship at its current locations
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # center ship on screen
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
