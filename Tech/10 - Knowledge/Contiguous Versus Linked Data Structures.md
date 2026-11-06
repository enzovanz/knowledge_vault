---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

Data structures can be classified by whether they use one contiguous slab of memory or separate chunks connected by pointers. This representation choice shapes indexed access, memory use, cache behavior, and how the structure grows or changes.

## Explanation

### Contiguous structures

Contiguously allocated structures use [[Arrays]] as their foundation. Examples include arrays, matrices, heaps, and hash tables. Their adjacent, fixed-size records support direct indexed access, compact storage, and good memory locality. A fixed array has a predetermined capacity; a dynamic array can grow by occasionally allocating a larger region and copying its elements.

### Linked structures

Linked structures consist of distinct memory chunks connected by [[Pointers]]. Lists, trees, and graph adjacency lists are common examples. Each node contains the stored data and at least one pointer to another node; the structure also needs an entry pointer, such as the head of a linked list.

This representation can grow one node at a time and can insert or remove a known node by changing a small number of pointers. The trade-offs are pointer storage, allocation overhead, weaker memory locality, and the lack of direct indexed access. Reaching the element at position i in a linked list takes O(i), even though following one known link is O(1). A doubly linked list spends another pointer per node to make movement and some updates in both directions easier.

### Python naming warning

The word **list** names different representations in theory and in Python:

- **In this classification:** a list means a linked structure made of nodes and pointers.
- **In Python:** `list` is a dynamic-array abstraction, not a linked list. See [[Arrays#Python's `list`]] for its representation and complexity consequences.

A linked list must be implemented separately when that representation is required.

| Property | Contiguous representation | Linked representation |
| --- | --- | --- |
| Random access by index | O(1) | O(n) |
| Sequential traversal | Usually cache-friendly | Often less cache-friendly |
| Insert or remove at a known position | O(n) when elements must shift | O(1) for a list after locating the relevant node |
| Per-element overhead | Low | References and often allocation metadata |
| Growth | May require reallocation and copying | Add nodes individually |

The table describes typical arrays and linked lists rather than every structure in each family. The important distinction is between the abstract operations a program needs and the representation used to implement them: a favorable update cost does not help if finding the update position dominates the work.

## Example

Consider inserting `X` after `B`:

```text
Array:       [A][B][C][D]  →  [A][B][X][C][D]
Linked list: A → B → C → D  →  A → B → X → C → D
```

The array may need to shift `C` and `D` one position to the right. If a linked-list operation already has a pointer to node `B`, it creates `X` and changes links. Finding `B` by position would still require traversing the list, while the array can access it directly by index.

## Connections

- Related: [[Algorithm Analysis and Big O Notation]] — separate the cost of locating a position from the cost of modifying it.
- Related: [[Binary Search Versus Hash Maps]] — binary search relies on efficient indexed access, while hash maps commonly use array-backed storage internally.
- Source: [[The Algorithm Design Manual]], second edition, §3.1, printed pp. 66–71 (PDF pages 78–83). [Reading PDF](https://sureshcseit.wordpress.com/wp-content/uploads/2021/04/skienathealgorithmdesignmanual.pdf#page=78).
