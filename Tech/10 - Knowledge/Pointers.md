---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

A pointer is a value representing a memory address. Pointers let a program refer to existing data instead of copying it and provide the connections between separately allocated nodes in linked data structures.

## Explanation

In C, a pointer has a type describing the kind of value expected at the address it stores. Given:

```c
int x = 42;
int *p = &x;
```

- **`x`** names the integer variable and evaluates to its value, `42`.
- **`&x`** uses the address-of operator to produce the memory address where `x` lives.
- **`p`** is a pointer variable. Its value is the address of `x`.
- **`*p`** uses the dereference operator to access the integer stored at the address held by `p`.
- **`&p`** is the address of the pointer variable itself, not the address stored inside it.

The `*` symbol has two related uses in C. In the declaration `int *p`, it declares `p` as a pointer to an integer. In an expression such as `*p`, it dereferences the pointer. Assigning through the pointer, as in `*p = 7`, changes `x` because both expressions refer to the same memory location.

Pointers enable linked structures because a node can store the address of another node. A linked list, for example, needs a pointer to its first node, and each node stores a pointer to its successor. The special value `NULL` represents the absence of a valid target and commonly marks the end of a structure.

Pointer syntax and capabilities vary across languages. Python normally exposes **references** instead of raw memory addresses, while C permits explicit address manipulation. Regardless of syntax, the central distinction remains: the pointer has its own address and stores another address as its value.

## Example

Assume `x` lives at address `0x1000`, while pointer variable `p` lives at `0x2000` and points to `x`:

| Expression | Meaning | Result |
| --- | --- | --- |
| `x` | Value stored in variable `x` | `42` |
| `&x` | Address where `x` lives | `0x1000` |
| `p` | Address stored as the value of pointer `p` | `0x1000` |
| `&p` | Address where pointer variable `p` lives | `0x2000` |
| `*p` | Value found by following the address stored in `p` | `42` |

The memory relationship is:

```text
Address    Variable    Stored value
0x1000     x           42
0x2000     p           0x1000 ──────► x
```

Thus `p == &x`, but `&p != &x`; and `*p == x`.

### Pointers as connections between nodes

A singly linked-list node shows how pointers connect separate pieces of memory:

```c
typedef struct list {
    item_type item;      /* stored data */
    struct list *next;   /* pointer to the next node */
} list;

list *head = NULL;
```

Each node contains:

- `item`, one or more fields holding the useful data;
- `next`, a pointer whose value is the address of another `list` node; and
- an external pointer such as `head`, which provides the entry point to the structure.

If `head` points to node `A`, `A.next` points to `B`, and `B.next` is `NULL`, the structure is:

```text
head
  │
  ▼
┌──────────┐      ┌──────────┐
│ item: A  │      │ item: B  │
│ next: ───┼─────►│ next: NULL
└──────────┘      └──────────┘
```

The nodes need not be adjacent in memory; their stored addresses establish the logical order. This flexibility costs space because every node stores pointer fields in addition to data. A doubly linked node stores pointers to both its successor and predecessor, trading another pointer per node for easier movement and updates in both directions.

## Connections

- Related: [[Contiguous Versus Linked Data Structures]] — pointers connect the separately allocated nodes of linked structures.
- Related: [[Arrays]] — array indexes calculate addresses implicitly, whereas pointers hold addresses explicitly.
- Source: [[The Algorithm Design Manual]], second edition, §3.1.2, printed pp. 68–69 (PDF pages 80–81). [Reading PDF](https://sureshcseit.wordpress.com/wp-content/uploads/2021/04/skienathealgorithmdesignmanual.pdf#page=80).
