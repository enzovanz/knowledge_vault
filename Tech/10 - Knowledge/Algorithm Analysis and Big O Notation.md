---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

Algorithm analysis describes how an algorithm's resource use grows with input size. Big O gives an asymptotic upper bound; paired with worst-case analysis, it helps estimate how well an algorithm scales without timing every possible input.

## Explanation

### RAM model of computation

The **Random Access Machine (RAM)** is an idealized computer for counting work independently of a particular language or processor:

- Basic operations on machine-sized values, such as arithmetic, comparisons, and assignments, cost constant time.
- Accessing a memory location costs constant time; the model assumes sufficient memory and ignores cache and disk differences.
- A loop or subroutine costs the work it actually performs, rather than counting as one operation.

Define the input size **n** first: array length, number of vertices, or number of input bits, depending on the problem. Counting steps gives a function T(n), not an exact prediction in seconds. Arbitrarily large integers and expensive memory transfers may require a more detailed model.

### Cases and bounds answer different questions

For inputs of the **same size n**, the case selects which cost to study:

| Case | Cost selected |
| --- | --- |
| Best | Minimum work among inputs of size n |
| Worst | Maximum work among inputs of size n |
| Average | Expected work under a stated probability distribution over inputs |

The notation then bounds the growth of that selected function:

| Notation | Meaning | For all sufficiently large n, with positive constants |
| --- | --- | --- |
| O(g(n)) | Upper bound | T(n) ≤ c · g(n) |
| Ω(g(n)) | Lower bound | T(n) ≥ c · g(n) |
| Θ(g(n)) | Tight bound: both upper and lower | c₁ · g(n) ≤ T(n) ≤ c₂ · g(n) |

**Big O does not mean worst case, and Ω does not mean best case.** All three notations can describe any case. A worst-case upper bound is especially useful because it limits growth even for unfavorable inputs; Θ gives more information when a matching lower bound is known.

Constants and lower-order terms disappear in asymptotic classification: 4n² + 7n + 12 is Θ(n²). It is also O(n³), but that upper bound is looser. These bounds apply beyond some threshold n₀, so they do not determine which implementation wins on small inputs.

### Growth rates and dominance

From fastest-growing to slowest-growing:

$$
n! \succ 2^n \succ n^3 \succ n^2 \succ n\log n \succ n \succ \log n \succ 1
$$

Here **f ≻ g** means f eventually outgrows every constant multiple of g: g(n)/f(n) approaches zero. This is an asymptotic relationship, not a claim that the inequality holds for every small n. In a sum, the fastest-growing term determines the growth class.

| Representative function | Growth class | Typical source of work | n = 10 | n = 100 | n = 1,000 |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | Constant | Read one array position | 1 | 1 | 1 |
| log₂ n | Logarithmic | Repeatedly halve a search interval | 3.32 | 6.64 | 9.97 |
| n | Linear | Visit every item | 10 | 100 | 1,000 |
| n log₂ n | Linearithmic | Merge sort | 33.2 | 664 | 9,966 |
| n² | Quadratic | Consider every pair | 100 | 10,000 | 1,000,000 |
| n³ | Cubic | Consider every triple | 1,000 | 1,000,000 | 1,000,000,000 |
| 2ⁿ | Exponential | One constant-time action per subset | 1,024 | ≈ 1.27 × 10³⁰ | ≈ 1.07 × 10³⁰¹ |
| n! | Factorial | One constant-time action per permutation | 3,628,800 | ≈ 9.33 × 10¹⁵⁷ | ≈ 4.02 × 10²⁵⁶⁷ |

Values are calculated function values, rounded where needed, rather than measured runtimes. Writing out every subset or permutation explicitly adds the cost of producing its elements. Logarithm bases differ by a constant factor, so they have the same asymptotic class.

![Common growth rates on a linear scale](../../97%20-%20Assets/Algorithm%20analysis%20growth%20rates.svg)

The linear scale shows how quickly large functions leave a fixed work budget; curves that exceed the vertical range are clipped. The curves represent functions with coefficient 1, not every algorithm in each class.

**Take-home lesson:** Learn these common growth classes first; they cover most everyday algorithm analysis. Constants still affect actual runtime, but a faster-growing function eventually overwhelms any fixed constant advantage.

## Example

Search an unsorted array from left to right, stopping at the first match:

- **Best case:** the first item matches, so the work is Θ(1).
- **Worst case:** the item is absent or last, requiring n checks, so the work is Θ(n).
- **Average case:** if the item occurs exactly once and each position is equally likely, the expected checks are (n + 1)/2, also Θ(n).

Thus the worst-case cost is both O(n) and Ω(n). Doubling n roughly doubles the worst-case work; a quadratic algorithm would instead grow by roughly four times.

## Connections

- Related: [[Modeling the Problem]] — define the input and its size before analyzing an algorithm.
- Source: [[The Algorithm Design Manual]], second edition, chapter 2, §§2.1–2.3 (printed pp. 31–40; PDF pages 43–52). [Reading PDF](https://sureshcseit.wordpress.com/wp-content/uploads/2021/04/skienathealgorithmdesignmanual.pdf#page=43).
