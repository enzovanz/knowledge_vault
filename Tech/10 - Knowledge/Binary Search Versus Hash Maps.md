---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

Binary search and hash maps both support lookup, but exploit different information: binary search uses the order of a sequence, while a hash map computes where a key should be stored. Choose based on the operations the data must support, not lookup complexity alone.

## Explanation

Binary search is an **algorithm** applied to sorted, random-access data. It compares the target with the middle element and discards half of the remaining search interval, giving O(log n) lookup. Because the data remains ordered, the same technique can find boundaries, nearest values, and ranges efficiently.

A hash map is a **data structure** backed by an array and a hash function. The hash of a key determines a candidate storage location; the map then checks the key and resolves any collision using a strategy such as chaining or open addressing. It does not perform binary search. Exact-key lookup is O(1) on average but O(n) in the worst case, and hash order does not naturally support nearest-value or range queries.

| Need | Sorted array with binary search | Hash map |
| --- | --- | --- |
| Exact lookup | O(log n) | O(1) average; O(n) worst case |
| Closest value | O(log n) | O(n) generally |
| Return a range of k matches | O(log n + k) | O(n + k) generally |
| Insert while preserving the representation | O(n) due to shifting | O(1) amortized average |
| Memory overhead | Usually lower | Usually higher |

These lookup costs exclude construction. Sorting unsorted data costs O(n log n), while building a hash map costs O(n) on average. For one lookup, an O(n) linear scan may therefore be cheaper overall; repeated lookups can justify preprocessing. A balanced binary search tree is a third option when both maintained order and frequent insertion or deletion matter.

## Example

Given sorted prices `[10, 20, 30, 40, 50]`, binary search can find the smallest price greater than or equal to `35`—`40`—in O(log n). A hash map can quickly answer whether the exact key `35` exists, but finding its nearest larger key generally requires examining all keys because the map does not preserve their order.

## Connections

- Related: [[Algorithm Analysis and Big O Notation]] — include preprocessing and distinguish average from worst-case bounds when comparing approaches.
- Source: [Binary Search Versus Hashmaps](chatgpt-conversation://6aee0728-75ec-8326-855b-aae151ca1bc3)
