import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet, AlienBullet
from aliens import Aliens

# Initialize Pygame
pygame.init()

# Create an instance of Settings
ai_settings = Settings()

# Set up the window
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Earth Defense")

# Create the ship
ship = Ship(ai_settings, screen)

# Create the aliens
aliens = Aliens(ai_settings, screen)

# Create a sprite group to hold bullets
bullets = pygame.sprite.Group()

# Create a sprite group to hold alien bullets
alien_bullets = pygame.sprite.Group()

# Game state
ship_alive = True
game_over = False
score = 0
health = 100

# Colors
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

# Font and text
font = pygame.font.SysFont(None, ai_settings.font_size)
text = font.render("Earth Defense", True, bright_red)

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
                if len(bullets) < 5:
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

def _update_alien_bullets():
    """Update alien bullet positions and remove off-screen bullets."""
    alien_bullets.update()
    
    # Remove alien bullets that have gone off the bottom of the screen
    for bullet in alien_bullets.copy():
        if bullet.rect.top > ai_settings.screen_height:
            alien_bullets.remove(bullet)

def _check_bullet_alien_collisions():
    """Check for collisions between bullets and aliens."""
    global score
    
    # Check for any bullets that have hit aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    # Add points for each alien destroyed
    score += len(collisions) * 100
    
    # If all aliens are destroyed, create a new fleet
    if len(aliens) == 0:
        aliens._create_fleet()

def _check_alien_bullet_ship_collisions():
    """Check for collisions between alien bullets and the ship."""
    global ship_alive, game_over, health
    
    # Check if any alien bullet hit the ship
    collisions = pygame.sprite.spritecollide(ship, alien_bullets, True)
    
    if collisions:
        # Lose 10 HP for each bullet hit
        health -= len(collisions) * 10
        
        # Check if health reaches 0
        if health <= 0:
            ship_alive = False
            game_over = True

def _update_screen():
    """Update images on screen and flip to new screen."""
    # Fill background
    screen.fill(ai_settings.bg_color)

    # Draw text at top center
    text_x = (ai_settings.screen_width - text.get_width()) // 2
    screen.blit(text, (text_x, 10))

    # Draw the ship if alive
    if ship_alive:
        ship.blitme()

    # Draw aliens
    aliens.blitme()

    # Draw bullets
    for bullet in bullets:
        bullet.draw_bullet()

    # Draw alien bullets
    for bullet in alien_bullets:
        bullet.draw_bullet()

    # Draw score in bottom left corner
    score_font = pygame.font.SysFont(None, 36)
    score_text = score_font.render(f"Score: {score}", True, bright_red)
    screen.blit(score_text, (10, ai_settings.screen_height - 40))

    # Draw health in bottom right corner
    health_text = score_font.render(f"HP: {health}", True, bright_green)
    health_x = ai_settings.screen_width - health_text.get_width() - 10
    screen.blit(health_text, (health_x, ai_settings.screen_height - 40))

    # Draw game over message if applicable
    if game_over:
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, bright_red)
        game_over_x = (ai_settings.screen_width - game_over_text.get_width()) // 2
        game_over_y = (ai_settings.screen_height - game_over_text.get_height()) // 2 - 50
        screen.blit(game_over_text, (game_over_x, game_over_y))

        # Draw final score
        final_score_text = score_font.render(f"FINAL SCORE: {score}", True, bright_red)
        final_score_x = (ai_settings.screen_width - final_score_text.get_width()) // 2
        final_score_y = game_over_y + 80
        screen.blit(final_score_text, (final_score_x, final_score_y))

    # Update display
    pygame.display.flip()

# Main game loop
running = True
while running:
    _check_events()
    
    # Only update game if ship is alive
    if ship_alive:
        ship.update()
        aliens.update()
        aliens.shoot(alien_bullets)
        _update_bullets()
        _update_alien_bullets()
        _check_bullet_alien_collisions()
        _check_alien_bullet_ship_collisions()
    
    _update_screen()

    # Cap at 60 FPS
    clock.tick(ai_settings.fps)

# Quit Pygame
pygame.quit()
sys.exit()