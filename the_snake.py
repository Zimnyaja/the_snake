from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Главный класс игры. Родитель для основных объектов."""

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = ()

    def __init__(self, position=position, body_color=body_color):
        """Инициализируем объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заявляем функцию, пока она пустая."""
        pass


class Apple(GameObject):
    """Яблочко. Описывает яблоко и действия с ним."""

    position = ()
    body_color = APPLE_COLOR

    def __init__(self, position=position, body_color=body_color):
        """Инициализируем объект класса Яблоко. Позиция рандомная."""
        super().__init__(position, body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Присваивает позиции случайное значение в пределах поля."""
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        return self.position

    def draw(self):
        """Отрисовывает яблоко в заданном цвете и позиции."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змея собственной персоной. Описывает змею и её поведение."""

    lenght = 1
    positions = [GameObject.position]
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self, pose=positions, color=body_color, direction=direction,
                 next=next_direction, len=lenght):
        """Инициализируем змею."""
        super().__init__(pose, color)
        self.positions = pose
        self.last = None
        self.direction = direction
        self.next_direction = next
        self.lenght = len

    def update_direction(self):
        """Обновляет направление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змеи. Добавляет голову, удаляет хвост."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = (head[0] + dx * GRID_SIZE, head[1] + dy * GRID_SIZE)
        x, y = new_head

        if x == SCREEN_WIDTH and self.direction == RIGHT:
            x = 0
        elif x < 0 and self.direction == LEFT:
            x = (SCREEN_WIDTH - GRID_SIZE)
        elif y < 0 and self.direction == UP:
            y = (SCREEN_HEIGHT - GRID_SIZE)
        elif y == SCREEN_HEIGHT and self.direction == DOWN:
            y = 0

        new_head = (x, y)

        if len(self.positions) > 3 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)

        if len(self.positions) - 1 > self.lenght:
            self.positions.pop()

        self.last = self.positions[-1]

    def draw(self):
        """Отрисовывает змею на экране, затирает хвост"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает голову змеи. Первый элемент списка."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змею в начальное состояние после столкновения.
        Рандомно выбирает новое направление.
        """
        self.lenght = 1
        self.last = None
        self.positions = [GameObject.position]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Управление клавишами"""
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


def checking_intersection(snake, object_position, tested_position):
    """Функция проверяет пересечение координат объекта со змеей.
    Используется для проверки новой рандомной позиции объектов.
    Работает при наличии 2х объектов Яблока на поле.
    """
    if tested_position in (*snake, object_position):
        return True


def main():
    """Ниже тело основной программы"""
    pygame.init()

    apple = Apple()
    snake = Snake()
    stone = Apple(body_color=STONE_COLOR)
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(SPEED)

        def checking_intersection(snake, object_position, tested_position):
            if tested_position in (*snake, object_position):
                return True

        while checking_intersection(snake.positions, stone.position,
                                    apple.position):
            apple.randomize_position()
        while checking_intersection(snake.positions, apple.position,
                                    stone.position):
            stone.randomize_position()

        apple.draw()
        stone.draw()
        snake.move()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()

        if apple.position in snake.positions and snake.lenght % 5 == 0:
            snake.lenght += 1
            apple.randomize_position()
            while checking_intersection(snake.positions, stone.position,
                                        apple.position):
                apple.randomize_position()
            stone.randomize_position()
            while checking_intersection(snake.positions, apple.position,
                                        stone.position):
                stone.randomize_position()
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif apple.position in snake.positions:
            snake.lenght += 1
            apple.randomize_position()
            while checking_intersection(snake.positions, stone.position,
                                        apple.position):
                apple.randomize_position()

        if stone.position in snake.positions:
            snake.reset()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
