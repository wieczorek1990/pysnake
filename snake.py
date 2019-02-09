import pygame
import random
from collections import deque
from pygame.locals import *


WINSIZE = [640, 480]
SIZE = 20
BOARD_SIZE = [WINSIZE[0] // SIZE, WINSIZE[1] // SIZE]
BLACK = 0, 0, 0
WHITE = 255, 255, 255

class Snake:
    def __init__(self):
        self.parts = deque([(BOARD_SIZE[0] // 2,
                             BOARD_SIZE[1] // 2)])
        self.down()

    def head(self):
        return self.parts[0]

    def move(self, x, y):
        last = self.parts.pop()
        if len(self.parts) > 0:
            front = self.head()
        else:
            front = last
        self.parts.extendleft([(x + front[0], y + front[1])])

    def eat(self, food):
        self.parts.extendleft([(food.x, food.y)])

    def up(self):
        self.move(0, -1)
        self.last_move = (0, -1)

    def down(self):
        self.move(0, 1)
        self.last_move = (0, 1)

    def left(self):
        self.move(-1, 0)
        self.last_move = (-1, 0)

    def right(self):
        self.move(1, 0)
        self.last_move = (1, 0)

    def collision(self):
        point = self.head()
        if point[0] < 1 or point[0] > BOARD_SIZE[0] - 2:
            return True
        elif point[1] < 1 or point[1] > BOARD_SIZE[1] - 2:
            return True
        for i in range(len(self.parts)):
            if i == 0:
                continue
            if self.parts[i] == point:
                return True
        return False

 
class Food:
    def __init__(self):
        self.appear()

    def appear(self):
        self.x, self.y = random.randint(0, BOARD_SIZE[0] - 1),\
                         random.randint(0, BOARD_SIZE[1] - 1)

    def __contains__(self, snake):
        return any([item == (self.x, self.y) for item in snake.parts])


def draw_snake(surface, snake):
    for pos in snake.parts:
        for x in range(pos[0] * SIZE, (1 + pos[0]) * SIZE):
            for y in range(pos[1] * SIZE, (1 + pos[1]) * SIZE):
                surface.set_at((x, y), BLACK)


def draw_food(surface, food):
    for x in range(food.x * SIZE, (1 + food.x) * SIZE):
        for y in range(food.y * SIZE, (1 + food.y) * SIZE):
            surface.set_at((x, y), BLACK)


def main():
    random.seed()
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Snake')

    done = 0
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT:
                done = 1
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    snake.up()
                if e.key == K_DOWN:
                    snake.down()
                if e.key == K_LEFT:
                    snake.left()
                if e.key == K_RIGHT:
                    snake.right()
        screen.fill(WHITE)
        if snake.collision():
            break
        if snake in food:
            snake.eat(food)
            food.appear()
        snake.move(snake.last_move[0], snake.last_move[1])
        draw_snake(screen, snake)
        draw_food(screen, food)
        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()

