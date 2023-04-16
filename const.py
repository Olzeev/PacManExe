import pygame.display

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FPS = 60

FOV = 90
TILE_SIZE = 100
RAY_LENGTH = TILE_SIZE * 10
RAYS_AMOUNT = int(WIDTH / 15)
WALL_HEIGHT = int(HEIGHT * 0.8)
DISTANCE_TO_SCREEN = 100
SENSITIVITY = 0.3
