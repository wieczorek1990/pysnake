#include <ncurses.h>
#include <time.h>
#include <deque>
#include <random>

#define Y_MAX 24
#define X_MAX 80

using namespace std;

class Snake {
public:
  deque<pair<int, int>> parts;
  pair<int, int> last_move;
  Snake() {
    parts.push_back(make_pair(Y_MAX / 2, X_MAX / 2));
    last_move = make_pair(0, 0);
    down();
  }
  void up() {
    if (!forbidden_move(0, -1)) {
      move(0, -1);
      last_move = make_pair(0, -1);
    }
  }
  void down() {
    if (!forbidden_move(0, 1)) {
      move(0, 1);
      last_move = make_pair(0, 1);
    }
  }
  void left() {
    if (!forbidden_move(-1, 0)) {
      move(-1, 0);
      last_move = make_pair(-1, 0);
    }
  }
  void right() {
    if (!forbidden_move(1, 0)) {
      move(1, 0);
      last_move = make_pair(1, 0);
    }
  }
  void move(int x, int y) {
    parts.pop_back();
    pair<int, int> front = parts.front();
    parts.push_front(make_pair(y + front.first,
                               x + front.second));
  }
  void move() {
    move(last_move.first, last_move.second);
  }
  pair<int, int> head() {
    return parts.front();
  }
  void eat(pair<int, int> point) {
    parts.push_front(point);
  }
  bool collision() {
    pair<int, int> point = head();
    if (point.first < 0 || point.first > Y_MAX - 1) {
      return true;
    } else if (point.second < 0 || point.second > X_MAX - 1) {
      return true;
    }
    for (int i = 0; i < parts.size(); ++i) {
      if (i == 0) {
        continue;
      }
      if (parts.at(i) == point) {
        return true;
      }
    }
    return false;
  }
  bool forbidden_move(int x, int y) {
    return last_move.first == -x && last_move.second == -y;
  }
};

class Food {
public:
  pair<int, int> point;
  Food() {
    appear();
  }
  void appear() {
    point = make_pair(
      rand() % Y_MAX,
      rand() % X_MAX
    );
  }
};

int main() {
  int ch;

  initscr();
  cbreak();
  noecho();
  curs_set(0);
  WINDOW *win = newwin(Y_MAX, X_MAX, 0, 0);
  nodelay(stdscr, true);
  keypad(stdscr, true);
  timeout(100);

  srand(time(NULL));

  Snake snake;
  Food food;

  while (true) {
    if ((ch = getch()) == ERR) {
      // user has not responded
      snake.move();
    } else {
      // user pressed a key
      if (ch == KEY_DOWN) {
        snake.down();
      } else if (ch == KEY_UP) {
        snake.up();
      } else if (ch == KEY_LEFT) {
        snake.left();
      } else if (ch == KEY_RIGHT) {
        snake.right();
      }
    }

    if (snake.collision()) {
      endwin();
      exit(0);
    }

    if (snake.head() == food.point) {
      snake.eat(food.point);
      food.appear();
    }

    wclear(win);

    for (deque<pair<int, int>>::iterator it = snake.parts.begin();
         it != snake.parts.end();
         ++it) {
      pair<int, int> p = *it;
      mvwaddch(win, p.first, p.second, ACS_CKBOARD);
    }
    mvwaddch(win, food.point.first, food.point.second, ACS_DIAMOND);

    wrefresh(win);
  }
}

