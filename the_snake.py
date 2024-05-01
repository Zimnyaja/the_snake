from random import choice, randint

import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 128, 0)
STONE_COLOR = (160, 160, 160)
SNAKE_COLOR = (0, 255, 0)
SPEED = 9

KEY_DIRECTION = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pg.time.Clock()


class GameObject:
    """Главный класс игры. Родитель для основных объектов."""

    def __init__(self, body_color=None, position=CENTER):
        """Инициализируем объект."""
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Заявляем функцию. Пока она пустая."""
        raise NotImplementedError('Функция будет реализована'
                                  'в классах наследниках')

    def draw_one(self, pose, color_fill=None, color_out=BORDER_COLOR):
        """Отрисовывает один квадратик"""
        color_fill = color_fill or self.body_color
        rect = pg.Rect(pose, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color_fill, rect)
        pg.draw.rect(screen, color_out, rect, 1)


class Apple(GameObject):
    """Яблочко. Описывает яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR, taken=[]):
        """Инициализируем объект класса Яблоко. Позиция рандомная."""
        super().__init__(body_color)
        self.randomize_position(taken)

    def randomize_position(self, taken_position):
        """Присваивает объекту случайное значение в пределах поля.
        Проверяет пересечение с объектами на поле.
        """
        while True:
            self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                             (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
            if self.position not in taken_position:
                break

    def draw(self):
        """Отрисовывает яблоко в заданном цвете и позиции."""
        self.draw_one(self.position)


class Snake(GameObject):
    """Змея собственной персоной. Описывает змею и её поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализируем змею."""
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змеи. Добавляет голову, удаляет хвост."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]

        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змею на экране, затирает хвост"""
        for position in self.positions[:-1]:
            self.draw_one(position)

        self.draw_one(self.positions[0])
        if self.last:
            self.draw_one(self.last, BOARD_BACKGROUND_COLOR,
                          BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Возвращает голову змеи. Первый элемент списка."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змею в начальное состояние после столкновения.
        Рандомно выбирает новое направление.
        """
        self.lenght = 1
        self.last = None
        self.positions = [CENTER]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))


def reset_screen(object):
    """Сбрасывает объект, затирает экран"""
    object.reset()
    screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Управление клавишами"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            else:
                game_object.next_direction = KEY_DIRECTION.get(
                    (game_object.direction, event.key), game_object.direction)


def main():
    """Ниже тело основной программы"""
    pg.init()

    snake = Snake()
    apple = Apple(taken=[snake.positions])
    stone = Apple(body_color=STONE_COLOR, taken=[*snake.positions,
                                                 apple.position])

    while True:

        clock.tick(SPEED)
        handle_keys(snake)

        pg.display.set_caption('Змейка.  Управление - стрелки.  '
                               'Выход - Esc.  Съедаем яблоко, избегаем камня. '
                               f'{snake.lenght}')

        if snake.positions[0] in snake.positions[2:]:
            reset_screen(snake)

        if apple.position in snake.positions and snake.lenght % 5 == 0:
            snake.lenght += 1
            apple.randomize_position([*snake.positions, stone.position])
            stone.randomize_position([*snake.positions, apple.position])

            screen.fill(BOARD_BACKGROUND_COLOR)
        elif apple.position in snake.positions:
            snake.lenght += 1
            apple.randomize_position([*snake.positions, stone.position])

        if (stone.position in snake.positions):
            reset_screen(snake)

        snake.move()
        snake.update_direction()
        apple.draw()
        snake.draw()
        stone.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
