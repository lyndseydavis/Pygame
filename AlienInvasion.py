import sys
import pygame
from settings import Settings

# overall class to manage game assets and behavior
class AlienInvasion:
    # initialize the game and create resources
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        # set background color
        self.bg_color = (230, 230, 230)

    # start the main loop for the game
    def run_game(self):
        # watch for keyboard and mouse events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # redraw the screen during each pass through the loop
            self.screen.fill(self.bg_color)
            # make most recent screen visible
            pygame.display.flip()


# make a game instance and run the game
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
