import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

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

        # create an instance to store game stats & scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # make the play button
        self.play_button = Button(self, "Play")

    # start the main loop for the game
    def run_game(self):
        # watch for keyboard and mouse events
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # update position and get rid of old bullets
    # update bullet position
    def _update_bullets(self):
        self.bullets.update()
        # get rid of bullets that have disappeard
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    # check for bullets that hit aliens
    # if so, get rid of bullet and alien
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # add points to score for collisions
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # destroy exsisting bullets and create new fleet
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    # create a fleet of aliens
    def _create_fleet(self):
        # make an alien
        alien = Alien(self)
        # calculate number of aliens and spacing between each per row
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # calculate number of rows
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        # create full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create alien and place in row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    # update the position of aliens in fleet
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens reaching bottom
        self._check_aliens_bottom()

    # respond appropriately if alien reaches edge
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    # drop the entire fleet and change direction
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    # respond to key pressing
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # respond to key releases
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # start a new game when player hits play
    def _check_play_button(self, mouse_pos):
        # deactivate play button when disappeared
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()

            # reset game stats
            self.stats.reset_stats()

            # change status to active
            self.stats.game_active = True
            self.sb.prep_score()

            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

    # create a bullet and add to bullet group
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # update images on the screen and flip to new screen
    def _update_screen(self):
        # redraw screen on each pass
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw the score info
        self.sb.show_score()

        # draw play button on screen if game inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make most recent screen visible
        pygame.display.flip()

    # respond to ship being hit by alien
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # decrease number of ships by 1
            self.stats.ships_left -= 1

            # get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        # game over
        else:
            # make game inactive
            self.stats.game_active = False
            # show mouse
            pygame.mouse.set_visible(True)

    # check if any aliens reached bottom of screen
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat as if ship was hit
                self._ship_hit()
                break


# make a game instance and run the game
if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
