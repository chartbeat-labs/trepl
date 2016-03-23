"""Implementations of useful checkers."""


from functools import partial


def default(copysets, copyset):
    """Check that always passes.

    The check function checks for custom constraints, such as rack or
    tier awareness. 'copysets' contains a list of copysets
    build_copysets has generated so far, and 'copyset' is the copyset
    that build_copysets wants to check as a valid.

    This is the default check, meaning we don't care about constraints
    such as rack awareness.

    """

    return True


def rack(rack_map, spread=None, R=None, allow_greater=False):
    """Returns a rack aware checker.

    The checker ensures that it is possible to construct a set (of
    length R) including given set s that contains nodes from exactly
    `spread` racks (or greater, if allow_greater is True).

    `rack_map` is a map of node id -> rack id. There should be an entry for
    every possible node, and rack id is any object that is hashable
    (typically an int or string).

    `spread` and `R` both default to len(s) (i.e. each node must be in a
    different rack).

    A typical invocation looks something like:

        build_copysets(rack_map.keys(), 6, 2,
                       checker=rack(rack_map))

    """

    def _checker(rack_map, spread, R, allow_greater, copysets, copyset):
        if spread:
            if R:
                # As we're building up the set, we relax the restrictions
                # because we just need to check if it's possible to build a
                # copyset that includes the given one. As the len(s) approaches
                # R, target_spread approaches the given spread.
                target_spread = spread - R + len(copyset)
            else:
                target_spread = spread
        if not spread:
            spread = len(copyset)
            target_spread = spread

        racks = set()
        for node in copyset:
            try:
                r = rack_map[node]
            except KeyError:
                print "ERROR: no rack mapping for node '%s'" % node
                print
                raise
            racks.add(r)

        if allow_greater:
            return len(racks) >= target_spread
        else:
            return len(racks) >= target_spread and len(racks) <= spread

    return partial(_checker, rack_map, spread, R, allow_greater)


def tiered(backup_tier, R):
    """Returns a tier aware checker.

    The returned checker ensures that it's possible to construct a set
    (of length R) including given set s that will contain exactly one
    node from the backup tier.

    `backup_tier` is a list of node ids that count as backups.

    A typical invocation looks something like:

        build_copysets(primary_tier + backup_tier, 6, 2,
                       checker=tiered(backup_tier, 6))

    """

    def _checker(backup_tier, R, copysets, copyset):
        num_backups = len(copyset.intersection(set(backup_tier)))
        if len(copyset) < R:
            return num_backups <= 1
        else:
            return num_backups == 1

    return partial(_checker, backup_tier, R)


def composed(*checkers):
    """Returns a checker that is composed of a other checkers.

    The returned checker ensures that all of the supplied checkers
    pass.

    """

    def _checker(copysets, copyset):
        return all(c(copysets, copyset) for c in checkers)

    return _checker
