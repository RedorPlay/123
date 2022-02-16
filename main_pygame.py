import pygame
import os
from QT_window import MyWidget
from PyQt5.QtWidgets import QApplication, QPushButton
import sys

FPS = 50

pygame.init()
size = width, height = 1000, 700
screen = pygame.display.set_mode(size)

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
results_group = pygame.sprite.Group()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scree):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (self.cell_size * j + self.left,
                                                               self.cell_size * i + self.top,
                                                               self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (self.cell_size * j + self.left,
                                                               self.cell_size * i + self.top,
                                                               self.cell_size, self.cell_size))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, player_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_level(filename):
    # filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    players = []
    enemies = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == ',':
                Tile('snow', x, y)
            elif level[y][x] == '@':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Champion(x, y))
                else:
                    enemies.append(Champion(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)
            elif level[y][x] == '1':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Greendragon(x, y))
                else:
                    enemies.append(Greendragon(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)

            elif level[y][x] == '2':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Catapult(x, y))
                else:
                    enemies.append(Catapult(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)

            elif level[y][x] == '3':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Wolf(x, y))
                else:
                    enemies.append(Wolf(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)

            elif level[y][x] == '4':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Skeleton(x, y))
                else:
                    enemies.append(Skeleton(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)
            elif level[y][x] == '5':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Ghost(x, y))
                else:
                    enemies.append(Ghost(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)
            elif level[y][x] == '6':
                if ex.true_3:
                    Tile('snow', x, y)
                else:
                    Tile('grass', x, y)
                if x < 5:
                    players.append(Hydra(x, y))
                else:
                    enemies.append(Hydra(x, y))
                    enemies[-1].image = pygame.transform.flip(enemies[-1].image, True, False)
    return players, enemies, x, y


def terminate():
    pygame.quit()
    sys.exit()


tile_images = {
    'snow': load_image('snow.png'),
    'grass': load_image('grass.png')
}

tile_width = tile_height = 70


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Champion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("champion.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Knight'
        self.damage = 75
        self.hp = 100
        self.agility = 5

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("champion_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('champion.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Hydra(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("hydra.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Hydra'
        self.damage = 100
        self.hp = 200
        self.agility = 3

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("hydra_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('hydra.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("skeleton.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Skeleton'
        self.damage = 30
        self.hp = 75
        self.agility = 5

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("skeleton_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('skeleton.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("ghost.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Skeleton'
        self.damage = 50
        self.hp = 75
        self.agility = 5

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("ghost_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('ghost.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Greendragon(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("greendragon.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Dragon'
        self.damage = 150
        self.hp = 300
        self.agility = 3

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("greendragon_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('greendragon.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("wolf.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.name = 'Wolf'
        self.damage = 50
        self.hp = 50
        self.agility = 10

    def animation_fight(self):
        if ex.true_3:
            self.image = load_image('snow.png', -1)
        else:
            self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("wolf_fight.png", -1), 4, 1, self.rect.x, self.rect.y)
        for _ in range(3):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(30)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('wolf.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


class Catapult(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("catapult.png", -1)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.damage = 50
        self.hp = 100
        self.agility = 0

    def animation_fight(self):
        self.image = load_image('grass.png', -1)
        a = AnimatedSprite(load_image("catapult_fight.png", -1), 3, 3, self.rect.x, self.rect.y)
        for _ in range(8):
            a.update()
            if i < len(d):
                if d[i] == 1 and not fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            if i < len(d_1):
                if d_1[i] == 1 and fl:
                    a.image = pygame.transform.flip(a.image, True, False)
            player_group.draw(screen)
            clock.tick(10)
            pygame.display.flip()
        all_sprites.remove(a)
        player_group.remove(a)
        self.image = load_image('catapult.png', -1)
        if i < len(d):
            if d[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        if i < len(d_1):
            if d_1[i] == 1 and fl:
                self.image = pygame.transform.flip(self.image, True, False)
        all_sprites.draw(screen)


start = True
abc = pygame.mixer.Sound('data/01 - Main Menu.mp3')
abc.play()
abc.set_volume(0.25)
while start:
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('start.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("    Play    ", True, pygame.Color('#D2691E'))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2 - 100
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('#2F4F4F'), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 5)
    true = True

    while true:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start = False
                true = False

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
size = width, height = 700, 700
screen = pygame.display.set_mode(size)
board = Board(10, 10)
board.set_view(0, 0, 70)
run = True
clock = pygame.time.Clock()
players = []
enemies = []
results = [[], []]
players, enemies, level_x, level_y = generate_level(load_level('data/map.txt'))
fl = 0
d = [0] * len(players)
d_1 = [1] * len(enemies)
i = 0
all_sprites.draw(screen)
fl_3 = 0
players += [Champion(0, 0)]
enemies += [Champion(0, 0)]
while run and len(players) > 0 and len(enemies) > 0:
    if fl == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b = event.pos
                x1 = b[0] // board.cell_size
                y1 = b[1] // board.cell_size
                c = 0
                pos_x = players[i].rect.x
                t = 0
                if x1 * board.cell_size < pos_x and d[i] == 0:
                    players[i].image = pygame.transform.flip(players[i].image, True, False)
                    d[i] = 1
                elif x1 * board.cell_size > pos_x and d[i] == 1:
                    players[i].image = pygame.transform.flip(players[i].image, True, False)
                    d[i] = 0
                k = 0
                while c != abs(x1 * board.cell_size - pos_x) and k <= players[i].agility - 1 / 70:
                    c += 1
                    k += 1 / 70
                    if x1 * board.cell_size > pos_x:
                        t = 1
                        players[i].rect.x += 1
                        if len(pygame.sprite.spritecollide(players[i], player_group, False)) > 1:
                            players[i].rect.x -= 1
                    else:
                        t = 2
                        players[i].rect.x -= 1
                        if len(pygame.sprite.spritecollide(players[i], player_group, False)) > 1:
                            players[i].rect.x += 1
                    clock.tick(150)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                c = 0
                pos_y = players[i].rect.y
                while c != abs(y1 * board.cell_size - pos_y) and k <= players[i].agility - 1 / 70:
                    c += 1
                    k += 1 / 70
                    if y1 * board.cell_size > pos_y:
                        t = 1
                        players[i].rect.y += 1
                        if len(pygame.sprite.spritecollide(players[i], player_group, False)) > 1:
                            players[i].rect.y -= 1
                    else:
                        t = 2
                        players[i].rect.y -= 1
                        if len(pygame.sprite.spritecollide(players[i], player_group, False)) > 1:
                            players[i].rect.y += 1
                    clock.tick(150)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                zaglushka = 0
                posx = event.pos[0] // board.cell_size * board.cell_size
                posy = event.pos[1] // board.cell_size * board.cell_size
                for j in range(len(enemies)):
                    if (enemies[j].rect.x == posx or enemies[j].rect.x - 1 == posx) \
                            and (enemies[j].rect.y == posy or enemies[j].rect.y - 1 == posy) \
                            and abs(players[i].rect.x - enemies[j].rect.x) <= 70 \
                            and abs(players[i].rect.y - enemies[j].rect.y) <= 70:
                        zaglushka = 1
                    elif isinstance(players[i], Catapult) and (enemies[j].rect.x == posx or enemies[j].rect.x - 1 == posx) \
                            and (enemies[j].rect.y == posy or enemies[j].rect.y - 1 == posy):
                        zaglushka = 1
                if zaglushka:
                    players[i].animation_fight()
                    for j in range(len(enemies)):
                        if (enemies[j].rect.x == posx or enemies[j].rect.x - 1 == posx) \
                                and (enemies[j].rect.y == posy or enemies[j].rect.y - 1 == posy):
                            enemies[j].hp -= players[i].damage
                            if enemies[j].hp <= 0:
                                player_group.remove(enemies[j])
                                all_sprites.remove(enemies[j])
                                results[1].append(enemies[j])
                                results_group.add(enemies[j])
                                del d_1[j]
                                del enemies[j]
                            break

                i += 1
                if i >= len(players) and fl == 0:
                    i = 0
                    fl = 1
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fl = 1
                b = event.pos
                x1 = b[0] // board.cell_size
                y1 = b[1] // board.cell_size
                c = 0
                z = enemies[i].rect.x
                if x1 * board.cell_size < z and d_1[i] == 0:
                    enemies[i].image = pygame.transform.flip(enemies[i].image, True, False)
                    d_1[i] = 1
                elif x1 * board.cell_size > z and d_1[i] == 1:
                    enemies[i].image = pygame.transform.flip(enemies[i].image, True, False)
                    d_1[i] = 0
                k = 0
                while c != abs(x1 * board.cell_size - z) and k <= enemies[i].agility - 1 / 70:
                    c += 1
                    k += 1 / 70
                    if x1 * board.cell_size > z:
                        enemies[i].rect.x += 1
                        if len(pygame.sprite.spritecollide(enemies[i], player_group, False)) > 1:
                            enemies[i].rect.x -= 1
                    else:
                        enemies[i].rect.x -= 1
                        if len(pygame.sprite.spritecollide(enemies[i], player_group, False)) > 1:
                            enemies[i].rect.x += 1
                    clock.tick(150)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                c = 0
                z = enemies[i].rect.y
                while c != abs(y1 * board.cell_size - z) and k <= enemies[i].agility - 1 / 70:
                    c += 1
                    k += 1 / 70
                    if y1 * board.cell_size > z:
                        t = 1
                        enemies[i].rect.y += 1
                        if len(pygame.sprite.spritecollide(enemies[i], player_group, False)) > 1:
                            enemies[i].rect.y -= 1
                    else:
                        t = 2
                        enemies[i].rect.y -= 1
                        if len(pygame.sprite.spritecollide(enemies[i], player_group, False)) > 1:
                            enemies[i].rect.y += 1
                    clock.tick(150)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                zaglushka = 0
                posx = event.pos[0] // board.cell_size * board.cell_size
                posy = event.pos[1] // board.cell_size * board.cell_size
                for j in range(len(players)):
                    if (players[j].rect.x == posx or players[j].rect.x - 1 == posx) \
                            and (players[j].rect.y == posy or players[j].rect.y - 1 == posy) \
                            and abs(players[j].rect.x - enemies[i].rect.x) <= 70 \
                            and abs(players[j].rect.y - enemies[i].rect.y) <= 70:
                        zaglushka = 1
                    elif isinstance(enemies[i], Catapult) and (players[j].rect.x == posx or players[j].rect.x - 1 == posx) \
                            and (players[j].rect.y == posy or players[j].rect.y - 1 == posy):
                        zaglushka = 1
                if zaglushka:
                    enemies[i].animation_fight()
                    for j in range(len(players)):
                        try:
                            if (players[j].rect.x == posx or players[j].rect.x - 1 == posx) \
                                    and (players[j].rect.y == posy or players[j].rect.y - 1 == posy):
                                players[j].hp -= enemies[i].damage
                                if players[j].hp <= 0:
                                    player_group.remove(players[j])
                                    all_sprites.remove(players[j])
                                    results[0].append(players[j])
                                    results_group.add(players[j])
                                    del d[j]
                                    del players[j]
                        except IndexError:
                            pass
                i += 1
                if i >= len(enemies):
                    i = 0
                    fl = 0
    if ex.true_2:
        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        screen.fill((0, 0, 0))
        players, enemies, level_x, level_y = generate_level(load_level('data/map.txt'))
        d = [0] * len(players)
        d_1 = [1] * len(enemies)
        ex.true_2 = 0
        abc.stop()
        abc = pygame.mixer.Sound('data/17 - Battle - Academy.mp3')
        abc.play()
        abc.set_volume(0.25)
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(10)
    if fl == 0 and len(players) > 0 and len(enemies) > 0:
        pygame.draw.rect(screen, pygame.Color('Orange'), (players[i].rect.x, players[i].rect.y, 70, 70), 2)
    elif fl == 1 and len(enemies) > 0 and len(players) > 0:
        pygame.draw.rect(screen, pygame.Color('Red'), (enemies[i].rect.x, enemies[i].rect.y, 70, 70), 2)
    pygame.display.flip()
    if len(players) == 0 or len(enemies) == 0:
        start = True
        while start:
            fon = pygame.transform.scale(load_image('end.png'), (width, height))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 50)
            if len(players) > len(enemies):
                text = font.render("Победил Игрок 1", True, pygame.Color('#D2691E'))
            else:
                text = font.render("Победил Игрок 2", True, pygame.Color('#D2691E'))
            screen.blit(text, (205, 60))
            text = font.render("""    Результаты    """, True, pygame.Color('#D2691E'))
            text_x = width // 2 - text.get_width() // 2
            text_y = height // 2 - text.get_height() // 2 - 200
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, pygame.Color('#2F4F4F'), (text_x - 10, text_y - 10,
                                                               text_w + 20, text_h + 20), 5)
            text = font.render("Потери Игрока 1", True, pygame.Color('#D2691E'))
            screen.blit(text, (30, 250))
            for i in range(10):
                pygame.draw.rect(screen, pygame.Color('#2F4F4F'), (i * 70, 300, 70, 70), 5)
            text = font.render("Потери Игрока 2", True, pygame.Color('#D2691E'))
            screen.blit(text, (30, 400))
            for i in range(10):
                pygame.draw.rect(screen, pygame.Color('#2F4F4F'), (i * 70, 450, 70, 70), 5)
            for i in range(len(results[0])):
                results[0][i].rect = results[0][i].image.get_rect().move(i * 70, 300)
            for i in range(len(results[1])):
                results[1][i].rect = results[1][i].image.get_rect().move(i * 70, 450)
            results_group.draw(screen)
            true = True
            while true:
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        start = False
                        true = False
