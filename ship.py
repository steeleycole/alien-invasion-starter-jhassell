import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings

        # Create the ship's surface
        self.width = 50
        self.height = 75
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))  # Make black transparent

        # Draw the ship shape: a triangle
        pygame.draw.polygon(self.image, (0, 255, 0), [(self.width // 2, 0), (0, self.height), (self.width, self.height)])

        # Get the rect
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)