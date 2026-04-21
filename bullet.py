import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship):
        """Initialize the bullet and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Create the bullet's rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, 5, 15)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's y coordinate as a float for smooth movement
        self.y = float(self.rect.y)

        # Bullet speed
        self.speed = -3

        # Bullet color
        self.color = (255, 255, 255)

    def update(self):
        """Update the bullet's position."""
        # Update position
        self.y += self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
