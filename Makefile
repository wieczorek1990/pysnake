.DEFAULT_GOAL := build

build:
	g++ -lncurses main.cpp -o snake && chmod +x snake

install:
	cp snake /usr/local/bin/snake

uninstall:
	rm /usr/local/bin/snake
