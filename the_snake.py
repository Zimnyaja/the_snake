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

KEY_DICT = {
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
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Главный класс игры. Родитель для основных объектов."""

    def __init__(self, position=CENTER, body_color=()):
        """Инициализируем объект."""
        self.position = position
        self.body_color = body_color
    
    def draw(self):
        """Заявляем функцию. Пока она пустая."""
        raise NotImplementedError('Функция будет реализована'
                                  'в классах наследниках')

    def draw_one(self, pose, color_fill=BOARD_BACKGROUND_COLOR,
                 color_out=BOARD_BACKGROUND_COLOR):
        """Отрисовывает один квадратик"""
        rect = pg.Rect(pose, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color_fill, rect)
        pg.draw.rect(screen, color_out, rect, 1)


class Apple(GameObject):
    """Яблочко. Описывает яблоко и действия с ним."""

    def __init__(self, position=(), body_color=APPLE_COLOR):
        """Инициализируем объект класса Яблоко. Позиция рандомная."""
        super().__init__(position, body_color)
        self.randomize_position((CENTER))

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
        self.draw_one(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Змея собственной персоной. Описывает змею и её поведение."""

    def __init__(self, position=[CENTER], body_color=SNAKE_COLOR):
        """Инициализируем змею."""
        super().__init__(position, body_color)
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

        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            self.last = self.positions[-1]

        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змею на экране, затирает хвост"""
        for position in self.positions[:-1]:
            # Тут была рекомендация убрать цикл. Но если ее убрать,
            # При обновлении позиция камня, змея теряет свое тело.
            self.draw_one(position, self.body_color, BORDER_COLOR)

        self.draw_one(self.positions[0], self.body_color, BORDER_COLOR)
        if self.last:
            self.draw_one(self.last)

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
            elif (game_object.direction, event.key) in KEY_DICT:
                game_object.next_direction = (
                    KEY_DICT.get((game_object.direction, event.key),
                                 game_object.direction))


def main():
    """Ниже тело основной программы"""
    pg.init()

    apple = Apple()
    snake = Snake()
    stone = Apple(body_color=STONE_COLOR)

    while True:

        clock.tick(SPEED)
        handle_keys(snake)

        if apple.position in snake.positions and snake.lenght % 5 == 0:
            snake.lenght += 1
            apple.randomize_position([*snake.positions, stone.position])
            stone.randomize_position([*snake.positions, apple.position])
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif apple.position in snake.positions:
            snake.lenght += 1
            apple.randomize_position([*snake.positions, stone.position])

        if stone.position in snake.positions:
            snake.reset()

        snake.move()
        snake.update_direction()
        apple.draw()
        snake.draw()
        stone.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
