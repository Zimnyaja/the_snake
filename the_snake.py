from random import choice, randint

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
SPEED = 1

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Главный класс игры. Родитель для основных объектов"""

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = ()

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заявляем функцию, пока она пустая"""
        pass


class Apple(GameObject):
    """Яблочко. Описывает яблоко и действия с ним."""

    position = ()
    body_color = APPLE_COLOR

    def __init__(self, position=position, body_color=body_color):
        """Инициализируем объект. Если позиция и цвет не указаны, значения
        берем из аргументов класса Яблоко. Если указана конкретная позиция
        яблока (разные вариации игры), оставляем её. Если нет - рандом.
        """
        super().__init__(position, body_color)
        if position:
            self.position = position
        else:
            self.position = self.randomize_position()

    def randomize_position(self):
        """Присваивает позиции случайное значение в пределах поля."""
        self.position = ((randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        return self.position

    def draw(self):
        """Отрисовывает яблоко в заданном цвете и позиции"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змея собственной персоной. Описывает змею и её поведение"""

    lenght = 1
    positions = GameObject.position

    # # Метод draw класса Snake
    def draw(self):
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



def main():
    # Инициализация PyGame:
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    # Тут нужно создать экземпляры классов.
    apple1 = Apple((0,0))
    apple = Apple()
    clock.tick(SPEED)
    apple1.body_color = (BORDER_COLOR)
    apple1.draw()
    apple.draw()
    pygame.display.update()
#    while True:
 #       clock.tick(SPEED)
 #       apple.draw()
        # Тут опишите основную логику игры.
  #      pygame.display.update()
    #pygame.quit()


if __name__ == '__main__':
    main()



# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
