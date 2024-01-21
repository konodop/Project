# Импортируем os для доступа к спрайтам
import os
# Импортируем random для условий ведения боя
import random
import sys
# Импортируем пайгейм для самой игры
import pygame

q = ['1.png', '2.png', '3.png', '4.png']
random.shuffle(q)
flnam = "map.txt"
screen = pygame.display.set_mode((550, 500))
# Характеристики персонажа
health = 100
defence = 1
damage = 5
money = 0
kills = 0


# Функция вывода текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("Arial.ttf", size)
    text_surface = font.render(text, True, pygame.Color('WHITE'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# Виды плиток
tile_images = {'wall': pygame.transform.scale(load_image('stone.png'), (50, 50)),
               'empty': load_image('grass.png'),
               'armor': load_image('armor.png'),
               'weapon': load_image('sword.png'),
               'heal': load_image('heal.png'),
               'enemy': load_image(q[0])
               }
player_image = load_image('Warrior.png')
# Размер плиток в пикселях
tile_width = tile_height = 50

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Задаём начальное положение камеры
def reset(obj):
    obj.rect.x -= (player.pos[0] - 10) * 50 + 250
    obj.rect.y -= (player.pos[1] - 10) * 50 + 300


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, key):
        # Перемещение по ключам
        if key == '4':
            self.dx = 50
            self.dy = 0
        elif key == '3':
            self.dx = -50
            self.dy = 0
        elif key == '2':
            self.dy = -50
            self.dx = 0
        elif key == '1':
            self.dy = 50
            self.dx = 0
        elif key == '0':
            self.dx = self.dy = 0
        elif key == '5':
            self.dy = -400
            self.dx = 0
        elif key == '6':
            self.dy = 400
            self.dx = 0


class End(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        # Выводим картинку о завершении игры
        self.image = pygame.image.load(os.path.join('data', 'gameover.png'))
        self.rect = self.image.get_rect()


# Класс Плиток
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)


# Класс Игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'w':
                Tile('empty', x, y)
                Tile('weapon', x, y)
            elif level[y][x] == 'a':
                Tile('empty', x, y)
                Tile('armor', x, y)
            elif level[y][x] == 'e':
                Tile('empty', x, y)
                Tile('enemy', x, y)
            elif level[y][x] == 'h':
                Tile('empty', x, y)
                Tile('heal', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (550, 500))
    screen.blit(fon, (0, 0))
    draw_text(screen, 'Расхититель Пещер', 30, 150, 10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        pygame.time.Clock().tick(30)


if __name__ == '__main__':
    pygame.init()
    camera = Camera()
    running = True
    start_screen()
    s = 1
    level_map = load_level(flnam)
    player, max_x, max_y = generate_level(level_map)
    all_sprites.draw(screen)
    player_group.draw(screen)
    if s == 1:
        for sprite in all_sprites:
            reset(sprite)
        for p in player_group:
            reset(p)
        s = 0
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = player.pos
                if event.key == pygame.K_UP:
                    if level_map[y - 1][x] != '#':
                        if money > 4:
                            if level_map[y - 1][x] == 'w':
                                damage *= 1.5
                                money -= 5
                            elif level_map[y - 1][x] == 'a':
                                defence *= 1.5
                                money -= 5
                        if money > 9 and health < 100:
                            if level_map[y - 1][x] == 'h':
                                health = 100
                                money -= 10
                        camera.update('1')
                        player.move(x, y - 1)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                elif event.key == pygame.K_DOWN:
                    if level_map[y + 1][x] != '#':
                        if y <= 19:
                            camera.update('2')
                            player.move(x, y + 1)
                            for sprite in all_sprites:
                                camera.apply(sprite)
                        else:
                            camera.update('6')
                            player.move(x, y - 8)
                            kills += 1
                            health -= (random.randint(6, 20) / defence * kills / damage)
                            money += random.randint(2, 4)
                            for sprite in all_sprites:
                                camera.apply(sprite)
                elif event.key == pygame.K_RIGHT:
                    if level_map[y][x + 1] != '#':
                        camera.update('3')
                        player.move(x + 1, y)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                elif event.key == pygame.K_LEFT:
                    if level_map[y][x - 1] != '#':
                        camera.update('4')
                        player.move(x - 1, y)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                else:
                    camera.update('0')
            screen.fill((0, 0, 0))
            # изменяем ракурс камеры
            # обновляем положение всех спрайтов
            all_sprites.draw(screen)
            player_group.draw(screen)
            # Выводим характеристики прерсонажа
            draw_text(screen, 'Здоровье: ' + str(int(health)), 18, 65, 10)
            draw_text(screen, 'деньги: ' + str(money), 18, 45, 36)
            draw_text(screen, 'убийства: ' + str(kills), 18, 51, 60)
            draw_text(screen, 'урон: ' + str(int(damage)), 18, 35, 85)
            draw_text(screen, 'защита: ' + str(int(defence)), 18, 45, 110)
            if health <= 0:
                screen = pygame.display.set_mode((600, 300))
                End(all_sprites)
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                            running = False
                    all_sprites.draw(screen)
                    pygame.display.update()
            pygame.display.flip()
    terminate()
