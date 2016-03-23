"""Implementation of Tiered Replication algorithm:

https://www.usenix.org/conference/atc15/technical-session/presentation/cidon

"""

from collections import defaultdict
from . import checkers


def build_copysets(nodes, R, S, checker=None, copysets=[]):
    """Returns a list of copysets, where a copyset is a list of R elements
    drawn from nodes.

    The algorithm attemps to minimize the number of copysets such that
    nodes have a minimum scatter width of S. See the cited paper for
    details.

    nodes: list of hashable elements (typically string or int, up to you)
    R: number of nodes per copyset
    S: minimum scatter width
    checker: constraints function (see default_checker)
    copysets: an initial set of copysets

    """

    checker = checker or checkers.default
    nodes = sorted(nodes)
    copysets = list(copysets)
    done = False

    scatter_widths = defaultdict(int)

    while not done:
        modified = False
        for node in nodes:
            if scatter_widths[node] >= S:
                continue

            copyset = set([node])
            sorted_nodes = sorted(
                (scatter_widths[n], n) for n in nodes if n != node
            )
            for _, n in sorted_nodes:
                copyset.add(n)
                if not checker(copysets, copyset) or copyset in copysets:
                    copyset.remove(n)
                    continue

                if len(copyset) == R:
                    copysets.append(copyset)
                    modified = True
                    break

            scatter_sets = defaultdict(set)
            for s in copysets:
                s = set(s)
                for n in s:
                    scatter_sets[n] |= s - set([n])

            scatter_widths.update({k: len(v) for k, v in scatter_sets.iteritems()})

        if not modified:
            # We failed to change anything in this pass, that means satisfying
            # the constraints is impossible.
            raise ValueError('Couldn\'t create valid copysets')
        done = all(
            scatter_widths[n] >= S for n in nodes
        )

    return sorted(sorted(s) for s in copysets)


