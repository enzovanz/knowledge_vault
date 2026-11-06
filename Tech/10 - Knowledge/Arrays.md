---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

An array stores fixed-size records in a contiguous memory region, allowing any element to be located directly from its index. Arrays provide constant-time indexed access, compact storage, and good memory locality, but fixed arrays cannot grow without allocating new storage.

## Explanation

### Indexing by address

An array is the fundamental contiguously allocated data structure. If the array begins at address B and each record occupies s bytes, the address of element i is:

$$
\operatorname{address}(i) = B + i \cdot s
$$

This calculation is constant time, so reading or replacing an element by index is O(1). It works because every record has the same size and the records occupy consecutive positions. Skiena compares this to equally sized houses arranged in order: knowing the house number is enough to calculate where it is.

### Why arrays are useful

- **Constant-time indexed access:** the index maps directly to an address; no preceding elements need to be traversed.
- **Space efficiency:** fixed-size records do not require a link or boundary marker for every element.
- **Memory locality:** iteration visits nearby addresses, helping the processor reuse data already loaded into its cache.

These properties make arrays foundations for other contiguous structures, including matrices, heaps, and hash tables.

### Fixed and dynamic arrays

A fixed array has a capacity chosen when its memory is allocated. Adding an element beyond that capacity is impossible without allocating another region. Reserving excessive capacity avoids early exhaustion but wastes memory.

A **dynamic array** grows by allocating a larger contiguous array, copying the existing elements, and releasing the old array. If its capacity doubles from m to 2m whenever it fills, one resize costs O(n), but resizes become progressively rarer. Across n appends, the total copying work is O(n), so append costs O(1) **amortized** even though an individual append can cost O(n).

The earliest element can be copied whenever capacity grows from 1 to 2, 2 to 4, 4 to 8, and so on. Most elements arrive much later and move far less: roughly half the elements move at most once, the preceding quarter at most twice, and progressively fewer elements experience every earlier resize. Because capacity doubles, expensive copies become exponentially less frequent as the array grows. The total copying across n appends is therefore O(n), or constant work per append when spread over the whole sequence.

This guarantee applies to every sequence of appends rather than to a probability distribution, which makes it an **amortized** bound rather than an average-case bound.

The array remains contiguous after each resize, but its starting address may change. References or pointers to its old storage can therefore become invalid in languages that expose them.

Indexed reads and replacements remain worst-case O(1). It is **append** that loses a worst-case O(1) guarantee because the particular append that triggers expansion must copy the existing elements.

### Python's `list`

Despite its name, Python's `list` is a dynamic-array abstraction rather than a linked list. In CPython, the contiguous array holds object references—implemented internally as pointers—while the referenced objects may be elsewhere in memory. This representation gives `items[i]` O(1) access, while inserting or deleting near the beginning costs O(n) because later references must shift.

## Example

For an array beginning at address `1000` with four-byte records, element `3` begins at:

```text
1000 + 3 × 4 = 1012
```

The same arithmetic locates any valid index, regardless of the array's length. By contrast, a linked list must follow three links from its head to reach position `3`.

## Connections

- Related: [[Contiguous Versus Linked Data Structures]] — contrasts array-based storage with nodes connected by pointers.
- Related: [[Algorithm Analysis and Big O Notation]] — dynamic-array append is a standard example of amortized analysis.
- Related: [[Binary Search Versus Hash Maps]] — binary search depends on an array's efficient indexed access.
- Source: [[The Algorithm Design Manual]], second edition, §3.1.1, printed pp. 66–68 (PDF pages 78–80). [Reading PDF](https://sureshcseit.wordpress.com/wp-content/uploads/2021/04/skienathealgorithmdesignmanual.pdf#page=78).
