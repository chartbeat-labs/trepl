import unittest
from itertools import combinations
from collections import defaultdict

from trepl import build_copysets
from trepl import checkers


class TreplTest(unittest.TestCase):
    def _test(self, N, R, S):
        copysets = build_copysets(
            range(N),
            R,
            S,
        )
        self._validate_copysets(copysets, R, S)

    def _validate_copysets(self, copysets, R, S):
        self.assertTrue(self._all_unique(copysets))
        self.assertEqual(self._get_R(copysets), R)
        self.assertGreaterEqual(min(self._get_S(copysets).values()), S)

    def test_simple(self):
        max_N = 20
        for N in range(3, max_N + 1):
            print "testing N=%d out of %d" % (N, max_N)
            for R in range(2, N + 1):
                for S in range(1, N):
                    self._test(N, R, S)

    def _all_unique(self, copysets):
        """Checks that each copyset is unique."""

        return all(
            c1 != c2 for c1, c2 in combinations(copysets, 2)
        )

    def _get_R(self, copysets):
        """Returns the size of each copyset if they're all the same
        size. Otherwise, raises error.

        """

        sizes = [
            len(c) for c in copysets
        ]

        if not sizes:
            raise ValueError("can't calculate R for empty copysets")

        if all(s == sizes[0] for s in sizes):
            return sizes[0]
        else:
            raise ValueError("copysets are of different length")

    def _get_S(self, copysets):
        """Returns a node -> scatter width map for the given copysets."""

        nodes = defaultdict(set)
        for s in copysets:
            for n in s:
                nodes[n] |= set(s) - set([n])

        r = {node: len(scatter_set) for node, scatter_set in nodes.iteritems()}
        return r

    def test_rack_checker(self):
        rack_map = {'A': 0,
                    'B': 0,
                    'C': 0,
                    'D': 1,
                    'E': 1,
                    'F': 1,
                    'G': 2,
                    'H': 2,
                    'I': 2}
        copysets = build_copysets(
            rack_map.keys(), 3, 2,
            checkers.rack(rack_map),
        )

        self._validate_copysets(copysets, 3, 2)
        for s in copysets:
            racks = set([rack_map[n] for n in s])
            self.assertEqual(len(racks), 3)

        # This somewhat complicated-looking example could represent a
        # a situation in which you have 6 machines spread across 3 racks,
        # with each node running 2 processes. A reasonable configuration
        # would be to ensure that each resulting set contains nodes from
        # at least 2 different racks, and no two nodes from the same machine.
        machine_map = {'A:0': 'A',
                       'A:1': 'A',
                       'B:0': 'B',
                       'B:1': 'B',
                       'C:0': 'C',
                       'C:1': 'C',
                       'D:0': 'D',
                       'D:1': 'D',
                       'E:0': 'E',
                       'E:1': 'E',
                       'F:0': 'F',
                       'F:1': 'F'}
        rack_map = {'A:0': 0,
                    'A:1': 0,
                    'B:0': 0,
                    'B:1': 0,
                    'C:0': 1,
                    'C:1': 1,
                    'D:0': 1,
                    'D:1': 1,
                    'E:0': 2,
                    'E:1': 2,
                    'F:0': 2,
                    'F:1': 2}
        copysets = build_copysets(
            rack_map.keys(), 3, 4,
            checkers.composed(
                checkers.rack(machine_map),
                checkers.rack(
                    rack_map,
                    spread=2,
                    R=3,
                    allow_greater=False),
            ),
        )
        self._validate_copysets(copysets, 3, 4)
        for s in copysets:
            racks = set([rack_map[n] for n in s])
            machines = set([machine_map[n] for n in s])
            self.assertEqual(len(machines), 3)
            self.assertGreaterEqual(len(racks), 2)

    def test_tiered_checker(self):
        primary_tier = ['A', 'B', 'C', 'D', 'E', 'F']
        backup_tier = ['G', 'H', 'I']

        copysets = build_copysets(
            primary_tier + backup_tier, 4, 6,
            checkers.tiered(backup_tier, 4),
        )

        self._validate_copysets(copysets, 4, 6)
        for s in copysets:
            backup_count = len(set([n for n in s if n in backup_tier]))
            self.assertEqual(backup_count, 1)


if __name__ == '__main__':
    unittest.main()
