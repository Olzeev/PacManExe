import pygame
import keyboard as key
from const import *
from math import sin, cos, atan, radians


time = 0
time_moving = 0
moving = False


class Field:
    def __init__(self):
        self.field = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.size_x = len(self.field[0])
        self.size_y = len(self.field)

    def draw_minimap(self, sc, player):
        for raw in range(self.size_x):
            for tile in range(self.size_y):
                if self.field[tile][raw] == 1:
                    pygame.draw.rect(sc, (255, 255, 255),
                                     (raw * TILE_SIZE, tile * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.draw.circle(sc, (255, 255, 255), (player.x, player.y), 5)
        pygame.draw.line(sc, (255, 0, 0), (player.x, player.y),
                         (player.x + 10 * cos(radians(player.angle)), player.y - 10 * sin(radians(player.angle))), 3)


class Player:
    def __init__(self, x, y, angle=0.1, speed=5, angle_speed=5):
        self.x, self.y = x, y
        self.angle = angle
        self.angle_speed = angle_speed
        self.speed = speed
        self.mouse_prev_x = WIDTH // 2

    def check_movements(self):
        global moving
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x != WIDTH // 2:
            self.angle -= (mouse_x - WIDTH // 2) * SENSITIVITY / 5
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

        moving_now = False

        if key.is_pressed('w'):
            self.x += self.speed * cos(radians(self.angle))
            self.y -= self.speed * sin(radians(self.angle))
            moving = True
            moving_now = True

        if key.is_pressed('a'):
            self.x += self.speed * cos(radians(self.angle + 90))
            self.y -= self.speed * sin(radians(self.angle + 90))
            moving = True
            moving_now = True

        if key.is_pressed('s'):
            self.x += self.speed * cos(radians(self.angle + 180))
            self.y -= self.speed * sin(radians(self.angle + 180))
            moving = True
            moving_now = True

        if key.is_pressed('d'):
            self.x += self.speed * cos(radians(self.angle - 90))
            self.y -= self.speed * sin(radians(self.angle - 90))
            moving = True
            moving_now = True

        if not moving_now:
            moving = False


class RayCaster:
    def draw(self, player, field, sc):
        pygame.draw.rect(sc, (100, 100, 100), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        angle0 = player.angle + FOV / 2
        angle_delta = FOV / RAYS_AMOUNT
        for ray_cur in range(RAYS_AMOUNT):
            angle_cur = angle0 - ray_cur * angle_delta
            ray_cur_length_total = RAY_LENGTH

            x_tile = player.x // TILE_SIZE * TILE_SIZE
            y_tile = player.y // TILE_SIZE * TILE_SIZE

            sin_a = sin(radians(angle_cur))
            cos_a = cos(radians(angle_cur))

            x_cur, delta_x = (x_tile, -1) if cos_a < 0 else (x_tile + TILE_SIZE, 1)
            y_cur, delta_y = (y_tile, -1) if sin_a > 0 else (y_tile + TILE_SIZE, 1)
            for i in range(0, field.size_x * TILE_SIZE, TILE_SIZE):
                dist_x = (x_cur - player.x) / cos_a
                y = player.y - dist_x * sin_a
                ind_x = int((x_cur + delta_x) // TILE_SIZE)
                ind_y = int(y // TILE_SIZE)
                if (ind_x < 0 or ind_x >= field.size_x or ind_y < 0 or ind_y >= field.size_y) or field.field[ind_y][ind_x] != 0:
                    break
                x_cur += delta_x * TILE_SIZE

            for i in range(0, field.size_y * TILE_SIZE, TILE_SIZE):
                dist_y = (player.y - y_cur) / sin_a
                x = player.x + dist_y * cos_a
                ind_x = int(x // TILE_SIZE)
                ind_y = int((y_cur + delta_y) // TILE_SIZE)
                if (ind_x < 0 or ind_x >= field.size_x or ind_y < 0 or ind_y >= field.size_y) or field.field[ind_y][ind_x] != 0:
                    break
                y_cur += delta_y * TILE_SIZE

            ray_cur_length_total = min(dist_x, dist_y)

            # pygame.draw.line(sc, (255, 0, 0), (player.x, player.y), (player.x + ray_cur_length_total * cos(radians(angle_cur)), player.y - ray_cur_length_total * sin(radians(angle_cur))))

            ray_cur_length_total *= cos(radians(abs(angle_cur - player.angle)))
            angle_in_screen_tan = (WALL_HEIGHT / 2) / ray_cur_length_total
            fragment_height = angle_in_screen_tan * DISTANCE_TO_SCREEN * 2
            fragment_x = ray_cur * WIDTH / RAYS_AMOUNT
            fragment_width = angle_delta / FOV * WIDTH

            k = max(RAY_LENGTH - ray_cur_length_total, 0) / RAY_LENGTH
            add_y = sin(time_moving / 5) * 30

            pygame.draw.rect(sc, (50 * k, 50 * k, 200 * k), (fragment_x, HEIGHT / 2 - fragment_height / 2 + add_y, fragment_width, fragment_height))


class App:
    def create_window(self):
        pygame.init()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def update_window(self):
        global time, time_moving
        pygame.display.flip()
        self.clock.tick(FPS)
        time += 1
        if moving:
            time_moving += 1

    def print_text(self, x, y, text, size, color):
        font = pygame.font.Font(None, size)
        surf = font.render(text, True, color)
        self.sc.blit(surf, (x, y))

    def main(self):
        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        field = Field()
        player = Player(200, 200)
        ray_caster = RayCaster()

        while self.run:
            self.check_events()
            player.check_movements()

            self.sc.fill((0, 0, 0))

            ray_caster.draw(player, field, self.sc)


            #field.draw_minimap(self.sc, player)
            self.print_text(0, 0, str(int(self.clock.get_fps())), 50, (255, 0, 0))
            self.update_window()


