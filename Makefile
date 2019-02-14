.DEFAULT_GOAL := build

build:
	g++ snake.cpp -lncurses -o snake && chmod +x snake

install:
	cp snake /usr/local/bin/snake

uninstall:
	rm /usr/local/bin/snake
