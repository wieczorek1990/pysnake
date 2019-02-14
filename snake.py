import pygame
import random
from collections import deque
from pygame.locals import *


WIN_SIZE = [640, 480]
SIZE = 20
BOARD_SIZE = [WIN_SIZE[0] // SIZE, WIN_SIZE[1] // SIZE]
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
FONT_SIZE = 32


class Snake:
    def __init__(self):
        self.parts = deque([(BOARD_SIZE[0] // 2,
                             BOARD_SIZE[1] // 2)])
        self.last_move = (0, 0)
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

    def forbidden_move(self, x, y):
      return self.last_move[0] == -x and self.last_move[1] == -y

    def up(self):
        if not self.forbidden_move(0, -1):
          self.move(0, -1)
          self.last_move = (0, -1)

    def down(self):
        if not self.forbidden_move(0, 1):
          self.move(0, 1)
          self.last_move = (0, 1)

    def left(self):
        if not self.forbidden_move(-1, 0):
          self.move(-1, 0)
          self.last_move = (-1, 0)

    def right(self):
        if not self.forbidden_move(1, 0):
          self.move(1, 0)
          self.last_move = (1, 0)

    def collision(self):
        point = self.head()
        if point[0] < 0 or point[0] > BOARD_SIZE[0] - 1:
            return True
        elif point[1] < 0 or point[1] > BOARD_SIZE[1] - 1:
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


def draw_highscore(surface, font, highscore):
  string = str(highscore)
  label = font.render(string, 1, RED)
  surface.blit(label, (WIN_SIZE[0] - label.get_width(), 0))


def main():
    random.seed()
    snake = Snake()
    food = Food()
    highscore = 0
    clock = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption('Snake')
    pygame.font.init()
    font = pygame.font.SysFont("monospace", FONT_SIZE)

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
            highscore += 1
            food.appear()
        snake.move(snake.last_move[0], snake.last_move[1])
        draw_snake(screen, snake)
        draw_food(screen, food)
        draw_highscore(screen, font, highscore)
        pygame.display.update()
        clock.tick(8)


if __name__ == '__main__':
    main()

