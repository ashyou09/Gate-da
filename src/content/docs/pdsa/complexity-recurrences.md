---
title: 3. Asymptotic complexity & recurrences
description: Big-O, Ω and Θ from definitions, counting loops, solving recurrences by unrolling, recursion trees and the Master theorem.
sidebar:
  label: 3. Complexity & recurrences
---

<span class="tag high">★ HIGH</span> <span class="tag yr">2024 Q40</span> <span class="tag yr">2026 Q15</span> <span class="tag yr">embedded every year</span>

**Why it matters:** there are only two direct questions so far (both on recurrences), but every sorting, searching, hashing and graph question assumes you know these costs. If you get this page right, the later topics become much easier.

## Topic map

<div class="mindmap">

- **Complexity**
  - Notation
    - $O$ upper bound, $\Omega$ lower bound, $\Theta$ tight
    - growth-rate ladder
  - Counting loops
    - nested → multiply
    - dependent → sum
    - halving / doubling → $\log n$
  - Recurrences
    - unrolling (substitution)
    - recursion tree
    - Master theorem
  - Standard results
    - binary search, merge sort, quicksort
    - best / worst / average case

</div>

---

## 3.1 What we measure

We count **basic operations** (comparisons, assignments, swaps) as a function of the input size $n$, and we keep only how fast that count grows. Constants and lower-order terms are dropped:

$$
3n^2 + 50n + 7 \;\in\; \Theta(n^2).
$$

## 3.2 The three notations

<div class="formula">

| Notation | Meaning | Formal definition (for some constants $c > 0$, $n_0$, and all $n \ge n_0$) |
|---|---|---|
| $f = O(g)$ | $f$ grows **at most** like $g$ | $f(n) \le c\,g(n)$ |
| $f = \Omega(g)$ | $f$ grows **at least** like $g$ | $f(n) \ge c\,g(n)$ |
| $f = \Theta(g)$ | $f$ grows **exactly** like $g$ | both $O(g)$ and $\Omega(g)$ |
| $f = o(g)$ | strictly slower | $\lim_{n\to\infty} f/g = 0$ |

**Limit test:** if $\lim_{n\to\infty} \dfrac{f(n)}{g(n)} = L$, then $L = 0 \Rightarrow f = o(g)$, $\;0 < L < \infty \Rightarrow f = \Theta(g)$, and $L = \infty \Rightarrow f = \omega(g)$.

</div>

$O$ is only an upper bound. "Merge sort is $O(n^2)$" is a *true* statement (just not a tight one). If a question asks for the **tight** or **exact** bound, it wants $\Theta$.

### The growth ladder (memorise this order)

$$
1 \;<\; \log\log n \;<\; \log n \;<\; \sqrt{n} \;<\; n \;<\; n\log n \;<\; n^2 \;<\; n^3 \;<\; 2^n \;<\; n! \;<\; n^n
$$

Useful facts:

- Every **polynomial** beats every **log power**: $(\log n)^{100} = o(n^{0.01})$.
- Every **exponential** beats every polynomial: $n^{100} = o(1.01^n)$.
- The base of a log doesn't matter: $\log_2 n = \Theta(\log_{10} n)$.
- $\log(n!) = \Theta(n\log n)$ (from Stirling's formula).
- But the base of an **exponential** does matter: $2^n = o(3^n)$.

## 3.3 Counting loops

| Loop pattern | Iterations | Complexity |
|---|---|---|
| `for i in range(n)` | $n$ | $\Theta(n)$ |
| two nested independent loops of size $n$ | $n \cdot n$ | $\Theta(n^2)$ |
| `for i in range(n): for j in range(i)` | $0 + 1 + \dots + (n-1) = \frac{n(n-1)}{2}$ | $\Theta(n^2)$ |
| `i = 1; while i < n: i *= 2` | $\lceil \log_2 n \rceil$ | $\Theta(\log n)$ |
| outer $n$ × inner doubling loop | $n \log n$ | $\Theta(n\log n)$ |
| `i = n; while i > 0: (loop i times); i //= 2` | $n + \frac n2 + \frac n4 + \dots \le 2n$ | $\Theta(n)$ (geometric series) |
| `i = 1; while i*i <= n: i += 1` | $\lfloor\sqrt n\rfloor$ | $\Theta(\sqrt n)$ |
| `i = 2; while i <= n: i = i*i` | $i = 2^{2^k}$ | $\Theta(\log\log n)$ |
| `for i in 1..n: j = i; while j <= n: j += i` | $\sum_{i} \frac{n}{i} = n H_n$ | $\Theta(n\log n)$ (harmonic) |

<div class="formula">

**Sums you need**

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2} \qquad \sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6} \qquad \sum_{i=0}^{k} 2^i = 2^{k+1} - 1
$$

$$
\sum_{i=1}^{n} \frac1i = H_n \approx \ln n \qquad\qquad \sum_{i=0}^{\infty} r^i = \frac{1}{1-r}\;\;(|r|<1)
$$

</div>

## 3.4 Recurrences

A recursive algorithm's running time is written as a **recurrence**: the cost on $n$ items, in terms of the cost on smaller inputs.

### Method 1: unrolling (substitution)

Keep substituting until you spot the pattern.

$T(n) = T(n-1) + n$, with $T(1) = 1$:

$$
T(n) = n + (n-1) + T(n-2) = \dots = n + (n-1) + \dots + 1 = \frac{n(n+1)}{2} = \Theta(n^2)
$$

$T(n) = T(n/2) + 1$:

$$
T(n) = T(n/4) + 2 = \dots = T(1) + \log_2 n = \Theta(\log n)
$$

### Method 2: the recursion tree

For $T(n) = 2T(n/2) + n$: each level of the tree does $n$ total work, and there are $\log_2 n$ levels.

```
level 0:            n                      → n
level 1:      n/2       n/2                → n
level 2:   n/4 n/4   n/4 n/4               → n
  ...                                      ...
level log n: 1 1 1 ... 1  (n leaves)       → n
                                     total = n log n
```

### Method 3: the Master theorem

<div class="formula">

For $T(n) = a\,T(n/b) + \Theta(n^d)$, with $a \ge 1$ and $b > 1$, compare $d$ with $\log_b a$:

$$
T(n) =
\begin{cases}
\Theta(n^d) & \text{if } d > \log_b a \quad\text{(the root's work dominates)}\\[4pt]
\Theta(n^d \log n) & \text{if } d = \log_b a \quad\text{(every level does equal work)}\\[4pt]
\Theta(n^{\log_b a}) & \text{if } d < \log_b a \quad\text{(the leaves dominate)}
\end{cases}
$$

**Extended case 2:** if $f(n) = \Theta(n^{\log_b a}\log^k n)$ with $k \ge 0$, then $T(n) = \Theta(n^{\log_b a}\log^{k+1} n)$.

</div>

**When the Master theorem does not apply:** subtractive recurrences like $T(n-1)$, unequal splits like $T(n/4) + T(3n/4)$, or a variable number of subproblems. Use unrolling or a recursion tree for those.

### Standard recurrences (recognise them on sight)

| Recurrence | Solution | Where it comes from |
|---|---|---|
| $T(n) = T(n/2) + 1$ | $\Theta(\log n)$ | binary search |
| $T(n) = T(n/2) + n$ | $\Theta(n)$ | quickselect with a lucky pivot |
| $T(n) = 2T(n/2) + 1$ | $\Theta(n)$ | tree traversal, max of an array by D&C |
| $T(n) = 2T(n/2) + n$ | $\Theta(n\log n)$ | merge sort, balanced quicksort |
| $T(n) = T(n-1) + 1$ | $\Theta(n)$ | linear recursion |
| $T(n) = T(n-1) + n$ | $\Theta(n^2)$ | worst-case quicksort, selection sort |
| $T(n) = 2T(n-1) + 1$ | $\Theta(2^n)$ | Tower of Hanoi |
| $T(n) = T(n-1) + T(n-2) + 1$ | $\Theta(\varphi^n)$, $\varphi \approx 1.618$ | naive Fibonacci |
| $T(n) = T(n/4) + T(3n/4) + n$ | $\Theta(n\log n)$ | quicksort with a constant-fraction split |
| $T(n) = 7T(n/2) + n^2$ | $\Theta(n^{\log_2 7}) \approx n^{2.81}$ | Strassen |

<div class="trap">

**Traps**

- A quicksort split of $\frac14 : \frac34$ (or even $\frac1{100} : \frac{99}{100}$) is still $\Theta(n\log n)$. Only a **constant-size** split, like $1 : (n-1)$, makes it $\Theta(n^2)$.
- $T(n) = 2T(n/2) + n\log n$ isn't Master case 3. It's the extended case 2 with $k = 1$, giving $\Theta(n\log^2 n)$.
- Best, worst and average case are **different functions**. A question that says "expected" wants the average over random inputs or random pivots.

</div>

---

## Summary: important points

<div class="formula">

1. Ladder: $1 < \log\log n < \log n < \sqrt n < n < n\log n < n^2 < 2^n < n! < n^n$.
2. Nested loops multiply, dependent loops sum, and halving gives $\log n$.
3. Shrinking work per iteration adds up as a geometric series, which is $\Theta$ of the first term.
4. Master theorem: compare $d$ with $\log_b a$. Bigger $d$ → root, equal → $\cdot \log n$, smaller → leaves.
5. A subtractive recurrence $T(n-c)$ needs unrolling, not the Master theorem.
6. Binary search: $F(n) = F(\lfloor n/2\rfloor) + 1 = \lfloor \log_2 n\rfloor + 1$.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q40 (2 marks, MCQ)

$F(n)$ is the maximum number of comparisons binary search makes on a sorted array of size $n$. Which is true?
(A) $F(n) = F(\lfloor n/2 \rfloor) + 1$ (B) $F(n) = F(\lfloor n/2\rfloor) + F(\lceil n/2\rceil)$ (C) $F(n) = F(\lfloor n/2\rfloor)$ (D) $F(n) = F(n-1) + 1$

<details>
<summary>Solution: answer (A)</summary>

One comparison with the middle element either finds the key or throws away about half of the array. In the worst case you keep the **larger** remaining half, which has $\lfloor n/2 \rfloor$ elements. So:

$$F(n) = 1 + F(\lfloor n/2\rfloor), \qquad F(1) = 1 \;\Rightarrow\; F(n) = \lfloor\log_2 n\rfloor + 1.$$

- (B) would mean searching **both** halves, which takes linear time.
- (D) is linear search.
- (C) never does any work.

</details>

### GATE DA 2026 Q15 (1 mark, MCQ)

Quicksort on $n$ distinct, randomly ordered elements uses the first element as the pivot, and partitioning takes linear time. Which recurrence gives the **expected** time $T(n)$?

(A) $T(1) + T(n-1) + O(n)$ (B) $T(n/4) + T(3n/4) + O(n)$ (C) $2T(n/2) + O(n)$ (D) $\dfrac1n\sum_{k=0}^{n-1}\big[T(k) + T(n-k-1)\big] + O(n)$

<details>
<summary>Solution: answer (D)</summary>

Because the input is randomly ordered, the first element is equally likely to be the 1st, 2nd, …, or $n$th smallest. If it's the $(k+1)$th smallest, the subproblems have sizes $k$ and $n-k-1$. The **expected** cost averages over all $n$ possibilities, each with probability $\frac1n$:

$$
T(n) = \frac1n \sum_{k=0}^{n-1}\big[T(k) + T(n-k-1)\big] + O(n) \;=\; \Theta(n \log n).
$$

- (A) is the **worst** case (pivot is always the extreme value).
- (C) is the **best** case (pivot is always the median).
- (B) is one particular split. It gives the right order, but it isn't the expectation.

</details>

---

## Test yourself (B): predicted 2027-style questions

**P1 (1 mark, MCQ).** What is the time complexity of the code below?

```python
i = n
while i > 0:
    for j in range(i):
        work()
    i //= 2
```

(A) $\Theta(\log n)$ (B) $\Theta(n)$ (C) $\Theta(n\log n)$ (D) $\Theta(n^2)$

<details>
<summary>Answer: (B)</summary>

The total work is $n + \frac n2 + \frac n4 + \dots \le 2n$, which is $\Theta(n)$. Students often pick (C) because they multiply "n work" by "log n iterations", but the work shrinks each iteration, so you have to add it up as a geometric series.

</details>

**P2 (2 marks, MSQ).** Which of these are true?
(A) $n^2 + 100n = O(n^2)$ (B) $2^{n+1} = \Theta(2^n)$ (C) $2^{2n} = \Theta(2^n)$ (D) $\log(n^3) = \Theta(\log n)$

<details>
<summary>Answer: A; B; D</summary>

- **(A)** True.
- **(B)** $2^{n+1} = 2\cdot 2^n$, a constant factor. True.
- **(C)** $2^{2n} = 4^n$, and $4^n / 2^n = 2^n \to \infty$. False.
- **(D)** $\log(n^3) = 3\log n$. True.

</details>

**P3 (2 marks, MCQ).** Solve $T(n) = 4T(n/2) + n^2$.
(A) $\Theta(n^2)$ (B) $\Theta(n^2\log n)$ (C) $\Theta(n^3)$ (D) $\Theta(n\log n)$

<details>
<summary>Answer: (B)</summary>

$a = 4$, $b = 2$, so $\log_2 4 = 2 = d$. That's case 2, giving $\Theta(n^2\log n)$.

</details>

**P4 (2 marks, MCQ).** Solve $T(n) = 3T(n/3) + \sqrt n$.
(A) $\Theta(\sqrt n)$ (B) $\Theta(\sqrt n \log n)$ (C) $\Theta(n)$ (D) $\Theta(n\log n)$

<details>
<summary>Answer: (C)</summary>

$\log_3 3 = 1 > d = \tfrac12$. That's case 3 (leaves dominate), giving $\Theta(n^{1}) = \Theta(n)$.

</details>

**P5 (1 mark, NAT).** For $n = 16$, how many times does `c += 1` run?

```python
c = 0
for i in range(1, n+1):
    j = i
    while j <= n:
        c += 1
        j += i
```

<details>
<summary>Answer: 50</summary>

For each $i$, the inner loop runs $\lfloor 16/i \rfloor$ times:

$$16 + 8 + 5 + 4 + 3 + 2 + 2 + 2 + 1\times 8 = 42 + 8 = 50.$$

In general this is $\sum \lfloor n/i\rfloor \approx n\ln n$, so $\Theta(n\log n)$.

</details>

**P6 (2 marks, MCQ).** Solve $T(n) = T(n-2) + n$, with $T(0) = 0$.
(A) $\Theta(n)$ (B) $\Theta(n\log n)$ (C) $\Theta(n^2)$ (D) $\Theta(2^{n/2})$

<details>
<summary>Answer: (C)</summary>

$T(n) = n + (n-2) + (n-4) + \dots$, which has about $n/2$ terms averaging about $n/2$. That's roughly $n^2/4 = \Theta(n^2)$. The Master theorem doesn't apply because the recurrence is subtractive.

</details>
