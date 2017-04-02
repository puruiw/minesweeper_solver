import sys

import numpy as np

from solver.simple_solver import SimpleSolver


def range_intersection(range1, range2):
    return max(range1[0], range2[0]), min(range1[1], range2[1])


def _useless_info(set, range):
    return range[0] <= 0 and range[1] >= len(set)


def update_info(info, tile_set, mine_range):
    if tile_set in info:
        if info[tile_set][0] < mine_range[0] or info[tile_set][1] > mine_range[1]:
            info[tile_set] = range_intersection(info[tile_set], mine_range)
            return True
    else:
        info[tile_set] = mine_range
        return True
    return False


def get_range(info, tile_set):
    if tile_set in info:
        return info[tile_set]
    return (0, len(tile_set))


def create_info_from_subset(super_set, sub, current_info, new_info):
    remain = super_set - sub
    super_range = get_range(current_info, super_set)
    sub_range = get_range(current_info, sub)
    remain_min = max(0, super_range[0] - sub_range[1])
    remain_max = min(len(remain), super_range[1] - sub_range[0])
    if not _useless_info(remain, (remain_min, remain_max)):
        update_info(new_info, remain, (remain_min, remain_max))


def create_info_from_intersecting_sets(s, t, current_info, new_info):
    intersect = s & t
    sa = s - intersect
    ta = t - intersect
    s_range = get_range(current_info, s)
    t_range = get_range(current_info, t)
    intersect_min = max(0, s_range[0] - len(sa), t_range[0] - len(ta))
    intersect_max = min(len(intersect), s_range[1], t_range[1])
    if not _useless_info(intersect, (intersect_min, intersect_max)):
        update_info(new_info, intersect, (intersect_min, intersect_max))
    create_info_from_subset(s, intersect, current_info, new_info)
    create_info_from_subset(t, intersect, current_info, new_info)


# TODO: a better random open function can easily improve our success rate.
# - at the beginning, using a 2-D normal distribution to open from center
# - later: chose the set that gaves us best chance (less mine/total ratio)
class SetSolver(SimpleSolver):
    def __init__(self, game, debug):
        super().__init__(game, debug)

    def solve_step(self):
        information = {}
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
                unknown_mines = state - marked
                information[frozenset(unknowns)] = (unknown_mines, unknown_mines)
        while self.solve_sets(information):
            if self.clean_solved_sets(information):
                return
        # self.random_open(information)
        super().random_open()

    def random_open(self, information):
        # try to find a set with lowest risk.
        lowest_risk = 1
        for k in information.keys():
            risk = float(information[k][1]) / len(k)
            if risk < lowest_risk:
                lowest_risk = risk
                best = k

        mean_risk = (self.game.mines - self.game.marked) / (self.game.width * self.game.height - self.game.marked - self.game.opened)
        if lowest_risk < mean_risk:
            i = np.random.randint(0, len(best))
            x, y = list(best)[i]
            if self.game.get_state(x, y) == -2:
                self.game.open(x, y)
                return
            else:
                print("ALREADY OPENED? SHOULD NOT HAPPEN!", file=sys.stderr)
        #super().random_open()
        self.open_center()

    # low performance
    def open_center(self):
        closest = self.game.width + self.game.height
        for x in range(self.game.width):
            for y in range(self.game.height):
                state = self.game.get_state(x, y)
                if state == -2:
                    distance = abs(x - self.game.width / 2) + abs(y - self.game.height / 2)
                    if distance < closest:
                        closest = distance
                        best = (x, y)
        self.game.open(best[0], best[1])

    @staticmethod
    def solve_sets(information):
        new_info = {}
        for s in information.keys():
            for t in information.keys():
                if s == t:
                    continue
                if s > t:
                    create_info_from_subset(s, t, information, new_info)
                elif t > s:
                    create_info_from_subset(t, s, information, new_info)
                elif t & s:
                    create_info_from_intersecting_sets(s, t, information, new_info)

        found_info = False
        if new_info:
            for k in new_info.keys():
                if update_info(information, k, new_info[k]):
                    found_info = True
        return found_info

    def clean_solved_sets(self, information):
        found = []
        for k in information.keys():
            if information[k][1] == 0:
                self._open_all(k)
                found.append(k)
            elif len(k) == information[k][0]:
                self._mark_all(k)
                found.append(k)
        if found:
            for k in found:
                del information[k]
            return True
