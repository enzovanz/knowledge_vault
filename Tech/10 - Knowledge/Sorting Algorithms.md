---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

Sorting algorithms arrange elements in a chosen order, such as smallest to largest. This note collects each method's intuition, Python implementation, and time and space costs.

| Algorithm | Worst-case time | Auxiliary space | Implementation difficulty | Main detail to get right |
| --- | --- | --- | --- | --- |
| [Bubble Sort](#bubble-sort) | O(n²) | O(1) | Easy | Compare adjacent elements and shrink the unsorted range after each pass. |
| [Selection Sort](#selection-sort) | O(n²) | O(1) | Easy | Track the smallest element's index, then swap once per pass. |
| [Insertion Sort](#insertion-sort) | O(n²) | O(1) | Slightly trickier | Save the current element before shifting larger elements, then insert it into the gap. |

These bounds describe the implementations below. Here, **n** is the number of elements. Auxiliary space excludes the input list.

## Bubble Sort

### How it works

Compare neighboring elements and swap them when they are out of order. After one pass, the largest element in the unsorted portion has moved to its final position at the right end. Repeat over the remaining portion, stopping early if a pass makes no swaps.

For example, sorting `[3, 2, 1]`:

```text
First pass:  [3, 2, 1] → [2, 3, 1] → [2, 1, 3]
Second pass: [2, 1, 3] → [1, 2, 3]
```

### Implementation (Python)

This implementation modifies the list in place and returns `None`.

```python
def bubble_sort(items: list[int]) -> None:
    for end in range(len(items) - 1, 0, -1):
        swapped = False

        for i in range(end):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True

        if not swapped:
            break
```

### Complexity analysis

Here, **n** is the number of elements; comparisons and swaps are assumed to cost constant time.

- **Time complexity: O(n²) worst case and on average** for uniformly random orderings of distinct elements. Repeated passes compare neighboring elements, with up to `(n − 1) + (n − 2) + … + 1 = n(n − 1)/2` comparisons. **O(n) best case:** an already sorted list needs only one pass because no swaps occur.
- **Space complexity: O(1) auxiliary space.** Sorting uses the original list and a fixed number of variables, without allocating another list.

## Selection Sort

### How it works

Find the smallest element in the unsorted portion and swap it into the first unsorted position. Each pass extends the sorted portion on the left by one element.

For example, sorting `[3, 1, 2]`:

```text
First pass:  [3, 1, 2] → [1, 3, 2]  (select 1)
Second pass: [1, 3, 2] → [1, 2, 3]  (select 2)
```

### Implementation (Python)

This implementation modifies the list in place and returns `None`.

```python
def selection_sort(items: list[int]) -> None:
    for start in range(len(items) - 1):
        smallest = start

        for i in range(start + 1, len(items)):
            if items[i] < items[smallest]:
                smallest = i

        if smallest != start:
            items[start], items[smallest] = items[smallest], items[start]
```

### Complexity analysis

- **Time complexity: O(n²) in the best, average, and worst cases.** Finding each minimum requires scanning the remaining unsorted portion, giving `(n − 1) + (n − 2) + … + 1` comparisons even when the list is already sorted. There are at most `n − 1` swaps.
- **Space complexity: O(1) auxiliary space.** The algorithm rearranges the original list using a fixed number of index variables.

## Insertion Sort

### How it works

Build a sorted portion on the left, starting with the first element. Take the next element, shift larger elements in the sorted portion one position to the right, and insert it into the gap. Repeat until every element has been inserted.

For example, sorting `[3, 1, 2]`:

```text
Insert 1: [3, 1, 2] → [1, 3, 2]
Insert 2: [1, 3, 2] → [1, 2, 3]
```

### Implementation (Python)

This implementation modifies the list in place and returns `None`.

```python
def insertion_sort(items: list[int]) -> None:
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1

        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            j -= 1

        items[j + 1] = current
```

### Complexity analysis

- **Time complexity: O(n²) worst case and on average** for uniformly random orderings of distinct elements. Each insertion may shift all preceding elements; reverse order requires `1 + 2 + … + (n − 1)` shifts. **O(n) best case:** an already sorted list requires one comparison per insertion and no shifts.
- **Space complexity: O(1) auxiliary space.** Only the current element and a fixed number of index variables are stored outside the original list.

## Connections

- Related: [[Algorithm Analysis and Big O Notation]] — interpret time and space bounds and distinguish best-case from worst-case costs.
