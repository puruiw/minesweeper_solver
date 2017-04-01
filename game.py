import numpy as np


def putchar(c):
    print(' ' + str(c), end="")


class Game:
    @staticmethod
    def beginner():
        return Game(9, 9, 10)

    @staticmethod
    def intermediate():
        return Game(16, 16, 40)

    @staticmethod
    def expert():
        return Game(30, 16, 99)

    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.marked = 0
        self.opened = 0
        self.boom = False

        # generate tiles: -1: mine, 0~8:mines around this tile.
        self.tiles = np.zeros((width, height), dtype=np.int8)
        for i in np.random.choice(width * height, mines, replace=False):
            self.tiles[i % width][int(i / width)] = -1
        for x in range(width):
            for y in range(height):
                if self.tiles[x][y] != -1:
                    self.tiles[x][y] = self._nearby_mines(x, y)

        # states: -1: marked as mine, 0: not opened, 1, opened.
        self.states = np.zeros((width, height), dtype=np.int8)

    def nearby(self, x, y):
        nearby_tiles = ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1))
        return [(p, q) for (p, q) in nearby_tiles if (0 <= p < self.width and 0 <= q < self.height)]

    def _nearby_mines(self, x, y):
        return np.sum([self.tiles[p][q] == -1 for (p, q) in self.nearby(x, y)])

    def nearby_marks(self, x, y):
        return np.sum([self.states[p][q] == -1 for (p, q) in self.nearby(x, y)])

    def open(self, x, y):
        if self.states[x][y] == -1:
            return -1
        elif self.states[x][y] == 1:
            return self.tiles[x][y]

        self.states[x][y] = 1
        result = self.tiles[x][y]
        if result == -1:
            self.boom = True
        else:
            self.opened += 1
        return result

    def success(self):
        return self.opened == self.width * self.height - self.mines

    def auto_open(self, x, y):
        to_open = [(x, y)]
        while to_open:
            location = to_open.pop(0)
            result = self.open(location[0], location[1])
            if self.success():
                self.mark_remaining()
            if result == 0:
                for (p, q) in self.nearby(location[0], location[1]):
                    if self.get_state(p, q) == -2 and (p, q) not in to_open:
                        to_open.append((p, q))

    def double_open(self, x, y):
        if self.states[x][y] != 1:
            return
        tile = self.tiles[x][y]
        if tile != self.nearby_marks(x, y):
            return
        for (p, q) in self.nearby(x, y):
            if self.states[p][q] == 0:
                self.auto_open(p, q)

    def mark(self, x, y):
        if self.states[x][y] != 0:
            return
        self.states[x][y] = -1
        self.marked += 1

    def unmark(self, x, y):
        if self.states[x][y] == -1:
            self.states[x][y] = 0
            self.marked -= 1

    def _tile_mark(self, x, y):
        if self.tiles[x][y] == -1:
            return 'X'
        return self.tiles[x][y]

    def mark_remaining(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.get_state(x, y) == -2:
                    self.mark(x, y)

    def get_state(self, x, y):
        if self.states[x][y] == -1:
            return -1
        elif self.states[x][y] == 0:
            return -2
        else:
            return self.tiles[x][y]

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.states[x][y] == -1:
                    putchar('*')
                elif self.states[x][y] == 1:
                    putchar(self._tile_mark(x, y))
                else:
                    putchar('_')
            print('')
        print('Mines: %4d' % (self.mines - self.marked))
        if self.boom:
            print('####### BOOOOOOOOOOOM ######')
        elif self.success():
            self.mark_remaining()
            print('####### SUCCESS! ######')
        print('')

    def _debug(self):
        for y in range(self.height):
            for x in range(self.width):
                putchar(self._tile_mark(x, y))
            print('')


if __name__ == r'__main__':
    g = Game(9, 9, 10)
    g._debug()
    print('\n\n')
    g.auto_open(5, 5)
    g.show()