import pygame
import random
import time
import numpy as np

# Инициализация Pygame
pygame.init()

# Установка размеров окна
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
moving = False
# Ваш ASCII-арт
ascii_art = """
      /\_/\\
 /\  / o o \\
//\\\\ \\~(*)~/
`  \\/   ^ /
   | \\|| ||
   \\ '|| ||
    \\)()-())
"""

# Преобразуйте ASCII-арт в список строк
lines = ascii_art.split('\n')

# Найти максимальную длину строки
max_length = max(len(line) for line in lines)

# Создайте пустой список для хранения пикселей
pixels = []

# Пройдите по каждой строке
for line in lines:
    # Удалить пробелы в начале и конце строки
    line = line.strip()
    # Добавить пробелы в конце строки, если она короткая
    line += ' ' * (max_length - len(line))
    # Преобразуйте каждый символ в 0 или 1
    row = [0 if char == ' ' else 1 for char in line]
    # Добавьте строку в список пикселей
    pixels.append(row)

# Преобразуйте список пикселей в numpy массив
image = np.array(pixels)
pixel_size = 10

# Создайте две версии изображения котика
cat_surface_right = pygame.Surface((len(pixels[0])*pixel_size, len(pixels)*pixel_size))
cat_surface_left = pygame.Surface((len(pixels[0])*pixel_size, len(pixels)*pixel_size))

for y in range(len(pixels)):
    for x in range(len(pixels[y])):
        color = (0, 0, 0) if pixels[y][x] == 1 else (255, 255, 255)
        pygame.draw.rect(cat_surface_right, color, pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size))
        pygame.draw.rect(cat_surface_left, color, pygame.Rect((len(pixels[0])-x-1)*pixel_size, y*pixel_size, pixel_size, pixel_size))

# В начале игры котик смотрит вправо
cat_surface_current = cat_surface_right

# Установка начального положения котика и скорости его движения
cat_x, cat_y = 0, screen_height - cat_surface_right.get_height()
cat_speed = 1

# Создание корма
food_size = 40
food_x, food_y = random.randint(0, screen_width - food_size), random.randint(0, screen_height - food_size)
food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # случайный цвет
food_eaten = False
food_time = time.time()

# Создание шрифта
font = pygame.font.Font(None, 36)

# Создание счетчика еды
food_counter = 0

# Создание системы опыта и уровней
experience = 0
level = 1
experience_for_next_level = 100

# Основной цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление положения котика
    moving = False
    if cat_x < food_x:
        cat_x += cat_speed
        cat_surface_current = cat_surface_right
        moving = True
    elif cat_x > food_x:
        cat_x -= cat_speed
        cat_surface_current = cat_surface_left
        moving = True
    if cat_y < food_y:
        cat_y += cat_speed
        moving = True
    elif cat_y > food_y:
        cat_y -= cat_speed
        moving = True

    # Обеспечиваем "цикличность" движения котика
    cat_x = cat_x % screen_width
    cat_y = cat_y % screen_height

    # Проверка, съел ли котик корм
    if moving and abs(cat_x - food_x) < cat_speed and abs(cat_y - food_y) < cat_speed:
        food_eaten = True
        food_counter += 1  # увеличиваем счетчик еды
        experience += 10  # увеличиваем опыт

        # Проверка, достигнут ли следующий уровень
        if experience >= experience_for_next_level:
            level += 1  # повышаем уровень
            experience -= experience_for_next_level  # сбрасываем опыт
            experience_for_next_level += 10  # увеличиваем требование для следующего уровня

    # Если корм съеден, создаем новый корм через 5 секунд
    if food_eaten and time.time() - food_time > 5:
        food_x, food_y = random.randint(0, screen_width - food_size), random.randint(0, screen_height - food_size)
        food_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # случайный цвет
        food_eaten = False
        food_time = time.time()

    # Очистка экрана
    screen.fill((255, 255, 255))

    # Отрисовка корма
    pygame.draw.rect(screen, food_color, pygame.Rect(food_x, food_y, food_size, food_size))

    # Отрисовка котика
    screen.blit(cat_surface_current, (cat_x, cat_y))

    # Отображение счетчика еды
    food_counter_text = font.render(f'поднято снарядов: {food_counter}', True, (0, 0, 0))
    screen.blit(food_counter_text, (10, 10))

    # Отображение уровня и опыта
    level_text = font.render(f'лвл: {level}', True, (0, 0, 0))
    screen.blit(level_text, (10, 40))
    experience_text = font.render(f'експ: {experience}/{experience_for_next_level}', True, (0, 0, 0))
    screen.blit(experience_text, (10, 70))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()