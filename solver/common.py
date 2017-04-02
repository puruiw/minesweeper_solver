import time

def try_one(factory):
    game, solver = factory(True)
    solver.solve()


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