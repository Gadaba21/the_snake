from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5
speed = SPEED
# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Создаем базоввый класс"""

    body_color = BOARD_BACKGROUND_COLOR  # Цвет объекта

    def __init__(self, position=[(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]):
        self.position = position

    def draw(self, positions):
        """Метод для отрисовки обьектов"""
        for position in positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Создаем класс змея"""

    length = 1  # Начальная длинна змеи
    max_length = 20  # Длина змеи
    direction = RIGHT  # Направление движения
    next_direction = None  # следующее направление движения
    body_color = SNAKE_COLOR  # Цвет змеи

    def __init__(self):
        """Начальное состояние змеи"""
        self.reset()

    def update_direction(self, next_direction):
        """Изменение направления движения"""
        if next_direction:
            self.direction = next_direction
            next_direction = None

    def move(self):
        """Обновляет позицию змеи"""
        first, second = Snake.get_head_position(self.positions)
        first_dir, second_dir = self.direction
        first_coord = (first + (first_dir * GRID_SIZE)) % SCREEN_WIDTH
        second_coord = (second + (second_dir * GRID_SIZE)) % SCREEN_HEIGHT
        self.positions.insert(0, (first_coord, second_coord))
        self.positions.pop(-1)

    @staticmethod
    def get_head_position(position):
        """Возращаем 1 элемент в змейке, его голову"""
        head_position = position[0]
        return head_position

    def reset(self):
        """Возвращает змею в исходное состояние"""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]


class Apple(GameObject):
    """Создаем класс яблоко"""

    body_color = APPLE_COLOR  # Задаем цвет яблока

    def __init__(self, randomize_position=[(SCREEN_WIDTH / 2,
                                            SCREEN_HEIGHT / 2)]):
        """Создаем экземпляр класса"""
        self.position = randomize_position

    @staticmethod
    def randomize_position():
        """Задаем случайную позицию на игровом поле"""
        position = [(randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                     randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]
        return position


def handle_keys(game_object):
    """Меняет направление движения при нажатия клавиш b скорость змеи"""
    global speed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_1:
                speed += 1
            elif event.key == pg.K_2:
                speed -= 1


def main():
    """Основная функция управления змеёй"""
    pg.init()  # Инициализация PyGame:

    # Создаем экземпляр классов
    apple = Apple(Apple.randomize_position())
    snake = Snake()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        clock.tick(speed)  # Скорость змеи
        handle_keys(snake)  # Управление змеей
        snake.update_direction(snake.next_direction)  # Изменение направления
        # Поедание яблока
        if apple.position[0] == Snake.get_head_position(snake.positions):
            apple.position = apple.randomize_position()
            # Змейка не увеличивается если достигнит максимальной длины
            if len(snake.positions) != snake.max_length:
                snake.positions.append(apple.position)
        # Столкновение с телом змеи
        if Snake.get_head_position(snake.positions) in snake.positions[2:]:
            snake.reset()
        if apple.position in snake.positions:
            apple.position = apple.randomize_position()
        snake.move()  # Передвижение змеи
        apple.draw(apple.position)  # Отрисовка яблока
        snake.draw(snake.positions)  # Отрисовка змеи
        pg.display.update()  # Обновление игрового поля


if __name__ == "__main__":
    main()
