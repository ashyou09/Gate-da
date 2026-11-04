---
title: 7. Stacks, queues, deques & linked lists
description: LIFO and FIFO behaviour, operation traces, expression evaluation, circular queues, valid stack permutations and linked-list pointer work.
sidebar:
  label: 7. Stacks, queues & lists
  order: 7
---

**Why it matters:** 2024 Q16 (matching), 2024 Q32 (a deque trace) and 2025 Q64 (a stack pseudocode trace) all came from here. These questions reward **slow, literal tracing**: write the structure down after every single operation.

## Topic map

<div class="mindmap">

- **Linear structures**
  - Stack (LIFO)
    - push / pop / top in $O(1)$
    - uses: recursion, undo, DFS, brackets, expressions
    - valid pop sequences: Catalan number
  - Queue (FIFO)
    - enqueue / dequeue in $O(1)$
    - circular array: wrap with mod, keep one slot empty
    - uses: BFS, scheduling
  - Deque
    - insert / remove at both ends in $O(1)$
  - Expressions
    - postfix evaluation with a stack
    - infix → postfix (precedence, associativity)
  - Linked lists
    - singly / doubly / circular
    - insert / delete at a known node $O(1)$, search $O(n)$
    - reverse, middle (slow/fast), cycle detection

</div>

## 7.1 Stack: last in, first out

Think of a pile of plates: you can only add or remove at the **top**.

| Operation | Effect | Cost |
|---|---|---|
| `push(x)` | put `x` on top | $O(1)$ |
| `pop()` | remove and return the top | $O(1)$ |
| `top()` / `peek()` | read the top without removing it | $O(1)$ |

In Python, a list works as a stack: `append` pushes and `pop()` pops, both at the end.

**Where stacks appear:** the function call stack (recursion), undo, DFS, matching brackets, and evaluating expressions.

**Tracing rule:** write the stack horizontally with the top on the **right**, and rewrite it after every operation.

## 7.2 Expressions with a stack

**Evaluating postfix** (operator after its operands): scan left to right. Push numbers. When you meet an operator, pop **b** first, then **a**, and push `a op b`. The order matters for `-`, `/` and `^`.

`6 2 3 + - 3 8 2 / + *`:

| Token | Stack (top on the right) |
|---|---|
| 6, 2, 3 | 6 2 3 |
| + | 6 5 |
| − | 1 |
| 3, 8, 2 | 1 3 8 2 |
| / | 1 3 4 |
| + | 1 7 |
| * | **7** |

**Infix → postfix** (shunting-yard): operands go straight to the output. For an operator, first pop any operators on the stack with **higher** precedence (or **equal** precedence, if the new operator is left-associative), then push it. `(` is pushed. On `)`, pop until the matching `(`.

| Infix | Postfix |
|---|---|
| `a + b * (c - d) / e` | `a b c d - * e / +` |
| `(a + b) * c - d / e` | `a b + c * d e / -` |
| `a ^ b ^ c` | `a b c ^ ^` (`^` is right-associative) |

## 7.3 Queue: first in, first out

| Operation | Effect | Cost |
|---|---|---|
| `enqueue(x)` | add at the **rear** | $O(1)$ |
| `dequeue()` | remove from the **front** | $O(1)$ |

In Python, use `collections.deque` (`append` / `popleft`). `list.pop(0)` is $O(n)$, because every remaining element shifts.

### Circular array queue

An array of size $n$ with indices `front` and `rear`, both of which wrap around with `mod n`.

<div class="formula">

- enqueue: `A[rear] = x; rear = (rear + 1) % n`
- dequeue: `x = A[front]; front = (front + 1) % n`
- **empty** when `front == rear`
- **full** when `(rear + 1) % n == front`, so one slot is always left unused and the **capacity is $n - 1$**
- number of elements $= (\text{rear} - \text{front} + n) \bmod n$

</div>

### Queue from two stacks

Push onto stack **In**. To dequeue, if stack **Out** is empty, pop everything from In and push it onto Out, then pop from Out. Each element moves at most twice, so this is **$O(1)$ amortised** per operation.

## 7.4 Deque (double-ended queue)

A deque supports `insertFirst`, `insertLast`, `removeFirst` and `removeLast`, all in $O(1)$. It can act as a stack (use one end) or as a queue (insert at one end, remove at the other).

## 7.5 Which pop orders can a stack produce?

Push $1, 2, \dots, n$ in that order, with pops allowed at any time. Not every permutation of the output is possible.

**Test:** go through the target output. For each value, keep pushing until that value is on top, then pop it. If the value you need is already **buried** under something else in the stack, the order is impossible.

- `3 2 4 1` from `1 2 3 4`: push 1, 2, 3, pop 3, pop 2, push 4, pop 4, pop 1. ✓
- `3 1 4 2`: push 1, 2, 3, pop 3, then you need 1, but 2 is on top of it. ✗

<div class="formula">

The number of valid pop sequences for $n$ elements is the **Catalan number**

$$
C_n = \frac{1}{n+1}\binom{2n}{n}: \quad 1, 1, 2, 5, 14, 42, 132, \dots
$$

The same numbers count binary trees with $n$ nodes and balanced bracket strings with $n$ pairs.

</div>

## 7.6 Linked lists

A linked list is a chain of nodes, each holding a value and a pointer to the `next` node (and to `prev`, in a doubly linked list).

| Operation | Singly linked | Doubly linked | Array / Python list |
|---|---|---|---|
| access the $k$th element | $O(k)$ | $O(k)$ | $O(1)$ |
| insert or delete at the head | $O(1)$ | $O(1)$ | $O(n)$ |
| insert after a known node | $O(1)$ | $O(1)$ | $O(n)$ |
| delete a known node | $O(n)$ (you need its predecessor) | $O(1)$ | $O(n)$ |
| search | $O(n)$ | $O(n)$ | $O(n)$ |

**Pointer order matters.** To insert node `x` after node `p`: first `x.next = p.next`, **then** `p.next = x`. Doing it the other way round loses the rest of the list.

Classic patterns:

- **Reverse** in place with three pointers: `prev, cur = None, head`, then repeat `nxt = cur.next; cur.next = prev; prev = cur; cur = nxt`.
- **Middle element:** move a slow pointer 1 step and a fast pointer 2 steps. When fast reaches the end, slow is at the middle.
- **Cycle detection (Floyd):** the same slow and fast pointers. They meet if and only if there's a cycle.
- No random access means **no $O(\log n)$ binary search** on a linked list (2025 Q27).

---

## Summary: important points

<div class="formula">

1. Stack = LIFO, queue = FIFO, deque = both ends. All core operations are $O(1)$.
2. Trace by writing the whole structure after **every** operation.
3. Postfix evaluation: pop **b** then **a**, then compute `a op b`.
4. Infix → postfix: pop operators of higher (or equal, for left-associative) precedence first. `^` is right-associative.
5. Circular queue of size $n$: full when `(rear + 1) % n == front`, so the capacity is $n - 1$.
6. Valid stack pop orders: test with push-until-top. There are $C_n$ of them.
7. Linked list: $O(1)$ insert at a known spot, $O(n)$ access and search. Set the new node's pointer before relinking.
8. BFS uses a queue, DFS and recursion use a stack.

</div>

<div class="trap">

- `list.pop(0)` in Python is $O(n)$. A real queue uses `deque.popleft()`.
- In postfix, `a b -` means $a - b$, not $b - a$.
- A circular queue of size 5 holds only **4** elements under the usual convention.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q32 (1 mark, NAT)

Start with an empty deque D, then run: insertFirst(10), insertLast(32), a ← removeFirst(), insertLast(28), insertLast(17), a ← removeFirst(), a ← removeLast(). What is the final value of a?

<details>
<summary>Show solution</summary>

**Answer: 17**

| Operation | Deque (front … rear) | a |
|---|---|---|
| insertFirst(10) | 10 | |
| insertLast(32) | 10 32 | |
| removeFirst() | 32 | 10 |
| insertLast(28) | 32 28 | |
| insertLast(17) | 32 28 17 | |
| removeFirst() | 28 17 | 32 |
| removeLast() | 28 | **17** |

</details>

### GATE DA 2025 Q64 (2 marks, NAT)

The stack pseudocode that pushes 0 to 8, then pops, discarding one extra element after each odd value. This is solved step by step on the [Recursion page](/pdsa/recursion-tracing/#gate-da-2025-q64-2-marks-nat-recursions-stack-made-explicit). **Answer: 24.** Redo it here without looking.

### GATE DA 2024 Q16 (1 mark, MCQ)

Match FIFO, lookup and LIFO with stacks, queues and hash tables. **Answer: FIFO → queues, lookup → hash tables, LIFO → stacks** (option A). The full solution is on the [Hashing page](/pdsa/hashing/).

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Evaluate the postfix expression `5 3 2 * + 4 -`.

<details>
<summary>Show solution</summary>

**Answer: 7**

- 5 3 2 → `*` gives 5 6
- `+` gives 11
- 4 → 11 4
- `-` gives $11 - 4 = $ **7**

</details>

**F2 (1 mark, MCQ).** What is the postfix form of `a + b * (c - d) / e`?
(A) `a b c d - * e / +` (B) `a b + c d - * e /` (C) `a b c - d * e / +` (D) `a b c d - e / * +`

<details>
<summary>Show solution</summary>

**Answer: (A)**

The parenthesised `c - d` becomes `c d -`. Then `b * (…)` becomes `b c d - *`. `*` and `/` share precedence and associate left, so `/ e` applies to that whole result: `b c d - * e /`. Finally `a + …` puts `+` at the end.

</details>

**F3 (2 marks, MSQ).** Push 1, 2, 3, 4 in that order, popping at any time. Which output sequences are possible?
(A) 3 2 4 1 (B) 3 1 4 2 (C) 4 3 2 1 (D) 2 4 1 3

<details>
<summary>Show solution</summary>

**Answer: A; C**

- **(A)** ✓, traced in §7.5.
- **(B)** After popping 3, the stack is [1, 2]. The next output 1 is buried under 2. ✗
- **(C)** Push all four, then pop all four. ✓
- **(D)** Push 1, 2, pop 2. Push 3, 4, pop 4. The stack is now [1, 3], and 1 is buried under 3. ✗

</details>

**F4 (1 mark, NAT).** Push $1, \dots, 5$ in order, with pops allowed at any time. How many distinct output sequences are possible?

<details>
<summary>Show solution</summary>

**Answer: 42**

$C_5 = \frac{1}{6}\binom{10}{5} = \frac{252}{6} = 42$.

</details>

**F5 (2 marks, NAT).** A circular queue is stored in an array of size 5, with `front = rear = 0` at the start and the "one slot empty" full condition. Run: enqueue 10, 20, 30; dequeue twice; enqueue 40, 50, 60, 70. An enqueue on a full queue is ignored. How many elements does the queue hold at the end?

<details>
<summary>Show solution</summary>

**Answer: 4**

- After enqueueing 10, 20, 30: front = 0, rear = 3.
- After two dequeues: front = 2. The queue holds [30].
- Enqueue 40 → rear = 4. Enqueue 50 → rear = 0 (wraps). Enqueue 60 → rear = 1.
- Enqueue 70: $(1 + 1) \bmod 5 = 2 = $ front, so the queue is full and 70 is ignored.

The queue holds 30, 40, 50, 60: **4** elements, which is the capacity $n - 1$.

</details>

**F6 (2 marks, MSQ).** For a singly linked list with only a `head` pointer, which operations take $O(1)$ time?
(A) insert at the head (B) delete the last node (C) insert after a node you have a pointer to (D) find the middle node

<details>
<summary>Show solution</summary>

**Answer: A; C**

- **(B)** You need the second-to-last node, which means walking the whole list: $O(n)$.
- **(D)** Even the slow/fast pointer method walks $n/2$ nodes: $O(n)$.

</details>
