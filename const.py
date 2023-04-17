import pygame.display

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
# size of screen, automatically determined according to your screen. Lower if there is a high load on the system

FPS = 40    # maximum FPS. Increase if system capacity allows

FOV = 90
# player field of view. You can change it but the appearance of the game can be greatly distorted for the worse

TILE_SIZE = 100    # Size of the tiles that make up the playing field. Don't change
RAY_LENGTH = TILE_SIZE * 10     # maximum length of the ray
RAYS_AMOUNT = int(WIDTH / 15)   # must be a divider of 'WIDTH'
WALL_HEIGHT = int(HEIGHT * 0.8)    # height of the walls. Don't change
DISTANCE_TO_SCREEN = 100    # This is needed to calculate the distance to the wall. Don't change
SENSITIVITY = 0.3
# Mouse sensitivity (0.0 - 1.0). You can change it here, but it is also available in pause menu of the game
