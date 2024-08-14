import pygame
import sys
import random
from grid import Grid

"""Main entry point of the app"""
# Initialize pygame
pygame.init()

# Define the screen dimensions
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))


def main():
    grid = Grid()
    print("Initialize Crossword")
    grid.display_grid()
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Fill the screen with black
        grid.cell_grid.draw(screen)  # Draw all the cells
        pygame.display.flip()  # Update the screen

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
