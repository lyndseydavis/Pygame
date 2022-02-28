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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    # start the main loop for the game
    def run_game(self):
        # watch for keyboard and mouse events
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    # respond to keypresses and mouse events
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # move the ship to the right and left
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    # respond to key pressing
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    # respond to key releases
    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K.LEFT:
            self.ship.moving_left = False

    # update images on the screen and flip to new screen
    def _update_screen(self):
        # redraw screen on each pass
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # make most recent screen visible
        pygame.display.flip()


# make a game instance and run the game
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
