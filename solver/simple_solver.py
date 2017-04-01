import time
import numpy as np
from game import Game


class SimpleSolver:
    def __init__(self, game, debug=False):
        self.game = game
        self.debug = debug
        self.solved_tiles = set()

    def solve(self):
        while not self.game.boom and not self.game.success():
            self.solve_step()
            if self.debug:
                if self.game.success():
                    self.game.mark_remaining()
                self.game.show()

    def nearby_by_status(self, x, y, state):
        return [(p, q) for (p, q) in self.game.nearby(x, y) if self.game.get_state(p, q) == state]

    def count_nearby_by_status(self, x, y, status):
        return len(self.nearby_by_status(x, y, status))

    def _open_all(self, tiles):
        for (p, q) in tiles:
            self.game.open(p, q)

    def _mark_all(self, tiles):
        for (p, q) in tiles:
            self.game.mark(p, q)

    def solve_step(self):
        for x in range(self.game.width):
            for y in range(self.game.height):
                state = self.game.get_state(x, y)
                if state < 0: # not opened yet
                    continue
                if (x, y) in self.solved_tiles:
                    continue
                unknowns = self.nearby_by_status(x, y, -2)
                if not unknowns:
                    self.solved_tiles.add((x, y))
                    continue

                marked = self.count_nearby_by_status(x, y, -1)
                if marked == state:
                    self._open_all(unknowns)
                    return
                if len(unknowns) == state - marked:
                    self._mark_all(unknowns)
                    return
        self.random_open()

    def random_open(self):
        for x in range(self.game.width):
            for y in range(self.game.height):
                if self.game.get_state(x, y) == -2:
                    self.game.open(x, y)
                    return


def benchmark(factory, loops=1000):
    success = 0
    start = time.time()
    for i in range(loops):
        game, solver = factory(False)
        solver.solve()
        if game.success():
            success += 1
        if (i + 1) % 10 == 0 or i == loops - 1:
            print("%d games, %d success, %f success rate, %f seconds" % (
                i + 1, success, success / (i + 1), time.time() - start))


def try_one(factory):
    game, solver = factory(True)
    solver.solve()


def simple_solver_factory(debug):
    game = Game.expert()
    return game, SimpleSolver(game, debug)

if __name__ == r'__main__':
    benchmark(simple_solver_factory())