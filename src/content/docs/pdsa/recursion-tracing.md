---
title: 2. Recursion & call counting
description: Call trees, the runtime stack, counting activations, print order, and how GATE DA turns recursion into 2-mark NATs.
sidebar:
  label: 2. Recursion & tracing
  order: 2
---

**Why it matters:** 2024 Q38 and Q41, 2025 Q63 and Q64, and 2026 Q39 and Q58 are all solved with **one drawing: the call tree**. Get fast at drawing it and these become easy 2-mark questions.

## Topic map

<div class="mindmap">

- **Recursion**
  - Anatomy
    - base case
    - recursive case (must shrink toward the base)
  - Runtime stack
    - push on call, pop on return
    - depth = longest root→leaf path
  - Call tree
    - nodes = total calls (activations)
    - leaves = base-case calls
  - Order of work
    - before the call → "head" (way down)
    - after the call → "tail" (way back up)
  - Counting
    - recurrence for the number of calls
    - Fibonacci-type count $= 2F - 1$
  - Memoisation
    - each distinct state solved once → leads to DP

</div>

---

## 2.1 Anatomy of a recursive function

```python
def fact(n):
    if n == 0:          # base case: answer known directly
        return 1
    return n * fact(n - 1)   # recursive case: smaller problem
```

You need both parts:

- a **base case** that stops the recursion, and
- a **recursive case** that moves *toward* the base case.

If either is missing, you get infinite recursion, which Python reports as a `RecursionError` after roughly 1000 levels.

## 2.2 The runtime stack

Each call gets its own **stack frame** with its own parameters and local variables. A frame is **pushed** when the call starts and **popped** when it returns.

```
fact(3) calls fact(2) calls fact(1) calls fact(0)

        ┌─────────┐
        │ fact(0) │ ← top: returns 1 first
        ├─────────┤
        │ fact(1) │   waits for fact(0)
        ├─────────┤
        │ fact(2) │   waits for fact(1)
        ├─────────┤
        │ fact(3) │   initial call
        └─────────┘
```

<div class="formula">

- **Total activations** = number of nodes in the call tree, including the first call.
- **Maximum stack depth** = number of nodes on the longest root-to-leaf path.
- **Number of base-case calls** = number of leaves.

</div>

## 2.3 The call tree: the one tool you need

Draw a node for every call, with its argument written inside, and an edge to each call it makes.

`mystery(n)`: return 1 if `n <= 0`, else `mystery(n-1) + mystery(n-2)`.

```
                    m(4)
                /          \
            m(3)            m(2)
           /    \          /    \
       m(2)     m(1)    m(1)    m(0)
      /   \     /  \    /  \
   m(1)  m(0) m(0) m(-1) m(0) m(-1)
   /  \
m(0) m(-1)
```

Count the nodes: **15 activations**. Count the leaves (base cases): **8**, which is also the return value, since every leaf returns 1 and the results are added.

### Counting without drawing: a recurrence for the count

Let $C(n)$ be the total number of calls made by `f(n)`. Each call counts itself, then adds the calls made by its children:

$$
C(n) = 1 + C(n-1) + C(n-2), \qquad C(\text{base}) = 1
$$

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| base is `n <= 0` | 1 | 3 | 5 | 9 | 15 | 25 | 41 |
| base is `n <= 1` | 1 | 1 | 3 | 5 | 9 | 15 | 25 |

<div class="formula">

**Fibonacci-type call count.** Let $F_1 = F_2 = 1$ be the Fibonacci numbers. Then:

$$
\text{base } n \le 1:\; C(n) = 2F_{n+1} - 1 \qquad\qquad \text{base } n \le 0:\; C(n) = 2F_{n+2} - 1
$$

Why: in a tree where every internal node has exactly 2 children, $\text{nodes} = 2\cdot\text{leaves} - 1$.

</div>

That last fact is worth remembering on its own. In **any** recursion where every non-base call makes exactly two calls,

$$
\text{total calls} = 2 \times (\text{base-case calls}) - 1.
$$

## 2.4 Order of work: before the call vs after it

Code that runs **before** the recursive call happens on the way **down**. Code that runs **after** it happens on the way **back up**, in reverse order.

```python
def h(n):
    if n == 0: return
    print(n)        # before: 3, 2, 1
    h(n - 1)
    print(-n)       # after: -1, -2, -3
h(3)                # prints 3 2 1 -1 -2 -3
```

Two recursive calls with work between them gives an **in-order** pattern, like this ruler sequence:

```python
def p(n):
    if n > 0:
        p(n - 1)
        print(n)
        p(n - 1)
p(3)      # 1 2 1 3 1 2 1   → prints 2^n − 1 = 7 numbers
```

## 2.5 Recursion that mutates shared data

Lists are passed by reference (see [§1.4](/pdsa/python-semantics/#14-functions-pass-by-object-reference)). Every frame works on the **same** list, so a change made deep in the recursion is visible to everyone.

```python
def fun(D, s1, s2):
    if s1 < s2:
        D[s1], D[s2] = D[s2], D[s1]
        fun(D, s1 + 1, s2 - 1)
```

Each call swaps the two ends, then recurses on the inner part. The result is that `D[s1..s2]` is **reversed**. (This is GATE DA 2024 Q41, answer C.)

## 2.6 Memoisation: from exponential to linear

Naive Fibonacci recomputes the same sub-calls again and again. If you **cache** each result, each distinct argument is computed only once.

| Version | Calls for $F(n)$ | Time |
|---|---|---|
| naive | $2F_{n+1} - 1$ | $\Theta(\varphi^n)$, about $O(2^n)$ |
| memoised | $n + 1$ distinct states | $\Theta(n)$ |

This is the core idea of dynamic programming:

$$
\text{cost} = (\text{number of distinct states}) \times (\text{work per state}).
$$

---

## Summary: important points

<div class="formula">

1. **Always draw the call tree.** Nodes = calls, leaves = base cases, longest path = depth.
2. Call-count recurrence: $C(n) = 1 + \sum C(\text{children})$, with $C(\text{base}) = 1$.
3. In a binary call tree, $\text{nodes} = 2\cdot\text{leaves} - 1$.
4. Check the base condition (`<= 0` vs `<= 1`). It shifts every count.
5. Work before the call happens going down. Work after the call happens coming back up, in reverse.
6. A list passed through the recursion is shared by every frame.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q39 (2 marks, MCQ)

```python
def mystery(n):
    if n <= 0:
        return 1
    else:
        return mystery(n-1) + mystery(n-2)
```

How many function calls (stack activations), including the initial one, does `mystery(4)` make?
(A) 5 (B) 9 (C) 15 (D) 17

<details>
<summary>Show solution</summary>

**Answer: (C) 15**

Use $C(n) = 1 + C(n-1) + C(n-2)$ with $C(0) = C(-1) = 1$:

- $C(1) = 1 + 1 + 1 = 3$
- $C(2) = 1 + 3 + 1 = 5$
- $C(3) = 1 + 5 + 3 = 9$
- $C(4) = 1 + 9 + 5 = \mathbf{15}$

Quick check with the shortcut: the base case is $n \le 0$, so $C(4) = 2F_6 - 1 = 2(8) - 1 = 15$. ✓

**Trap:** (B) 9 is the answer if you used base case $n \le 1$. Always read the base condition.

</details>

### GATE DA 2024 Q38 (2 marks, MCQ)

```python
def count(child_dict, i):
    if i not in child_dict.keys():
        return 1
    ans = 1
    for j in child_dict[i]:
        ans += count(child_dict, j)
    return ans

child_dict = dict()
child_dict[0] = [1, 2]
child_dict[1] = [3, 4, 5]
child_dict[2] = [6, 7, 8]
print(count(child_dict, 0))
```

<details>
<summary>Show solution</summary>

**Answer: 9 (option D)**

`child_dict` describes a tree: 0 has children 1 and 2, 1 has children 3, 4, 5, and 2 has children 6, 7, 8. `count(i)` returns 1 for `i` itself plus the count of every child subtree. In other words, it counts **the nodes in the subtree rooted at `i`**.

- `count(3) = count(4) = … = count(8) = 1` (these aren't keys, so they're leaves)
- `count(1) = 1 + 3 = 4` and `count(2) = 1 + 3 = 4`
- `count(0) = 1 + 4 + 4 = ` **9**

</details>

### GATE DA 2026 Q58 (2 marks, NAT)

```python
def fun(L, i=0):
    if i >= len(L) - 1:
        return 0
    if L[i] > L[i+1]:
        L[i+1], L[i] = L[i], L[i+1]
        return 1 + fun(L, i+1)
    else:
        return fun(L, i+1)

data = [5, 3, 4, 1, 2]
count = 0
for _ in range(len(data)):
    count += fun(data)
print(count)
```

<details>
<summary>Show solution</summary>

**Answer: 8**

Look at what `fun` does: it walks `i = 0 … n-2`, swaps each out-of-order adjacent pair, and counts the swaps. That's **one pass of bubble sort**, written recursively. Because `data` is a list, the swaps stay in place for the next pass.

| Pass | List after the pass | Swaps |
|---|---|---|
| 1 | [3, 4, 1, 2, **5**] | 4 |
| 2 | [3, 1, 2, **4, 5**] | 2 |
| 3 | [1, 2, **3, 4, 5**] | 2 |
| 4 | unchanged | 0 |
| 5 | unchanged | 0 |

Total = **8**.

**Shortcut:** bubble sort swaps = number of **inversions** (pairs $i<j$ with $a_i > a_j$). In [5,3,4,1,2]: 5 is bigger than 4 later elements, 3 than 2, 4 than 2, and 1 than none. $4 + 2 + 2 + 0 = 8$. ✓ More on this in [Searching & sorting](/pdsa/searching-sorting/).

</details>

### GATE DA 2025 Q64 (2 marks, NAT): recursion's stack, made explicit

```
Create empty stack S
Set x=0, flag=0, sum=0
Push x onto S
while (S is not empty){
    if (flag equals 0){ Set x = x+1; Push x onto S }
    if (x equals 8): Set flag=1
    if (flag equals 1){
        x = Pop(S)
        if (x is odd): Pop(S)
        Set sum = sum + x }
}
Output sum
```

<details>
<summary>Show solution</summary>

**Answer: 24**

**Phase 1: pushing.** Starting from `[0]`, the loop pushes 1, 2, … 8. When `x = 8`, `flag` becomes 1. The stack is `[0, 1, 2, 3, 4, 5, 6, 7, 8]`, with 8 on top.

**Phase 2: popping.** Each loop iteration pops `x` into the sum. If `x` is odd, it also pops (and discards) the next element.

| Popped `x` | Odd? Extra pop | sum |
|---|---|---|
| 8 | no | 8 |
| 7 | yes, discards 6 | 15 |
| 5 | yes, discards 4 | 20 |
| 3 | yes, discards 2 | 23 |
| 1 | yes, discards 0 | 24 |

The stack is now empty, so the output is **24**.

</details>

---

## Test yourself (B): predicted 2027-style questions

**P1 (2 marks, NAT).** For the function below, what is `g(5)`, and how many calls does `g(5)` make in total?

```python
def g(n):
    if n <= 1: return n
    return g(n-1) + 2*g(n-2)
```

<details>
<summary>Show solution</summary>

**Answer: g(5) = 11, 15 calls**

**Value.** $g(0) = 0$, $g(1) = 1$, $g(2) = 1$, $g(3) = 1 + 2 = 3$, $g(4) = 3 + 2 = 5$, $g(5) = 5 + 6 = $ **11**.

**Calls.** The call structure is the same as Fibonacci with base $n \le 1$, because the multiplier 2 doesn't add calls. So $C(5) = 2F_6 - 1 = $ **15**.

</details>

**P2 (1 mark, MCQ).** What does `r("GATE")` return?

```python
def r(s):
    if len(s) <= 1: return s
    return r(s[1:]) + s[0]
```

(A) `GATE` (B) `ETAG` (C) `EGAT` (D) `ATEG`

<details>
<summary>Show solution</summary>

**Answer: (B) ETAG**

`r("GATE") = r("ATE") + "G" = (r("TE") + "A") + "G" = (("E" + "T") + "A") + "G"`, which is `ETAG`. The function reverses the string.

</details>

**P3 (2 marks, NAT).** How many numbers does `p(5)` print? (`p` is the ruler function from §2.4.)

<details>
<summary>Show solution</summary>

**Answer: 31**

Let $N(n)$ be the count. $N(n) = 2N(n-1) + 1$ with $N(0) = 0$, so $N(n) = 2^n - 1$, and $N(5) = $ **31**.

</details>

**P4 (1 mark, NAT).** What does `s(2027)` return, and what is the maximum stack depth (counting the first call)?

```python
def s(n):
    if n == 0: return 0
    return n % 10 + s(n // 10)
```

<details>
<summary>Show solution</summary>

**Answer: 11, depth 5**

The calls are `s(2027)`, `s(202)`, `s(20)`, `s(2)`, `s(0)`: that's **5 frames** on the stack at the deepest point. The function adds the digits: $7 + 2 + 0 + 2 = $ **11**.

</details>

**P5 (2 marks, MSQ).** For naive recursive Fibonacci `F(n) = F(n-1) + F(n-2)` with base `n <= 1`, which statements are true?
(A) The maximum stack depth for `F(n)` is $n$ (B) The total calls for `F(6)` is 25 (C) Memoisation reduces the calls to $O(n)$ (D) The number of leaf calls of `F(n)` is $F_{n+1}$

<details>
<summary>Show solution</summary>

**Answer: A; B; C; D (all true)**

- **(A)** The longest path is `F(n) → F(n-1) → … → F(1)`, which is $n$ frames. True.
- **(B)** $C(6) = 2F_7 - 1 = 2(13) - 1 = 25$. True.
- **(C)** Each of the $n+1$ states is computed once. True.
- **(D)** Total nodes $= 2\cdot\text{leaves} - 1$, so leaves $= F_{n+1}$. True.

This is the kind of MSQ where all four options are correct. Check each statement on its own and don't assume some must be false.

</details>
