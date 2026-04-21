import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet

# Initialize Pygame
pygame.init()

# Create an instance of Settings
ai_settings = Settings()

# Set up the window
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Alien Invasion")

# Create the ship
ship = Ship(ai_settings, screen)

# Create a sprite group to hold bullets
bullets = pygame.sprite.Group()

# Colors
bright_red = (255, 0, 0)

# Font and text
font = pygame.font.SysFont(None, ai_settings.font_size)
text = font.render("Alien Invasion", True, bright_red)

# Clock for FPS
clock = pygame.time.Clock()

def _check_events():
    """Handle events and user input."""
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                # Create a new bullet if limit not reached
                if len(bullets) < 3:
                    new_bullet = Bullet(ai_settings, screen, ship)
                    bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False

def _update_bullets():
    """Update bullet positions and remove off-screen bullets."""
    bullets.update()
    
    # Remove bullets that have gone off the top of the screen
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

def _update_screen():
    """Update images on screen and flip to new screen."""
    # Fill background
    screen.fill(ai_settings.bg_color)

    # Draw text at top center
    text_x = (ai_settings.screen_width - text.get_width()) // 2
    screen.blit(text, (text_x, 10))

    # Draw the ship
    ship.blitme()

    # Draw bullets
    for bullet in bullets:
        bullet.draw_bullet()

    # Update display
    pygame.display.flip()

# Main game loop
running = True
while running:
    _check_events()
    ship.update()
    _update_bullets()
    _update_screen()

    # Cap at 60 FPS
    clock.tick(ai_settings.fps)

# Quit Pygame
pygame.quit()
sys.exit()