from game import Game

WIDTH = 9
HEIGHT = 9
MINES = 10

g = Game(WIDTH, HEIGHT, MINES)

# utility functions for console play

# start a game and open center tile.
def s():
    global g
    g = Game(WIDTH, HEIGHT, MINES)
    g.auto_open(4, 4)
    g.show()

# double click a tile
def d(x, y):
    g.double_open(x, y)
    g.show()

# click(open) a tile
def o(x, y):
    g.auto_open(x, y)
    g.show()

# right click (mark) a tile
def m(x, y):
    g.mark(x, y)
    g.show()

# unmark a tile
def u(x, y):
    g.unmark(x, y)
    g.show()