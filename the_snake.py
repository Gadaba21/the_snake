from random import randint

import pygame

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Создаем базоввый класс"""

    position = [(320, 240)]  # Позиция центра экрана
    body_color = BOARD_BACKGROUND_COLOR  # Цвет объекта

    def __init__(self, position=[(320, 240)], body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для передачи в дочерник класс"""
        pass


class Snake(GameObject):
    """Создаем класс змея"""

    length = 1  # Начальная длинна змеи
    max_length = 20  # Длина змеи
    direction = RIGHT  # Направление движения
    next_direction = None  # следующее направление движения
    body_color = SNAKE_COLOR  # Цвет змеи

    def __init__(self, direction=RIGHT, body_color=SNAKE_COLOR, position=[(320, 240)]):
        """Начальное состояние змеи"""
        self.direction = direction
        self.body_color = body_color
        self.positions = position
        self.length = len(self.positions)

    def update_direction(self):
        """Изменение направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змеи"""
        first, second = self.positions[0]
        first_dir, second_dir = self.direction
        if first > SCREEN_WIDTH:
            first = 0
        elif first < 0:
            first = SCREEN_WIDTH
        if second > SCREEN_HEIGHT:
            second = 0
        elif second < 0:
            second = SCREEN_HEIGHT
        self.positions.insert(0, (first + first_dir * 20, second + second_dir * 20))
        self.positions.pop(-1)

    def draw(self):
        """Затирает след от змейки и отрисовывает новое положение"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

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
        self.body_color = SNAKE_COLOR
        self.positions = [(320, 240)]


class Apple(GameObject):
    """Создаем класс яблоко"""

    body_color = APPLE_COLOR  # Задаем цвет яблока

    def __init__(self, randomize_position, body_color=APPLE_COLOR):
        """Создаем экземпляр класса"""
        self.body_color = body_color
        self.position = randomize_position

    @staticmethod
    def randomize_position():
        """Задаем случайную позицию на игровом поле"""
        position = [(randint(0, 31) * 20, randint(0, 23) * 20)]
        return position

    def draw(self):
        """Отрисовывает яблоко на игровом поле"""
        rect = pygame.Rect(self.position[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Меняет направление движения при нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция управления змеёй"""
    pygame.init()  # Инициализация PyGame:

    # Создаем экземпляр классов
    apple = Apple(Apple.randomize_position())
    snake = Snake()

    while True:
        clock.tick(SPEED)  # Скорость змеи
        handle_keys(snake)  # Управление змеей
        screen.fill(BOARD_BACKGROUND_COLOR)  # Обновление экрана
        snake.update_direction()  # Изменение направления движения
        # Поедание яблока
        if apple.position[0] == snake.positions[0]:
            apple.position = apple.randomize_position()
            apple.draw()
            screen.fill(BOARD_BACKGROUND_COLOR)
            # Змейка не увеличивается если достигнит максимальной длины
            if len(snake.positions) != snake.max_length:
                snake.positions.append(apple.position)
        # Столкновение с телом змеи
        if snake.positions[0] in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        snake.move()  # Передвижение змеи
        apple.draw()  # Отрисовка яблока
        snake.draw()  # Отрисовка змеи
        pygame.display.update()  # Обновление игрового поля


if __name__ == "__main__":
    main()
