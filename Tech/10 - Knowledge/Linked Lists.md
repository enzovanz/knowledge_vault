---
type: concept
domain: data structures and algorithms
created: 2026-11-06
---
## Summary

A linked list stores a sequence as separately allocated nodes, with each node holding data and a pointer to its successor. It can grow and reconnect nodes without shifting contiguous elements, but reaching a position or searching for a value requires following links from the head.

## Explanation

A **singly linked list** has a head reference that identifies its first node. Each node contains:

- a value, which is the data the list exists to store; and
- a `next` pointer, which points to the successor node or is `NULL` at the end.

![Linked list nodes with data and pointer fields](../../97%20-%20Assets/Linked%20list%20nodes%20and%20pointers.png)

The links determine the logical order even when the nodes occupy unrelated memory locations. Unlike an array, a linked list cannot calculate the location of node i directly: it must begin at the head and follow i links. Access by position and search are therefore O(n) in the worst case.

In C, a minimal node type can be represented as:

```c
typedef int item_type;

typedef struct list {
    item_type item;
    struct list *next;
} list;
```

`item` holds the data, while `next` stores the address of another node of the same type. A separate `list *` variable stores the head address that provides access to the whole structure; see [[Pointers]] for the distinction between a pointer, its address, and its target.

### Searching a list

Search examines the current node and then continues with its successor. It returns a pointer to the first matching node, or `NULL` after reaching the end.

The recursive version mirrors the list's recursive structure:

```c
list *search_list_recursive(list *l, item_type x)
{
    if (l == NULL)
        return NULL;

    if (l->item == x)
        return l;

    return search_list_recursive(l->next, x);
}
```

Its base case is the empty remainder of the list. Otherwise, the result is either the current node or the result of searching the smaller list beginning at `l->next`.

The iterative version avoids consuming one call-stack frame per node:

```c
list *search_list_iterative(list *l, item_type x)
{
    while (l != NULL) {
        if (l->item == x)
            return l;

        l = l->next;
    }

    return NULL;
}
```

Both versions take O(n) time in the worst case. The iterative version uses O(1) auxiliary space, while the recursive version uses O(n) call-stack space in the worst case.

### Inserting at the head

If the list does not need to remain sorted, the simplest insertion position is its beginning. No traversal is needed: allocate a node, point it to the current head, and replace the head with the new node.

```c
#include <stdlib.h>

void insert_list(list **l, item_type x)
{
    list *p;

    p = malloc(sizeof(list));
    p->item = x;
    p->next = *l;
    *l = p;
}
```

Two details carry the operation:

- `malloc(sizeof(list))` allocates enough memory for one node and returns its address. Production code must check whether `malloc` returned `NULL` before dereferencing `p`.
- `list **l` is a pointer to the caller's head pointer. `*l` is therefore the head pointer itself: `p->next = *l` connects the new node to the old first node, and `*l = p` changes the caller's head to the new node.

The caller passes the address of its head pointer:

```c
list *head = NULL;
insert_list(&head, 42);
```

Head insertion takes O(1) time. Passing only `list *l` would copy the head address into the function; assigning a new value to that local copy would not update `head` in the caller.

## Example

For `Lincoln → Jefferson → Clinton → None`, searching for `Jefferson`:

1. Compare `Lincoln`; it does not match.
2. Follow `Lincoln.next` to `Jefferson`.
3. Return the `Jefferson` node.

Searching for an absent value follows every link and stops when the current pointer becomes `NULL`.

## Connections

- Related: [[Pointers]] — node references provide the connections that form the list.
- Related: [[Contiguous Versus Linked Data Structures]] — contrasts linked nodes with array-backed storage.
- Related: [[Recursive Objects]] — a list is either empty or a node followed by a smaller list.
- Source: [[The Algorithm Design Manual]], second edition, §3.1.2, printed pp. 68–69 (PDF pages 80–81). [Reading PDF](https://sureshcseit.wordpress.com/wp-content/uploads/2021/04/skienathealgorithmdesignmanual.pdf#page=80).
