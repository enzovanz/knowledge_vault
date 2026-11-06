---
type: concept
domain: data structures and algorithms
created: 2026-11-04
---
## Summary

A recursive object can be described in terms of smaller objects of the same type. Recognizing this structure helps turn a problem into smaller instances that can be solved using the same reasoning.

## Explanation

A recursive description needs a **decomposition rule** that exposes smaller objects and **base cases** that describe the simplest objects directly. Each decomposition must make progress toward a base case—for example, by reducing the number of elements.

| Object | Decomposition | Possible base case |
| --- | --- | --- |
| **Permutation** | Remove the first item; the remaining sequence is a permutation of the remaining items. | The empty permutation |
| **Subset** | For a subset of `{1, …, n}`, remove `n` if present; what remains is a subset of `{1, …, n − 1}`. | The empty set, the only subset of an empty universe |
| **Tree** | Remove the root of a rooted tree to expose its child subtrees, or remove a leaf to leave a smaller tree. | A single vertex |
| **Graph** | Remove a vertex and its incident edges, or partition the vertices into two smaller groups and separate the edges crossing between them. | An empty graph or a single vertex |
| **Point set** | Partition the points into two smaller sets, such as by a separating line when possible. | An empty set or a single point |
| **Simple polygon** | Split along a diagonal whose interior lies inside the polygon, producing two smaller polygons. | A triangle |
| **String** | Remove the first character to leave a shorter string. | The empty string |

Keep the information needed to reconstruct the original object or combine results. For example, separating a graph into two parts does not make them independent: the crossing edges may still affect the answer. For subsets, record whether `n` was present; otherwise, two different subsets can reduce to the same smaller subset.

Base cases depend on the object's definition and the task. Empty strings and permutations are valid objects, while a genuine simple polygon needs at least three vertices. Whichever convention you choose, the decomposition must reach a case you handle explicitly.

A recursive structure suggests an algorithm, but does not establish its correctness or efficiency. You still need to show how solutions to the smaller instances produce the required answer.

## Example

To count the characters in `"cat"`, separate the first character from the remaining string and count the remainder in the same way:

```text
length("") = 0
length(first + rest) = 1 + length(rest)

length("cat") = 1 + length("at")
              = 2 + length("t")
              = 3 + length("")
              = 3
```

The remainder is always another string, each step removes one character, and the empty string stops the decomposition.

## Connections

- Related: [[Modeling the Problem]] — after identifying a mathematical structure, look for smaller instances of that same structure.
- Source: [[The Algorithm Design Manual]] by Steven S. Skiena
