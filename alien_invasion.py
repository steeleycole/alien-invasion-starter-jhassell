import pygame
import sys
from settings import Settings
from ship import Ship

# Initialize Pygame
pygame.init()

# Create an instance of Settings
ai_settings = Settings()

# Set up the window
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Alien Invasion")

# Create the ship
ship = Ship(ai_settings, screen)

# Colors
bright_red = (255, 0, 0)

# Font and text
font = pygame.font.SysFont(None, ai_settings.font_size)
text = font.render("Alien Invasion", True, bright_red)

# Clock for FPS
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill(ai_settings.bg_color)

    # Draw text at top center
    text_x = (ai_settings.screen_width - text.get_width()) // 2
    screen.blit(text, (text_x, 10))

    # Draw the ship
    ship.blitme()

    # Update display
    pygame.display.flip()

    # Cap at 60 FPS
    clock.tick(ai_settings.fps)

# Quit Pygame
pygame.quit()
sys.exit()