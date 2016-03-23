Trepl
====

Trepl is a generic
[Tiered Replication (Cidon et. al)](https://www.usenix.org/conference/atc15/technical-session/presentation/cidon)
implementation, designed to help pick replica placement of
[Kafka](http://kafka.apache.org/) partitions and configure
[WADE](https://github.com/chartbeat-labs/wade) chains. However, it can
be used in any situation where you might want to adjust probability of
data loss / unavailability from multiple replica failures.

Tiered Replication follows up on ideas introduced in the
[Copysets paper](https://www.usenix.org/conference/atc13/technical-sessions/presentation/cidon),
where you'll find detailed information on motivations and use cases:


Usage
----

Basic Trepl usage is simple:

```python
>>> trepl.build_copysets(['node1', 'node2', 'node3'], R=2, S=1)
[['node1', 'node2'], ['node1', 'node3']]

>>> trepl.build_copysets(['node1', 'node2', 'node3'], R=2, S=2)
[['node1', 'node2'], ['node1', 'node3'], ['node2', 'node3']]
```

Trepl also ships with rack and tier aware check functions:

```python
# not rack aware
>>> trepl.build_copysets(['node1', 'node2', 'node3'], R=2, S=1)
[['node1', 'node2'], ['node1', 'node3']]

# rack aware, node1 and node2 can not share a copyset since they're in
# the same rack
>>> rack_map = { 'node1': 'rack1', 'node2': 'rack1', 'node3': 'rack3' }
>>> trepl.build_copysets(
      rack_map.keys(), R=2, S=1,
      checker=trepl.checkers.rack(rack_map),
    )
[['node1', 'node3'], ['node2', 'node3']]

# scatter width must be 2, and data must exist on at least one node in
# the backup tier
>>> primary = ['A', 'B', 'C']
>>> backup = ['d', 'e']
>>> trepl.build_copysets(
      primary + backup, R=2, S=2,
      checker=trepl.checkers.tiered(backup, 2),
    )
[['A', 'd'], ['A', 'e'], ['B', 'd'], ['B', 'e'], ['C', 'd'], ['C', 'e']]
```


Authors
----

- [Wes Chow](https://github.com/wesc)
- [Matt Krukowski](https://github.com/krukowski)
