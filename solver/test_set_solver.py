import unittest

from solver.set_solver import *


class TestInformationSetFunctions(unittest.TestCase):
    def test_create_info_from_intersecting_sets(self):
        s = frozenset([(1, 1), (1, 2), (1, 3)])
        t = frozenset([(1, 2), (1, 3), (1, 4)])
        sa = frozenset([(1, 1)])
        ta = frozenset([(1, 4)])
        intersect = frozenset([(1, 2), (1, 3)])
        info = dict()
        info[s] = (1, 1)
        info[t] = (2, 2)
        create_info_from_intersecting_sets(s, t, info)
        self.assertEqual(len(info), 5, "Should have 5 information sets")
        self.assertEqual(info[sa], (0, 0))
        self.assertEqual(info[ta], (1, 1))
        self.assertEqual(info[intersect], (1, 1))

    def test_create_info_from_intersecting_sets2(self):
        s = frozenset([(1, 1), (1, 2), (1, 3)])
        t = frozenset([(1, 2), (1, 3), (1, 4)])
        sa = frozenset([(1, 1)])
        ta = frozenset([(1, 4)])
        intersect = frozenset([(1, 2), (1, 3)])
        info = dict()
        info[s] = (2, 2)
        info[t] = (2, 2)
        create_info_from_intersecting_sets(s, t, info)
        self.assertEqual(len(info), 3, "Should have 5 information sets")
        self.assertEqual(info[intersect], (1, 2))

if __name__ == '__main__':
    unittest.main()