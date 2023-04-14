import pygame
import keyboard as key
from const import *
from math import sin, cos, radians, degrees, atan2
import random

time = 0
time_moving = 0
moving = False
pause = False
pause_duration_counter = 0


def check_one_signed(a, b):
    if (a >= 0 and b >= 0) or (a <= 0 and b <= 0):
        return True
    return False


def dist_between_point(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class NPC:
    def __init__(self, x, y, sprite, angle=0.1, speed=4):
        self.x, self.y = x, y
        self.angle = angle
        self.sprite = sprite
        self.speed = speed
        self.hunt = False
        self.way_to_roam = (self.x // TILE_SIZE, self.y // TILE_SIZE)

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
                if 0 <= x2 < field.size_x and 0 <= y2 < field.size_y and field.field[y2][x2] != 1 and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

    def move(self, sc, field, player, raycaster):
        if dist_between_point(self.x, self.y, player.x, player.y) <= 500 or not raycaster.check_intersection(sc, field, self.x, self.y, player.x, player.y):
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

    def draw_minimap(self, sc, player, k=5):
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

        pygame.draw.circle(sc, (255, 255, 255), (player.x / k, player.y / k), 5)
        pygame.draw.line(sc, (255, 0, 0), (player.x / k, player.y / k),
                         (player.x / k + 10 * cos(radians(player.angle)), (player.y / k - 10 * sin(radians(player.angle)))), 3)


class Player:
    def __init__(self, x, y, angle=0.1, speed=5, angle_speed=5):
        self.x, self.y = x, y
        self.angle = angle
        self.angle_speed = angle_speed
        self.speed = speed
        self.mouse_prev_x = WIDTH // 2
        self.score = 0

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
                if field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] == 0:
                    self.score += 1
                    field.field[int(y1 // TILE_SIZE)][int(x1 // TILE_SIZE)] = -1
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('src/point_claim.wav'))

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


        if not moving_now:
            moving = False


class RayCaster:
    def draw(self, player, field, sc):
        pygame.draw.rect(sc, (100, 100, 100), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
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

            k = max(RAY_LENGTH - ray_cur_length_total, 0) / RAY_LENGTH
            add_y = sin(time_moving / 5) * 30
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
                if field.field[y][x] == self.digit_in_map:
                    sprite_x = x * TILE_SIZE + TILE_SIZE / 2
                    sprite_y = y * TILE_SIZE + TILE_SIZE / 2
                    if not ray_caster.check_intersection(sc, field, player.x, player.y, sprite_x, sprite_y):
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

                            if 0 <= sprite_pos_on_screen[0] < WIDTH and 0 <= sprite_pos_on_screen[1] < HEIGHT:
                                c = min(int(255 / dist * 50), 255)

                                to_draw.append(('circle', dist, (c, c, 0), sprite_pos_on_screen, fragment_height / 10))


                        '''
                        if cos_a_sprite <= 0:
                            angle_sprite = 180 - angle_sprite
                            if abs(angle_sprite - player.angle % 180) <= FOV / 2:
                                if angle_sprite >= player.angle % 180:
                                    sprite_x = (angle_sprite - player.angle % 180) / (FOV / 2) * (WIDTH / 2)
                                else:
                                    sprite_x = (player.angle % 180 - angle_sprite) / (FOV / 2) * (WIDTH / 2)
                        '''
        return to_draw

    def draw_npc(self, sc, field, player, ray_caster, NPC_s):
        to_draw = []
        for npc in NPC_s:
            if not ray_caster.check_intersection(sc, field, player.x, player.y, npc.x, npc.y):
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
                        to_draw.append(('sprite', dist, npc.sprite, sprite_pos_on_screen, fragment_height))

        return to_draw

    def draw(self, sc, field, player, ray_caster, NPC_s):
        if self.type == 'circle':
            return self.draw_circles(sc, field, player, ray_caster)
        elif self.type == 'npc':
            return self.draw_npc(sc, field, player, ray_caster, NPC_s)


class App:
    def create_window(self):
        pygame.init()
        pygame.mixer.init()
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

    def print_text(self, x, y, text, size, color, align='left'):
        font = pygame.font.Font(None, size)
        surf = font.render(text, True, color)
        if align == 'left':
            self.sc.blit(surf, (x, y))
        elif align == 'right':
            self.sc.blit(surf, (x - surf.get_width(), y))
        elif align == 'center':
            self.sc.blit(surf, (x - surf.get_width() / 2, y))

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
            color_delta1 = 100
        elif x >= WIDTH / 2 - 200 and x <= WIDTH / 2 + 200 and y >= HEIGHT / 2 + 80 and y <= HEIGHT / 2 + 180:
            color_delta2 = 100
        pygame.draw.rect(self.sc, (255 - color_delta1, 0, 0), (WIDTH / 2 - 200, HEIGHT / 2 - 120, 400, 100), border_radius=10)
        self.print_text(WIDTH / 2, HEIGHT / 2 - 100, 'Continue', 100, (255 - color_delta1, 255 - color_delta1, 255 - color_delta1), 'center')
        pygame.draw.rect(self.sc, (255 - color_delta2, 0, 0), (WIDTH / 2 - 200, HEIGHT / 2 + 80, 400, 100), border_radius=10)
        self.print_text(WIDTH / 2, HEIGHT / 2 + 100, 'Main menu', 100, (255 - color_delta2, 255 - color_delta2, 255 - color_delta2), 'center')

    def main(self):
        global pause
        pause = False
        pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        field = Field()
        player = Player(151, 151)
        ray_caster = RayCaster()
        NPC_s = [NPC(850, 950, pygame.image.load('src/ghosts/ghost1.png')),
                 NPC(900, 950, pygame.image.load('src/ghosts/ghost2.png')),
                 NPC(950, 950, pygame.image.load('src/ghosts/ghost3.png')),
                 NPC(1000, 950, pygame.image.load('src/ghosts/ghost4.png'))]

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
        pygame.mixer.Channel(0).set_volume(0.2)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('src/danger_theme.mp3'))
        pygame.mixer.Channel(1).set_volume(0)
        pygame.mixer.Channel(4).set_volume(0.2)
        pygame.mixer.Channel(4).play(pygame.mixer.Sound('src/pacman_sound.mp3'))
        pygame.mixer.Channel(5).play(pygame.mixer.Sound('src/opening.mp3'))
        while self.run:
            res = self.check_events()
            if res == 'exit':
                return res
            if player.score == 174:
                return 'win'
            if not pause:
                player.check_movements(field)

            self.sc.fill((0, 0, 0))
            to_draw = []
            to_draw += ray_caster.draw(player, field, self.sc)
            to_draw += self.draw_sprites(self.sc, field, player, sprites, ray_caster, NPC_s)
            to_draw = sorted(to_draw, key=lambda x: x[1], reverse=True)
            self.draw(to_draw)
            field.draw_minimap(self.sc, player)

            self.print_text(WIDTH / 2, 10, str(player.score), 70, (255, 255, 0), align='center')
            self.print_text(WIDTH - 10, 10, str(int(self.clock.get_fps())), 50, (255, 0, 0), align='right')

            hunt = False
            for npc in NPC_s:
                if dist_between_point(player.x, player.y, npc.x, npc.y) <= 70:
                    self.run = False
                    pygame.mixer.Channel(0).stop()
                    pygame.mixer.Channel(1).stop()
                    pygame.mixer.Channel(2).stop()
                    pygame.mixer.Channel(3).stop()
                    pygame.mixer.Channel(4).stop()
                    pygame.mixer.Channel(5).stop()
                    return 'lose'
                if npc.hunt:
                    hunt = True
                    npc.speed = 4
                else:
                    npc.speed = 2
                if not pause:
                    npc.move(self.sc, field, player, ray_caster)
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

            self.update_window()


def draw_buttons_main(sc):
    pygame.draw.rect(sc, (255, 255, 255), (100, 100, 400, 100))


app = App()

sc1 = pygame.display.set_mode((WIDTH, HEIGHT))
clock1 = pygame.time.Clock()

while True:
    player1 = Player(110, 110)
    player1.angle = -30.1
    field1 = Field()

    raycaster1 = RayCaster()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc1.fill((0, 0, 0))
        to_draw = raycaster1.draw(player1, field1, sc1)
        if key.is_pressed('enter'):
            break
        for el in to_draw:
            pygame.draw.rect(sc1, el[2], el[3])


        pygame.display.flip()
        clock1.tick(FPS)

    app.create_window()
    result = app.main()


