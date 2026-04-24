import pygame
from pygame.sprite import Sprite
from bullet import AlienBullet


class Alien(Sprite):
    """A class to represent a single alien ship."""

    def __init__(self, ai_settings, screen, x, y):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Create the alien's surface
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent

        # Draw the alien shape: a diamond
        pygame.draw.polygon(self.image, (255, 0, 255), [
            (self.width // 2, 0),           # Top
            (self.width, self.height // 2), # Right
            (self.width // 2, self.height), # Bottom
            (0, self.height // 2)           # Left
        ])

        # Get the rect and set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Alien speed (moves left to right)
        self.speed = 3.0
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Update the alien's position."""
        self.rect.x += self.speed * self.direction

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)


class Captain(Sprite):
    """A class to represent a captain alien ship."""

    def __init__(self, ai_settings, screen, x, y):
        """Initialize the captain and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Create the captain's surface
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent

        # Draw the captain shape: a diamond (yellow)
        pygame.draw.polygon(self.image, (255, 255, 0), [
            (self.width // 2, 0),           # Top
            (self.width, self.height // 2), # Right
            (self.width // 2, self.height), # Bottom
            (0, self.height // 2)           # Left
        ])

        # Get the rect and set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Captain speed (moves left to right)
        self.speed = 3.0
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Update the captain's position."""
        self.rect.x += self.speed * self.direction

    def blitme(self):
        """Draw the captain at its current location."""
        self.screen.blit(self.image, self.rect)


class Aliens(pygame.sprite.Group):
    """A class to manage all alien ships."""

    def __init__(self, ai_settings, screen):
        """Initialize the aliens group."""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        # Create three aliens positioned toward the middle top
        self._create_fleet()

    def _create_fleet(self):
        """Create the initial fleet of aliens."""
        # Create three aliens
        screen_width = self.ai_settings.screen_width
        screen_height = self.ai_settings.screen_height

        # Position aliens in the middle top area (below title text)
        start_y = 80
        spacing = (screen_width - 120) // 2

        for i in range(3):
            alien_x = 40 + i * spacing
            alien = Alien(self.ai_settings, self.screen, alien_x, start_y)
            self.add(alien)

    def update(self):
        """Update all aliens and handle bouncing at screen edges."""
        super().update()

        # Check if any alien has hit the edge and bounce the fleet
        for alien in self:
            if alien.rect.right >= self.ai_settings.screen_width:
                alien.rect.right = self.ai_settings.screen_width
                self._bounce_fleet()
                break
            elif alien.rect.left <= 0:
                alien.rect.left = 0
                self._bounce_fleet()
                break

    def _bounce_fleet(self):
        """Bounce the fleet off the screen edges."""
        for alien in self:
            alien.direction *= -1

    def blitme(self):
        """Draw all aliens on the screen."""
        for alien in self:
            alien.blitme()

    def shoot(self, alien_bullets):
        """Randomly shoot bullets from aliens."""
        import random
        # Only allow shooting if under the bullet limit
        if len(alien_bullets) < 3:
            # 5% chance per frame for each alien to shoot
            for alien in self:
                if random.random() < 0.05:
                    new_bullet = AlienBullet(self.ai_settings, self.screen, alien)
                    alien_bullets.add(new_bullet)


class Captains(pygame.sprite.Group):
    """A class to manage all captain alien ships."""

    def __init__(self, ai_settings, screen):
        """Initialize the captains group."""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen

    def _create_fleet(self):
        """Create the captain fleet."""
        # Create two captains
        screen_width = self.ai_settings.screen_width
        screen_height = self.ai_settings.screen_height

        # Position captains in the middle top area (below title text)
        start_y = 80
        spacing = screen_width - 120

        for i in range(2):
            captain_x = 60 + i * spacing
            captain = Captain(self.ai_settings, self.screen, captain_x, start_y)
            self.add(captain)

    def update(self):
        """Update all captains and handle bouncing at screen edges."""
        super().update()

        # Check if any captain has hit the edge and bounce the fleet
        for captain in self:
            if captain.rect.right >= self.ai_settings.screen_width:
                captain.rect.right = self.ai_settings.screen_width
                self._bounce_fleet()
                break
            elif captain.rect.left <= 0:
                captain.rect.left = 0
                self._bounce_fleet()
                break

    def _bounce_fleet(self):
        """Bounce the fleet off the screen edges."""
        for captain in self:
            captain.direction *= -1

    def blitme(self):
        """Draw all captains on the screen."""
        for captain in self:
            captain.blitme()

    def shoot(self, alien_bullets):
        """Randomly shoot bullets from captains."""
        import random
        # Only allow shooting if under the bullet limit
        if len(alien_bullets) < 3:
            # 5% chance per frame for each captain to shoot
            for captain in self:
                if random.random() < 0.05:
                    new_bullet = AlienBullet(self.ai_settings, self.screen, captain, damage=20)
                    alien_bullets.add(new_bullet)
