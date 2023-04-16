import pygame
pygame.init()
import keyboard as key
from const import *
from math import sin, cos, radians, degrees, atan2
import random

time = 0
time_moving = 0
moving = False
pause = False
pause_duration_counter = 0
score = 0
floor = pygame.transform.scale(pygame.image.load('src/floor.png'), (WIDTH, HEIGHT / 2))
level = 1


def check_one_signed(a, b):
    if (a >= 0 and b >= 0) or (a <= 0 and b <= 0):
        return True
    return False


def dist_between_point(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def print_text(sc, x, y, text, size, color, align='left', font=None):

    font = pygame.font.Font(font, size)
    surf = font.render(text, True, color)
    if align == 'left':
        sc.blit(surf, (x, y))
    elif align == 'right':
        sc.blit(surf, (x - surf.get_width(), y))
    elif align == 'center':
        sc.blit(surf, (x - surf.get_width() / 2, y))
    return surf


class NPC:
    def __init__(self, x, y, sprite, sprite_super, color, angle=0.1, speed=3+level / 5):
        self.x, self.y = x, y
        self.angle = angle
        self.sprite = sprite
        self.sprite_super = sprite_super
        self.speed = speed
        self.hunt = False
        self.way_to_roam = (self.x // TILE_SIZE, self.y // TILE_SIZE)
        self.color = color
        self.run_away = False

    def find_shortest_way(self, field, start, finish):  # made using BFS algorithm
        queue = [[start]]
        seen = {start}
        while queue:
            path = queue[0]
            queue = queue[1:len(queue)]
            x, y = path[-1]
            if y == finish[1] and x == finish[0]:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                x2 = int(x2)
                y2 = int(y2)
                if 0 <= x2 < field.size_x and 0 <= y2 < field.size_y and field.field[y2][x2] != 1 and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def move(self, sc, field, player, raycaster):
        if self.x // TILE_SIZE >= 8 and self.x // TILE_SIZE <= 10 and self.y // TILE_SIZE == 9:
            self.run_away = False
        if self.run_away and not (self.x // TILE_SIZE >= 8 and self.x // TILE_SIZE <= 10 and self.y // TILE_SIZE == 9):
            way = self.find_shortest_way(field, (self.x // TILE_SIZE, self.y // TILE_SIZE), (9, 9))
            if len(way) >= 2:
                x_to = way[1][0] * TILE_SIZE + TILE_SIZE / 2
                y_to = way[1][1] * TILE_SIZE + TILE_SIZE / 2

                if x_to > self.x:
                    self.x += 10
                elif x_to < self.x:
                    self.x -= 10

                if y_to > self.y:
                    self.y += 10
                elif y_to < self.y:
                    self.y -= 10
        elif (dist_between_point(self.x, self.y, player.x, player.y) <= 500 or not raycaster.check_intersection(sc, field, self.x, self.y, player.x, player.y)) and not player.super_mode:
            self.hunt = True
            way = self.find_shortest_way(field, (self.x // TILE_SIZE, self.y // TILE_SIZE), (player.x // TILE_SIZE, player.y // TILE_SIZE))

            if len(way) >= 2:
                x_to = way[1][0] * TILE_SIZE + TILE_SIZE / 2
                y_to = way[1][1] * TILE_SIZE + TILE_SIZE / 2

                if x_to > self.x:
                    self.x += self.speed
                elif x_to < self.x:
                    self.x -= self.speed

                if y_to > self.y:
                    self.y += self.speed
                elif y_to < self.y:
                    self.y -= self.speed

        else:
            if self.x // TILE_SIZE == self.way_to_roam[0] and self.y // TILE_SIZE == self.way_to_roam[1]:
                to_choose = []
                for x in range(field.size_x):
                    for y in range(field.size_y):
                        if field.field[y][x] == 0 or field.field[y][x] == -1:
                            to_choose.append((x, y))

                self.way_to_roam = random.choice(to_choose)

            else:

                way = self.find_shortest_way(field, (self.x // TILE_SIZE, self.y // TILE_SIZE), self.way_to_roam)
                x_to = way[1][0] * TILE_SIZE + TILE_SIZE / 2
                y_to = way[1][1] * TILE_SIZE + TILE_SIZE / 2

                if x_to > self.x:
                    self.x += self.speed
                elif x_to < self.x:
                    self.x -= self.speed

                if y_to > self.y:
                    self.y += self.speed
                elif y_to < self.y:
                    self.y -= self.speed

            self.hunt = False


class Field:
    def __init__(self):
        self.field = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.size_x = len(self.field[0])
        self.size_y = len(self.field)
        to_choose = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.field[y][x] == 0:
                    to_choose.append((x, y))
        for i in range(3):
            el = random.choice(to_choose)
            self.field[el[1]][el[0]] = 2

    def draw_minimap(self, sc, player, frames, k=5):
        for raw in range(self.size_x):
            for tile in range(self.size_y):
                dist_to_player = max((player.x // TILE_SIZE - raw) ** 2 + (player.y // TILE_SIZE - tile) ** 2, 1)
                if self.field[tile][raw] == 1:
                    pygame.draw.rect(sc, (0, 0, min(150 / dist_to_player, 150)),
                                     (raw * TILE_SIZE / k, tile * TILE_SIZE / k, TILE_SIZE / k, TILE_SIZE / k))
                else:
                    pygame.draw.rect(sc, (0, 0, min(50 / dist_to_player, 50)),
                                     (raw * TILE_SIZE / k, tile * TILE_SIZE / k, TILE_SIZE / k, TILE_SIZE / k))
                    if self.field[tile][raw] == 0:
                        pygame.draw.circle(sc, (min(255 / dist_to_player, 255), min(255 / dist_to_player, 255), 0), (raw * TILE_SIZE / k + TILE_SIZE / 2 / k, tile * TILE_SIZE / k + TILE_SIZE / 2 / k), TILE_SIZE / k / 5)
        ind = int(time / (FPS / 20)) % len(frames)
        sc.blit(pygame.transform.rotate(frames[ind], player.angle), (player.x / k - frames[ind].get_width() / 2, player.y / k - frames[ind].get_height() / 2))


class Player:
    def __init__(self, x, y, angle=0.1, speed=5, angle_speed=5):
        self.x, self.y = x, y
        self.angle = angle
        self.angle_speed = angle_speed
        self.speed = speed
        self.mouse_prev_x = WIDTH // 2
        self.score = 0
        self.score_super = 0
        self.super_mode = False
        self.super_mode_duration = 0

    def check_movements(self, field):
        global moving
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x != WIDTH // 2:
            self.angle -= (mouse_x - WIDTH // 2) * SENSITIVITY / 5
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

        moving_now = False

        if key.is_pressed('w'):
            x1 = self.x + self.speed * cos(radians(self.angle))
            y1 = self.y - self.speed * sin(radians(self.angle))
            if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] != 1 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                self.x = x1
                self.y = y1
                moving = True
                moving_now = True
                if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 0 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (
                        y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.score += 1
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/point_claim.wav'))
                elif field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 2 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.super_mode = True
                    self.super_mode_duration = 0
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/bonus_claim.wav'))

        if key.is_pressed('a'):
            x1 = self.x + self.speed * cos(radians(self.angle + 90))
            y1 = self.y - self.speed * sin(radians(self.angle + 90))
            if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] != 1:
                self.x = x1
                self.y = y1
                moving = True
                moving_now = True
                if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 0 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.score += 1
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/point_claim.wav'))
                elif field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 2 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.super_mode = True
                    self.super_mode_duration = 0
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/bonus_claim.wav'))

        if key.is_pressed('s'):
            x1 = self.x + self.speed * cos(radians(self.angle + 180))
            y1 = self.y - self.speed * sin(radians(self.angle + 180))
            if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] != 1:
                self.x = x1
                self.y = y1
                moving = True
                moving_now = True
                if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 0 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.score += 1
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/point_claim.wav'))
                elif field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 2 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.super_mode = True
                    self.super_mode_duration = 0
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/bonus_claim.wav'))

        if key.is_pressed('d'):
            x1 = self.x + self.speed * cos(radians(self.angle - 90))
            y1 = self.y - self.speed * sin(radians(self.angle - 90))
            if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] != 1:
                self.x = x1
                self.y = y1
                moving = True
                moving_now = True
                if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 0 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.score += 1
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/point_claim.wav'))
                elif field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 2 and \
                        (x1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - x1) ** 2 + (y1 // TILE_SIZE * TILE_SIZE + TILE_SIZE / 2 - y1) ** 2 <= TILE_SIZE ** 2:
                    self.super_mode = True
                    self.super_mode_duration = 0
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/bonus_claim.wav'))


        if not moving_now:
            moving = False


class RayCaster:
    def draw(self, player, field, sc):
        add_y = sin(time_moving / 5) * 30
        sc.blit(floor, (0, HEIGHT / 2))

        angle0 = player.angle + FOV / 2
        angle_delta = FOV / RAYS_AMOUNT
        to_draw = []
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
                if (ind_x < 0 or ind_x >= field.size_x or ind_y < 0 or ind_y >= field.size_y) or field.field[ind_y][ind_x] == 1:
                    break
                x_cur += delta_x * TILE_SIZE

            for i in range(0, field.size_y * TILE_SIZE, TILE_SIZE):
                dist_y = (player.y - y_cur) / sin_a
                x = player.x + dist_y * cos_a
                ind_x = int(x // TILE_SIZE)
                ind_y = int((y_cur + delta_y) // TILE_SIZE)
                if (ind_x < 0 or ind_x >= field.size_x or ind_y < 0 or ind_y >= field.size_y) or field.field[ind_y][ind_x] == 1:
                    break
                y_cur += delta_y * TILE_SIZE

            ray_cur_length_total = min(dist_x, dist_y)

            # pygame.draw.line(sc, (255, 0, 0), (player.x, player.y), (player.x + ray_cur_length_total * cos(radians(angle_cur)), player.y - ray_cur_length_total * sin(radians(angle_cur))))

            ray_cur_length_total *= cos(radians(abs(angle_cur - player.angle)))
            angle_in_screen_tan = (WALL_HEIGHT / 2) / ray_cur_length_total
            fragment_height = angle_in_screen_tan * DISTANCE_TO_SCREEN * 2
            fragment_x = ray_cur * WIDTH / RAYS_AMOUNT
            fragment_width = angle_delta / FOV * WIDTH

            k = min(max(RAY_LENGTH - ray_cur_length_total, 0) / (RAY_LENGTH + 500), 1)

            to_draw.append(('rect', ray_cur_length_total, (50 * k, 50 * k, 200 * k), (fragment_x, HEIGHT / 2 - fragment_height / 2 + add_y, fragment_width, fragment_height)))

        return to_draw

    def check_intersection(self, sc, field, x1, y1, x2, y2):
        dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        cos_a = (x2 - x1) / dist
        sin_a = (y1 - y2) / dist
        for i in range(int(dist)):
            x = int((x1 + i * cos_a) // TILE_SIZE)
            y = int((y1 - i * sin_a) // TILE_SIZE)
            if field.field[y][x] == 1:
                return True
        return False


class Sprite:
    def __init__(self, digit_on_map, type):

        self.digit_in_map = digit_on_map
        self.type = type

    def draw_circles(self, sc, field, player, ray_caster):
        to_draw = []
        for x in range(field.size_x):
            for y in range(field.size_y):
                if field.field[y][x] == 0 or field.field[y][x] == 2:
                    sprite_x = x * TILE_SIZE + TILE_SIZE / 2
                    sprite_y = y * TILE_SIZE + TILE_SIZE / 2
                    if dist_between_point(sprite_x, sprite_y, player.x, player.y) <= 800:
                        dist = ((player.x - (x * TILE_SIZE + TILE_SIZE / 2)) ** 2 + (player.y - (y * TILE_SIZE + TILE_SIZE / 2)) ** 2) ** 0.5
                        angle_p = player.angle % 360
                        dx, dy = x * TILE_SIZE + TILE_SIZE / 2 - player.x, player.y - y * TILE_SIZE - TILE_SIZE / 2

                        theta = degrees(atan2(dy, dx))
                        gamma = theta - angle_p
                        if dx > 0 and 180 <= angle_p <= 360 or dx < 0 and dy < 0:
                            gamma += 360

                        angle_delta = FOV / RAYS_AMOUNT
                        delta_rays = int(gamma / angle_delta)
                        center_ray = RAYS_AMOUNT // 2 - 1
                        current_ray = center_ray + delta_rays
                        dist *= cos(radians(FOV / 2 - current_ray * angle_delta))

                        if 0 <= current_ray <= RAYS_AMOUNT - 1:
                            angle_in_screen_tan = (WALL_HEIGHT / 2) / dist
                            fragment_height = angle_in_screen_tan * DISTANCE_TO_SCREEN * 2
                            shift = fragment_height / 2 * 1.4

                            add_y = sin(time_moving / 5) * 30
                            sprite_pos_on_screen = (WIDTH - current_ray * (WIDTH // RAYS_AMOUNT), HEIGHT / 2 - fragment_height / 2 + shift + add_y)
                            c = min(int(255 / dist * 50), 255)
                            if 0 <= sprite_pos_on_screen[0] < WIDTH and 0 <= sprite_pos_on_screen[1] < HEIGHT:
                                if field.field[y][x] == 0:
                                    color = (c, c, 0)
                                    to_draw.append(('circle', dist, color, sprite_pos_on_screen, fragment_height / 10))
                                elif field.field[y][x] == 2:
                                    color = (c, 0, 0)
                                    to_draw.append(('circle', dist, color, sprite_pos_on_screen, fragment_height / 7))

        return to_draw

    def draw_npc(self, sc, field, player, ray_caster, NPC_s):
        to_draw = []
        for npc in NPC_s:

            dist = ((player.x - npc.x) ** 2 + (
                        player.y - npc.y) ** 2) ** 0.5
            angle_p = player.angle % 360
            dx, dy = npc.x - player.x, player.y - npc.y

            theta = degrees(atan2(dy, dx))
            gamma = theta - angle_p
            if dx > 0 and 180 <= angle_p <= 360 or dx < 0 and dy < 0:
                gamma += 360

            angle_delta = FOV / RAYS_AMOUNT
            delta_rays = int(gamma / angle_delta)
            center_ray = RAYS_AMOUNT // 2 - 1
            current_ray = center_ray + delta_rays
            dist *= cos(radians(FOV / 2 - current_ray * angle_delta))

            if 0 <= current_ray <= RAYS_AMOUNT - 1:
                angle_in_screen_tan = (WALL_HEIGHT / 2) / dist
                fragment_height = angle_in_screen_tan * DISTANCE_TO_SCREEN * 2
                shift = 0

                add_y = sin(time_moving / 5) * 30
                sprite_pos_on_screen = (WIDTH - current_ray * (WIDTH // RAYS_AMOUNT) - fragment_height / 2, HEIGHT / 2 - fragment_height / 2 + shift + add_y)

                if 0 <= sprite_pos_on_screen[0] < WIDTH and 0 <= sprite_pos_on_screen[1] < HEIGHT:
                    c = min(int(255 / dist * 50), 255)
                    if not player.super_mode:
                        to_draw.append(('sprite', dist, npc.sprite, sprite_pos_on_screen, fragment_height))
                    else:
                        to_draw.append(('sprite', dist, npc.sprite_super, sprite_pos_on_screen, fragment_height))

        return to_draw

    def draw(self, sc, field, player, ray_caster, NPC_s):
        if self.type == 'circle':
            return self.draw_circles(sc, field, player, ray_caster)
        elif self.type == 'npc':
            return self.draw_npc(sc, field, player, ray_caster, NPC_s)


class App:
    def create_window(self):
        WIDTH = pygame.display.Info().current_w
        HEIGHT = pygame.display.Info().current_h
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.run = True
        self.beat_duration = 100
        self.beat_duration_counter = 0
        self.danger_volume = 0


    def check_events(self):
        global pause, pause_duration_counter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = event.pos

                if pause:
                    if x >= WIDTH / 2 - 200 and x <= WIDTH / 2 + 200 and y >= HEIGHT / 2 - 120 and y <= HEIGHT / 2 - 30:
                        pause = False
                        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    elif x >= WIDTH / 2 - 200 and x <= WIDTH / 2 + 200 and y >= HEIGHT / 2 + 80 and y <= HEIGHT / 2 + 180:
                        self.run = False
                        pygame.mixer.Channel(0).stop()
                        pygame.mixer.Channel(1).stop()
                        pygame.mixer.Channel(2).stop()
                        pygame.mixer.Channel(3).stop()
                        pygame.mixer.Channel(4).stop()
                        pygame.mixer.Channel(5).stop()
                        return 'exit'
                    elif x >= WIDTH / 2 - 96 and x <= WIDTH / 2 + 96 and y >= HEIGHT / 2 + 304 and y <= HEIGHT / 2 + 346:
                        global SENSITIVITY
                        SENSITIVITY = (x - (WIDTH / 2 - 96)) / 192


        if key.is_pressed('esc') and pause_duration_counter >= 20:
            pause = not pause
            pause_duration_counter = 0
            if pause:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            else:
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))


    def update_window(self):
        global time, time_moving, pause_duration_counter
        pygame.display.flip()
        self.clock.tick(FPS)
        time += 1
        if moving:
            time_moving += 1
        self.beat_duration_counter += 1
        pygame.mixer.Channel(1).set_volume(self.danger_volume)
        #if self.danger_volume:
        #    pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/danger_theme.mp3'))
        if self.beat_duration_counter >= self.beat_duration:
            if not pause:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound('src/heart_beat.wav'))
            self.beat_duration_counter = 0

        pygame.mixer.Channel(2).set_volume(max(1 - self.danger_volume * 2, 0))

        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/danger_theme.mp3'))

        pause_duration_counter += 1

    def draw_sprites(self, sc, field, player, sprites, ray_caster, NPC_s):
        ans = []
        for sprite in sprites:
            ans += sprite.draw(self.sc, field, player, ray_caster, NPC_s)
        return ans

    def draw(self, to_draw):
        for el in to_draw:
            if el[0] == 'circle':
                pygame.draw.circle(self.sc, el[2], el[3], el[4])
            elif el[0] == 'rect':
                pygame.draw.rect(self.sc, el[2], el[3])
            elif el[0] == 'sprite':
                self.sc.blit(pygame.transform.scale(el[2], (el[4], el[4])), el[3])

    def draw_pause(self):
        x, y = pygame.mouse.get_pos()
        color_delta1 = 0
        color_delta2 = 0
        if x >= WIDTH / 2 - 200 and x <= WIDTH / 2 + 200 and y >= HEIGHT / 2 - 120 and y <= HEIGHT / 2 - 20:
            color_delta1 = 50
        elif x >= WIDTH / 2 - 200 and x <= WIDTH / 2 + 200 and y >= HEIGHT / 2 + 80 and y <= HEIGHT / 2 + 180:
            color_delta2 = 50
        pygame.draw.rect(self.sc, (180 - color_delta1, 0, 0), (WIDTH / 2 - 200, HEIGHT / 2 - 120, 400, 100), border_radius=10)
        print_text(self.sc, WIDTH / 2, HEIGHT / 2 - 100, 'Continue', 60, (255 - color_delta1, 255 - color_delta1, 255 - color_delta1), align='center', font='src/font3.ttf')
        pygame.draw.rect(self.sc, (180 - color_delta2, 0, 0), (WIDTH / 2 - 200, HEIGHT / 2 + 80, 400, 100), border_radius=10)
        print_text(self.sc, WIDTH / 2, HEIGHT / 2 + 100, 'Main menu', 60, (255 - color_delta2, 255 - color_delta2, 255 - color_delta2), align='center', font='src/font3.ttf')
        print_text(self.sc, WIDTH / 2, HEIGHT / 2 + 250, 'Sensitivity', 30,
                   (255, 255, 255), align='center', font='src/font3.ttf')
        pygame.draw.rect(self.sc, (255, 255, 255), (WIDTH / 2 - 100, HEIGHT / 2 + 300, 200, 50), 2)
        pygame.draw.rect(self.sc, (255, 255, 255), (WIDTH / 2 - 96, HEIGHT / 2 + 304, 192 * SENSITIVITY, 42))

    def main(self):
        global pause, score
        pause = False
        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        field = Field()
        player = Player(151, 151)
        ray_caster = RayCaster()
        NPC_s = [NPC(850, 950, pygame.image.load('src/ghosts/ghost1.png'), pygame.image.load('src/ghosts/ghost1_super.png'), 'red'),
                 NPC(900, 950, pygame.image.load('src/ghosts/ghost2.png'), pygame.image.load('src/ghosts/ghost2_super.png'), 'blue'),
                 NPC(950, 950, pygame.image.load('src/ghosts/ghost3.png'), pygame.image.load('src/ghosts/ghost3_super.png'), 'yellow'),
                 NPC(1000, 950, pygame.image.load('src/ghosts/ghost4.png'), pygame.image.load('src/ghosts/ghost4_super.png'), 'pink')]
        minimap_frames = [
            pygame.transform.scale(pygame.image.load('src/pacman/frame1.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame2.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame3.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame4.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame5.png'),  (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame4.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame3.png'), (20, 20)),
            pygame.transform.scale(pygame.image.load('src/pacman/frame2.png'), (20, 20)),
        ]

        sprites = [Sprite(0, 'circle'),
                   Sprite(None, 'npc')]
        background_sounds = [
            pygame.mixer.Sound('src/background_audio/1.oga'),
            pygame.mixer.Sound('src/background_audio/2.oga'),
            pygame.mixer.Sound('src/background_audio/3.oga'),
            pygame.mixer.Sound('src/background_audio/4.oga'),
            pygame.mixer.Sound('src/background_audio/5.oga'),
            pygame.mixer.Sound('src/background_audio/6.oga'),
            pygame.mixer.Sound('src/background_audio/7.oga'),
            pygame.mixer.Sound('src/background_audio/8.oga'),
            pygame.mixer.Sound('src/background_audio/9.ogg')
        ]
        pygame.mixer.Channel(0).set_volume(0.05)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/danger_theme.mp3'))
        pygame.mixer.Channel(1).set_volume(0)
        pygame.mixer.Channel(4).set_volume(0.1)
        pygame.mixer.Channel(4).play(pygame.mixer.Sound('src/pacman_sound.mp3'))
        pygame.mixer.Channel(5).set_volume(1)
        pygame.mixer.Channel(5).play(pygame.mixer.Sound('src/opening.mp3'))
        pygame.mixer.Channel(6).set_volume(0.2)
        global score
        while self.run:
            res = self.check_events()
            if res == 'exit':
                return res
            if player.score == 171:
                pygame.mixer.Channel(0).stop()
                pygame.mixer.Channel(1).stop()
                pygame.mixer.Channel(2).stop()
                pygame.mixer.Channel(3).stop()
                pygame.mixer.Channel(4).stop()
                pygame.mixer.Channel(5).stop()

                score = player.score + player.score_super
                return 'win'
            if not pause:
                player.check_movements(field)

            self.sc.fill((0, 0, 0))
            to_draw = []
            to_draw += ray_caster.draw(player, field, self.sc)
            to_draw += self.draw_sprites(self.sc, field, player, sprites, ray_caster, NPC_s)
            to_draw = sorted(to_draw, key=lambda x: x[1], reverse=True)
            self.draw(to_draw)
            field.draw_minimap(self.sc, player, minimap_frames)

            print_text(self.sc, WIDTH / 2, 10, str(player.score + player.score_super), 70, (255, 255, 0), align='center', font='src/font2.ttf')
            print_text(self.sc, WIDTH - 10, 10, str(int(self.clock.get_fps())), 50, (255, 0, 0), align='right')

            hunt = False
            for npc in NPC_s:
                if dist_between_point(player.x, player.y, npc.x, npc.y) <= 70:
                    if not player.super_mode:
                        self.run = False
                        pygame.mixer.Channel(0).stop()
                        pygame.mixer.Channel(1).stop()
                        pygame.mixer.Channel(2).stop()
                        pygame.mixer.Channel(3).stop()
                        pygame.mixer.Channel(4).stop()
                        pygame.mixer.Channel(5).stop()

                        score = player.score + player.score_super
                        return ('lose', npc.color)
                    else:
                        pygame.mixer.Channel(6).play(pygame.mixer.Sound('src/catch.wav'))
                        if not npc.run_away:
                            player.score_super += 10
                        npc.run_away = True
                        npc.speed = 4
                elif npc.hunt:
                    hunt = True
                    npc.speed = 4 + level / 5
                else:
                    npc.speed = 2
                if not pause:
                    npc.move(self.sc, field, player, ray_caster)
                if player.super_mode:
                    pygame.draw.circle(self.sc, (255, 0, 0), (npc.x / 5, npc.y / 5), 10)

            if hunt:
                self.danger_volume = max(self.danger_volume, 0.02)
                self.danger_volume *= 1.07
            else:
                self.danger_volume = min(self.danger_volume, 1)
                self.danger_volume /= 1.07

            dist = None
            for npc in NPC_s:
                if dist is not None:
                    dist = min(dist, dist_between_point(player.x, player.y, npc.x, npc.y))
                else:
                    dist = dist_between_point(player.x, player.y, npc.x, npc.y)
            self.beat_duration = max(dist / 12, 20)

            if random.randint(1, 300) == 1 and not pygame.mixer.Channel(2).get_busy():
                pygame.mixer.Channel(2).play(random.choice(background_sounds))
            if moving:
                pygame.mixer.Channel(4).unpause()
            else:
                pygame.mixer.Channel(4).pause()
            if not pygame.mixer.Channel(4).get_busy():
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('src/pacman_sound.mp3'))

            if pause:
                self.draw_pause()
            player.super_mode_duration += 1
            if player.super_mode_duration >= FPS * 10:
                player.super_mode = False
            self.update_window()


def draw_buttons_main(sc, color1, color2):
    print_text(sc1, WIDTH * 0.75, 100, 'Menu', 100, (255, 255, 255), font='src/font1.ttf')
    #pygame.draw.rect(sc, (255, 255, 255), (WIDTH * 0.75, 300, 130, 60), 2)
    print_text(sc1, WIDTH * 0.75, 300, 'Start', 80, color1, font='src/font2.ttf')
    print_text(sc1, WIDTH * 0.75 + 150, 320, f'Level {level}', 50, (180, 180, 180), font='src/font2.ttf')
    #pygame.draw.rect(sc, (255, 255, 255), (WIDTH * 0.75, 400, 120, 60), 2)
    print_text(sc1, WIDTH * 0.75, 400, 'Quit', 80, color2, font='src/font2.ttf')


def draw_main_menu():

    player1 = Player(110, 110)
    player1.angle = -30.1
    field1 = Field()
    bg = pygame.transform.scale(pygame.image.load('src/main_menu_bg.png'), (WIDTH, HEIGHT))
    manual = pygame.transform.scale(pygame.image.load('src/manual.png'), (300, 411))
    raycaster1 = RayCaster()
    run = True
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/background_music.mp3'))
    pygame.mixer.Channel(0).set_volume(0.2)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= WIDTH * 0.75 and x <= WIDTH * 0.75 + 130 and y >= 300 and y <= 360:
                    run = False
                    pygame.mixer.Channel(0).stop()
                elif x >= WIDTH * 0.75 and x <= WIDTH * 0.75 + 120 and y >= 400 and y <= 460:
                    exit()
        sc1.blit(bg, (0, 0))

        print_text(sc1, WIDTH * 0.2, 120, 'PacMan', 100, (190, 190, 50), font='src/font4.ttf')
        print_text(sc1, WIDTH * 0.2 + 310, 120, '.exe', 100, (190, 0, 0), font='src/font4.ttf')
        print_text(sc1, WIDTH * 0.3, HEIGHT - 200, 'Collect all the points in this dark maze', 30, (150, 150, 150), align='center', font='src/font2.ttf')
        print_text(sc1, WIDTH * 0.3, HEIGHT - 150, 'Beware of ghosts. Heartbeat will tell you how far they are', 30, (150, 150, 150), align='center', font='src/font2.ttf')

        color1 = (255, 0, 0)
        color2 = (255, 0, 0)
        x, y = pygame.mouse.get_pos()
        if x >= WIDTH * 0.75 and x <= WIDTH * 0.75 + 130 and y >= 300 and y <= 360:
            color1 = (180, 0, 0)
        if x >= WIDTH * 0.75 and x <= WIDTH * 0.75 + 120 and y >= 400 and y <= 460:
            color2 = (180, 0, 0)

        draw_buttons_main(sc1, color1, color2)
        sc1.blit(manual, (WIDTH - 500, HEIGHT - 500))
        pygame.display.flip()
        clock1.tick(FPS)


def draw_screamer(color):
    pygame.mixer.Channel(0).set_volume(0.4)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/screamer.mp3'))
    delta_y = 200

    if color == 'red':
        image = pygame.image.load('src/ghosts/ghost1.png')
    elif color == 'blue':
        image = pygame.image.load('src/ghosts/ghost2.png')
    elif color == 'yellow':
        image = pygame.image.load('src/ghosts/ghost3.png')
    else:
        image = pygame.image.load('src/ghosts/ghost4.png')
    image = pygame.transform.scale(image, (HEIGHT, HEIGHT))
    bg = pygame.transform.scale(pygame.image.load('src/screamer_bg.png'), (WIDTH, HEIGHT))
    size = HEIGHT
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        sc1.blit(bg, (0, 0))

        sc1.blit(image, (WIDTH // 2 - image.get_width() // 2 + random.randint(-50, 50) * (delta_y / 200), delta_y - 200))
        image = pygame.transform.scale(image, (size, size))
        delta_y *= 0.95
        size += 10 * (delta_y / 200)
        if delta_y <= 1:
            run = False
        pygame.display.flip()
        clock1.tick(FPS)


def draw_lose_screen():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= WIDTH / 2 - 150 and x <= WIDTH / 2 + 150 and y >= HEIGHT - 200 and y <= HEIGHT - 100:
                    run = False

        sc1.fill((0, 0, 0))

        print_text(sc1, WIDTH / 2, 150, 'Game Over', 100, (180, 0, 0), align='center', font='src/font3.ttf')
        print_text(sc1, WIDTH / 2, HEIGHT / 2 - 50, 'Score ' + str(score), 100, (200, 0, 0), align='center', font='src/font2.ttf')

        x, y = pygame.mouse.get_pos()
        delta_color = 0
        if x >= WIDTH / 2 - 150 and x <= WIDTH / 2 + 150 and y >= HEIGHT - 200 and y <= HEIGHT - 100:
            delta_color = 50
        print_text(sc1, WIDTH / 2, HEIGHT - 200, 'Continue', 100, (180 - delta_color, 180 - delta_color, 180 - delta_color), align='center', font='src/font2.ttf')

        pygame.display.flip()
        clock1.tick(FPS)


def draw_win_screen():
    run = True
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x >= WIDTH / 2 - 150 and x <= WIDTH / 2 + 150 and y >= HEIGHT - 200 and y <= HEIGHT - 100:
                    run = False

        sc1.fill((0, 0, 0))

        print_text(sc1, WIDTH / 2, 150, 'Game complete', 100, (200, 200, 200), align='center', font='src/font3.ttf')
        print_text(sc1, WIDTH / 2 - 200, HEIGHT / 2 - 50, 'Time:', 100, (200, 0, 0), align='left', font='src/font4.ttf')
        surf = print_text(sc1, WIDTH / 2 + 20, HEIGHT / 2 - 50, str(time // FPS // 60), 100, (180, 180, 180),
                   align='left', font='src/font4.ttf')
        print_text(sc1, WIDTH / 2 + 20 + surf.get_width() + 10, HEIGHT / 2 - 50, 'm', 100, (200, 0, 0),
                   align='left', font='src/font4.ttf')
        surf1 = print_text(sc1, WIDTH / 2 + 120 + surf.get_width(), HEIGHT / 2 - 50, str((time // FPS) % 60), 100, (180, 180, 180),
                   align='left', font='src/font4.ttf')
        print_text(sc1, WIDTH / 2 + 140 + surf.get_width() + surf1.get_width(), HEIGHT / 2 - 50, 's', 100, (200, 0, 0),
                   align='left', font='src/font4.ttf')

        print_text(sc1, WIDTH / 2, HEIGHT / 2 + 150, f'score {score}', 100, (200, 0, 0),
                   align='center', font='src/font2.ttf')

        x, y = pygame.mouse.get_pos()
        delta_color = 0
        if x >= WIDTH / 2 - 150 and x <= WIDTH / 2 + 150 and y >= HEIGHT - 200 and y <= HEIGHT - 100:
            delta_color = 50
        print_text(sc1, WIDTH / 2, HEIGHT - 200, 'Continue', 100, (180 - delta_color, 180 - delta_color, 180 - delta_color), align='center', font='src/font2.ttf')

        pygame.display.flip()
        clock1.tick(FPS)


app = App()

sc1 = pygame.display.set_mode((WIDTH, HEIGHT))
clock1 = pygame.time.Clock()

result = None

while True:


    pygame.mixer.init()
    if result is None or result == 'exit':
        draw_main_menu()
    elif type(result) == tuple:
        level = 1
        draw_screamer(result[1])
        draw_lose_screen()
        draw_main_menu()
    else:
        level += 1
        draw_win_screen()
        draw_main_menu()


    app.create_window()
    result = app.main()


