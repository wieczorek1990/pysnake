#!/usr/bin/env ruby

require "curses"

Y_MAX = 24
X_MAX = 80

def place_string(y, x, string)
  Curses.setpos(x, y)
  Curses.addstr(string)
end

class Snake
  attr_reader :parts

  def initialize
    @parts = [[X_MAX / 2, Y_MAX / 2]]
    @last_move = [0, 0]
    down
  end

  def forbidden_move(x, y)
    (@last_move[0] == -x) and (@last_move[1] == -y)
  end

  def move
    _move(@last_move[0], @last_move[1])
  end

  def head
    @parts[0]
  end

  def _move(x, y)
    front = head
    @parts.pop
    @parts.unshift [front[0] + x, front[1] + y]
  end

  def up
    if not forbidden_move 0, -1
      _move 0, -1
      @last_move = [0, -1]
    end
  end

  def down
    if not forbidden_move 0, 1
      self._move 0, 1
      @last_move = [0, 1]
    end
  end

  def left
    if not forbidden_move -1, 0
      _move -1, 0
      @last_move = [-1, 0]
    end
  end

  def right
    if not forbidden_move 1, 0
      _move 1, 0
      @last_move = [1, 0]
    end
  end

  def eat(food)
    @parts.unshift [food.x, food.y]
  end

  def collision
    point = head
    if point[0] < 0 or point[0] > X_MAX - 1
      return true
    end
    if point[1] < 0 or point[1] > Y_MAX - 1
      return true
    end
    (0...@parts.size).each do |i|
      if i == 0
        next
      end
      if @parts[i] == point
        return true
      end
    end
    false
  end
end

class Food
  attr_reader :x, :y

  def initialize(snake)
    appear
  end

  def appear
    @x, @y = rand(0...X_MAX), rand(0...Y_MAX)
  end

  def contains(snake)
    snake.parts.any? {|part| part == [@x, @y]}
  end
end

def draw_snake(snake)
  snake.parts.each do |part|
    place_string part[0], part[1], '#'
  end
end

def draw_food(food)
  place_string food.x, food.y, '*'
end

Curses.init_screen
Curses.cbreak
Curses.noecho
Curses.curs_set 0
Curses.stdscr.nodelay = 1
Curses.stdscr.keypad = 1
srand Time.now.to_i

snake = Snake.new
food = Food.new snake

loop do
  char = Curses::getch
  if char == Curses::KEY_UP
    snake.up
  elsif char == Curses::KEY_DOWN
    snake.down
  elsif char == Curses::KEY_LEFT
    snake.left
  elsif char == Curses::KEY_RIGHT
    snake.right
  end
  if snake.collision
    break
  end
  if food.contains snake
    snake.eat food
    food.appear
  end
  snake.move
  Curses.clear
  draw_snake(snake)
  draw_food(food)
  Curses.refresh
  sleep(0.1)
end
Curses.close_screen
