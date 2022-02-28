import sys
import pygame
from settings import Settings
from ship import Ship

# overall class to manage game assets and behavior
class AlienInvasion:
    # initialize the game and create resources
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    # start the main loop for the game
    def run_game(self):
        # watch for keyboard and mouse events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            # make most recent screen visible
            pygame.display.flip()


# make a game instance and run the game
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
