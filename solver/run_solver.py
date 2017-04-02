#!/usr/bin/env python3
import sys

from game import Game
from solver.simple_solver import SimpleSolver
from solver.set_solver import SetSolver
from solver.common import try_one, benchmark

def usage():
    print("Usage: python3 -m solver.run_solver <solver> <level> [benchmark]")
    print("\tsolver: simple/set")
    print("\tlevel: beginner/intermediate/expert")
    sys.exit(1)


class Factory:
    def __init__(self, solver, game_level):
        self.level = game_level
        self.solver = solver

    def __call__(self, debug):
        if self.level == 'beginner':
            game = Game.beginner()
        elif self.level == 'intermediate':
            game = Game.intermediate()
        elif self.level == 'expert':
            game = Game.expert()
        else:
            usage()

        if self.solver == 'simple':
            solver = SimpleSolver(game, debug)
        elif self.solver == 'set':
            solver = SetSolver(game, debug)
        else:
            usage()

        return game, solver


if __name__ == r'__main__':
    if len(sys.argv) < 3:
        usage()
    solver = sys.argv[1]
    level = sys.argv[2]
    factory = Factory(solver, level)
    if len(sys.argv) > 3 and sys.argv[3] == 'benchmark':
        benchmark(factory)
    else:
        try_one(factory)




