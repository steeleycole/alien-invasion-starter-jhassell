import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Alien Invasion")

# Colors
dark_blue = (0, 0, 50)
bright_red = (255, 0, 0)

# Font and text
font = pygame.font.SysFont(None, 48)
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
    screen.fill(dark_blue)

    # Draw text at top center
    text_x = (800 - text.get_width()) // 2
    screen.blit(text, (text_x, 10))

    # Update display
    pygame.display.flip()

    # Cap at 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()