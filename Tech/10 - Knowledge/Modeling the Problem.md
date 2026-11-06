---
type: concept
domain: data structures and algorithms
created: 2026-11-04
---
## Summary

Modeling an algorithmic problem means translating its application-specific objects and rules into standard mathematical structures. Recognizing these structures helps you find known problems and algorithms, even when they come from a different application.

## Explanation

Before choosing an algorithm, identify the inputs, the required output, the constraints that make an answer valid, and any objective to minimize or maximize. Then ask which structures preserve the relationships that matter.

### Recognizing common objects

| Object | What it represents | Clues in a problem |
| --- | --- | --- |
| **Permutation** | An ordering of a fixed set of items; changing the order changes the answer. | Arrangement, tour, ordering, sequence |
| **Subset** | A selection of items; order does not matter. | Collection, committee, group, packaging, selection |
| **Tree** | A hierarchy with parent–child relationships; as a graph, it is connected and has no cycles. | Hierarchy, ancestry, taxonomy |
| **Graph** | Objects represented by vertices and pairwise relationships represented by edges. Edges may have directions or weights. | Network, circuit, connections, relationships |
| **Points** | Locations in a geometric space, described by coordinates. | Sites, positions, locations, records interpreted as feature vectors |
| **Polygons / polyhedra** | Regions with boundaries formed by line segments in two dimensions or polygonal faces in three dimensions. | Shapes, regions, boundaries |
| **String** | An ordered sequence of symbols, where symbols may repeat. | Text, characters, patterns, labels |

These clues suggest models; they do not establish them. A sequence with repeated items is not necessarily a permutation, a network with cycles is not a tree, and an arbitrary shape need not be polygonal. Verify the actual constraints.

The input and the solution may use different objects. A graph can describe the input while a permutation describes the order in which to visit its vertices. Also distinguish the mathematical model from its implementation: the same graph can be stored as an adjacency list or an adjacency matrix.

Once the model is precise, search for the structure **and the task**—for example, shortest path in a weighted graph—rather than only the application's terminology. Check that a known algorithm's assumptions match your constraints.

## Example

A courier must visit every delivery stop once and return to the depot while minimizing travel cost.

- Model stops as **vertices** and available travel connections as **weighted edges**. Coordinates can describe the stops as points, but road travel costs may differ from straight-line distance.
- Model a candidate visiting order as a **permutation** of the delivery stops, with the depot fixed at the beginning and end.
- Require every stop to appear exactly once and minimize the total travel cost, including the return trip.

This formulation reveals a traveling salesperson problem. Asking only for the cheapest route between two stops would instead lead to a shortest-path problem; recognizing a graph alone is not enough to choose an algorithm.

## Connections

- Related: [[Recursive Objects]] — decompose standard structures into smaller objects of the same type.
- Source: [[The Algorithm Design Manual]] by Steven S. Skiena
