---
title: 4. Searching & sorting
description: Linear and binary search, selection, bubble, insertion, merge and quick sort — passes, comparisons, swaps, inversions, stability.
sidebar:
  label: 4. Searching & sorting
  order: 4
---

**Why it matters:** this is the second-largest PDSA block (9 questions in 3 years, counting 2026 Q15 and Q58). GATE doesn't ask you to *write* a sort. It asks you to **count**: passes, comparisons, swaps, and the array's state after $k$ passes. That means you have to know the *exact* version of each algorithm, not just its idea.

## Topic map

<div class="mindmap">

- **Searching & sorting**
  - Searching
    - linear search $O(n)$, works on anything
    - binary search $O(\log n)$, needs sorted data + random access
  - Simple sorts $\Theta(n^2)$
    - selection: fewest swaps, not stable
    - bubble: swaps = inversions, stable
    - insertion: best on nearly-sorted data, stable
  - Divide & conquer $\Theta(n\log n)$
    - merge sort: stable, $O(n)$ extra space
    - quicksort: in place, worst case $\Theta(n^2)$
  - Properties
    - stability, in-place, adaptive
    - inversions
    - lower bound $\Omega(n\log n)$ for comparison sorts

</div>

---

## 4.1 Linear search

Check every element from left to right until you find the key.

| Case | Comparisons |
|---|---|
| best (key is first) | 1 |
| worst (key is last or absent) | $n$ |
| average, key present at a uniformly random position | $\frac{n+1}{2}$ |

It works on **any** sequence: unsorted data, linked lists, anything.

## 4.2 Binary search

```python
def bsearch(A, key):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] == key:   return mid
        elif A[mid] < key:  lo = mid + 1     # discard left half
        else:               hi = mid - 1     # discard right half
    return -1
```

Each comparison throws away half of what's left. That's where the $\log n$ comes from.

<div class="formula">

**Requirements:** the data must be (1) **sorted** and (2) support **$O(1)$ random access**, like an array or Python list.

**Worst-case comparisons**, where one three-way comparison (`==`, `<`, `>`) counts as one:

$$
F(n) = F(\lfloor n/2 \rfloor) + 1,\; F(1) = 1 \quad\Longrightarrow\quad F(n) = \lfloor \log_2 n \rfloor + 1
$$

| $n$ | 7 | 8 | 100 | 1000 | 1024 |
|---|---|---|---|---|---|
| $\lfloor\log_2 n\rfloor + 1$ | 3 | 4 | 7 | **10** | 11 |

</div>

**Why does a linked list fail?** Reaching the middle of a linked list takes $O(n)$ pointer steps. Binary search on a sorted linked list still uses only $O(\log n)$ *comparisons*, but its *time* is $O(n)$.

## 4.3 The three n² sorts: learn the exact versions

**Inversion:** a pair $(i, j)$ with $i < j$ but $A[i] > A[j]$. A sorted array has 0 inversions. A reverse-sorted array has $\binom n2$. Inversions are the key to most swap-counting questions.

### Selection sort

In pass $i$, find the **minimum** of `A[i..n-1]` and swap it into position $i$.

```python
for i in range(n - 1):
    m = i
    for j in range(i + 1, n):
        if A[j] < A[m]: m = j
    A[i], A[m] = A[m], A[i]
```

- **Comparisons:** always $\frac{n(n-1)}{2}$, regardless of the input.
- **Swaps:** at most $n - 1$, the **fewest** of any simple sort. That makes it the best choice when writes are expensive.
- After $k$ passes, the **first $k$ positions are final**: they hold the $k$ smallest elements, in order.
- **Not stable.** Example: `[2a, 2b, 1]`. Pass 1 swaps `2a` with `1`, giving `[1, 2b, 2a]`.

### Bubble sort

In each pass, compare adjacent pairs from left to right and swap any that are out of order. The largest remaining element "bubbles" to the end.

```python
for p in range(n - 1):
    swapped = False
    for j in range(n - 1 - p):
        if A[j] > A[j+1]:
            A[j], A[j+1] = A[j+1], A[j]; swapped = True
    if not swapped: break          # optimised version only
```

- **Swaps** = number of **inversions** (each adjacent swap removes exactly one).
- **Comparisons:** $\frac{n(n-1)}{2}$ in the plain version. With the `swapped` flag, the best case (already sorted) is $n - 1$.
- After $k$ passes, the **last $k$ positions are final**.
- **Stable**, because it only swaps when strictly greater.

### Insertion sort

Grow a sorted prefix. In pass $i$, take `A[i]` and slide it left until the element before it is $\le$ it.

```python
for i in range(1, n):
    j = i
    while j > 0 and A[j-1] > A[j]:
        A[j-1], A[j] = A[j], A[j-1]
        j -= 1
```

- **Swaps (shifts)** = number of **inversions**.
- **Comparisons** in pass $i$ = (shifts in that pass) + 1, unless the element slides all the way to the front. Total between $n - 1$ (sorted input) and $\frac{n(n-1)}{2}$ (reverse-sorted input).
- After $k$ passes, the **first $k+1$ positions are sorted relative to each other**, but they aren't necessarily final.
- **Stable** and **adaptive**: $\Theta(n + \text{inversions})$, so it's the fastest choice for nearly-sorted data.

<div class="formula">

**Passes: what's guaranteed after $k$ passes**

| Sort | Guaranteed after $k$ passes |
|---|---|
| Selection | first $k$ slots hold the $k$ smallest, in final position |
| Bubble | last $k$ slots hold the $k$ largest, in final position |
| Insertion | first $k+1$ slots are sorted *among themselves* |

</div>

## 4.4 Merge sort

Split the array in half, sort each half recursively, then **merge** the two sorted halves.

```python
def merge(L, R):
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: out.append(L[i]); i += 1    # <= keeps it stable
        else:            out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
```

- $T(n) = 2T(n/2) + \Theta(n)$, so $\Theta(n\log n)$ in the **best, average and worst** cases.
- Merging lists of sizes $m$ and $k$ takes **at most $m + k - 1$** comparisons (when they interleave) and **at least $\min(m, k)$** (when one list is entirely smaller).
- **Stable**, but **not in place**: it needs $\Theta(n)$ extra space.

## 4.5 Quicksort

Choose a **pivot**, **partition** the array into [≤ pivot] pivot [> pivot], then recurse on both sides.

**Lomuto partition** (pivot = last element). This is the version GATE assumes when it says "last element as pivot":

```python
def partition(A, lo, hi):
    pivot = A[hi]; i = lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[hi] = A[hi], A[i+1]
    return i + 1
```

<div class="formula">

| Case | When it happens | Recurrence | Time |
|---|---|---|---|
| Best | pivot is always the median | $2T(n/2) + n$ | $\Theta(n\log n)$ |
| Average / expected | random input or random pivot | $\frac1n\sum_k [T(k) + T(n-1-k)] + n$ | $\Theta(n\log n)$, about $1.39\,n\log_2 n$ comparisons |
| Worst | pivot is always the min or max (e.g. **sorted input with a first or last pivot**) | $T(n-1) + n$ | $\Theta(n^2)$ |

- **In place**, with $O(\log n)$ stack space on average and $O(n)$ in the worst case.
- **Not stable.**

</div>

## 4.6 The master comparison table

| Algorithm | Best | Average | Worst | Extra space | Stable | In place | Adaptive |
|---|---|---|---|---|---|---|---|
| Selection | $n^2$ | $n^2$ | $n^2$ | $O(1)$ | ✗ | ✓ | ✗ |
| Bubble (with flag) | $n$ | $n^2$ | $n^2$ | $O(1)$ | ✓ | ✓ | ✓ |
| Insertion | $n$ | $n^2$ | $n^2$ | $O(1)$ | ✓ | ✓ | ✓ |
| Merge | $n\log n$ | $n\log n$ | $n\log n$ | $O(n)$ | ✓ | ✗ | ✗ |
| Quick | $n\log n$ | $n\log n$ | $n^2$ | $O(\log n)$ | ✗ | ✓ | ✗ |

**Lower bound:** any **comparison-based** sort needs $\Omega(n\log n)$ comparisons in the worst case. A decision tree must have at least $n!$ leaves, so its height is at least $\log_2 n! = \Theta(n\log n)$.

---

## Summary: important points

<div class="formula">

1. Binary search needs **sorted data and random access**. Worst-case comparisons are $\lfloor\log_2 n\rfloor + 1$ (10 for $n = 1000$).
2. **Bubble swaps = insertion swaps = number of inversions.** Selection makes at most $n - 1$ swaps.
3. Selection and plain bubble always make $\frac{n(n-1)}{2}$ comparisons. Insertion makes $n - 1$ on sorted input.
4. After $k$ passes: selection fixes the **front**, bubble fixes the **back**, and insertion's front is only **relatively** sorted.
5. **Stable:** bubble, insertion, merge. **Not stable:** selection, quick.
6. Quicksort is $\Theta(n^2)$ on sorted input with a first or last pivot. Any constant-fraction split is still $\Theta(n\log n)$.
7. Merge sort is always $\Theta(n\log n)$ but needs $O(n)$ extra space. Merging $m + k$ items takes at most $m + k - 1$ comparisons.
8. Comparison sorts can't beat $\Omega(n\log n)$.

</div>

<div class="trap">

**Traps that cost marks**

- **Count comparisons, not iterations or swaps**, unless the question asks for swaps.
- Does the question mean *plain* bubble sort or the version with an early-exit flag? On sorted input they differ: $\frac{n(n-1)}{2}$ vs $n - 1$.
- In Lomuto partition, a "swap" where $i = j$ doesn't move anything. GATE 2024 counted those as **0** swaps.
- Binary search on a **linked list** isn't $O(\log n)$ time.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q45 (2 marks, MCQ)

Which of (i) bubble, (ii) insertion, (iii) selection sorts `[4, 3, 2, 1, 5]` into increasing order after **exactly two passes**?
(A) (i) only (B) (iii) only (C) (ii) and (iii) (D) (i) and (ii)

<details>
<summary>Show solution</summary>

**Answer: (B) selection only**

Simulate each one literally:

| Sort | After pass 1 | After pass 2 | Sorted? |
|---|---|---|---|
| Bubble | [3, 2, 1, 4, **5**] | [2, 1, 3, **4, 5**] | ✗ |
| Insertion | [**3, 4**, 2, 1, 5] | [**2, 3, 4**, 1, 5] | ✗ |
| Selection | [**1**, 3, 2, 4, 5] | [**1, 2**, 3, 4, 5] | ✓ |

Selection works here because, after placing 1 and 2, the remaining elements [3, 4, 5] happen to already be in order.

</details>

### GATE DA 2026 Q49 (2 marks, MSQ)

$P = [1, 2, 3, 5, 4]$. $N_1$ is the total number of comparisons made by bubble sort (BS) and $N_2$ the number made by insertion sort (IS). Which are correct?
(A) $N_1 = 10, N_2 = 4$ (B) $N_1 > N_2$ (C) IS on $P$ performs only one swap (D) Both BS and IS make at least one unnecessary comparison

<details>
<summary>Show solution</summary>

**Answer: B; C; D**

**Bubble sort** (plain version): $4 + 3 + 2 + 1 = 10$ comparisons. With the early-exit flag it's $4 + 3 = 7$. Either way, $N_1 > N_2$.

**Insertion sort:**

- $i = 1$: compare (1, 2), no shift. 1 comparison.
- $i = 2$: compare (2, 3). 1 comparison.
- $i = 3$: compare (3, 5). 1 comparison.
- $i = 4$: compare (5, 4) and swap, then compare (3, 4) and stop. 2 comparisons.

So $N_2 = $ **5**, not 4, and (A) is false.

- (B) True: $10 > 5$.
- (C) True: $P$ has exactly one inversion, (5, 4), so there's exactly one swap.
- (D) True: both algorithms compare (1, 2), which is already in order.

</details>

### GATE DA 2025 Q29 (1 mark, MSQ)

Insertion sort on `[1, 3, 5, 7, 9, 11, x, 15, 13]` takes **exactly two swaps**. Which values of $x$ are possible?
(A) 10 (B) 12 (C) 14 (D) 16

<details>
<summary>Show solution</summary>

**Answer: A; C**

Insertion swaps = inversions. The pair (15, 13) is always **1** inversion. We need exactly **one more** inversion involving $x$.

| $x$ | Inversions involving $x$ | Total | Valid? |
|---|---|---|---|
| 10 | (11, 10) | 2 | ✓ |
| 12 | none ($11 < 12 < 15$ and $12 < 13$) | 1 | ✗ |
| 14 | (14, 13) | 2 | ✓ |
| 16 | (16, 15), (16, 13) | 3 | ✗ |

</details>

### GATE DA 2024 Q30 (1 mark, NAT)

In-place quicksort with the **last element as pivot** on `[60, 70, 80, 90, 100]`. What is the minimum number of swaps?

<details>
<summary>Show solution</summary>

**Answer: 0**

Run Lomuto partition with pivot = 100. Every element is $\le 100$, so `i` moves forward together with `j`. Each "swap" is `A[i], A[j]` with $i = j$, which moves nothing. The final pivot swap is also with itself. The same thing happens at every recursive level, because the array is already sorted.

No element ever changes position, so the minimum number of real swaps is **0**. Notice what the question is pointing at: this is the **worst case for time** ($\Theta(n^2)$ comparisons) and yet it needs zero swaps.

</details>

### GATE DA 2026 Q31 (1 mark, NAT)

Recursive binary search on a sorted array of **1000** distinct integers, with three-way comparisons. What is the maximum number of comparisons if $y$ isn't in the array?

<details>
<summary>Show solution</summary>

**Answer: 10**

$\lfloor \log_2 1000 \rfloor + 1 = 9 + 1 = 10$. The search range shrinks $1000 \to 499\text{–}500 \to 249\text{–}250 \to \dots \to 1 \to$ empty. That's 10 midpoints examined.

</details>

### GATE DA 2025 Q27 (1 mark, MSQ)

For which inputs does binary search take $O(\log n)$ time in the worst case?
(A) array in any order (B) linked list in any order (C) array in increasing order (D) linked list in increasing order

<details>
<summary>Show solution</summary>

**Answer: (C) only**

The data must be sorted, so (A) and (B) fail: binary search isn't even correct on them. It also needs random access, so (D) fails: finding the middle of a linked list takes $O(n)$.

</details>

---

## Test yourself (B): predicted 2027-style questions

These follow the patterns above, with the variations most likely to show up next.

**F1 (1 mark, NAT).** Selection sort on `[8, 5, 2, 9, 1, 7]`. How many swaps does it make in total? (Don't count a swap of an element with itself.)

<details>
<summary>Show solution</summary>

**Answer: 3**

| Pass | Minimum of the unsorted part | Swap | Array afterwards |
|---|---|---|---|
| 1 | 1 | 8 ↔ 1 | [1, 5, 2, 9, 8, 7] |
| 2 | 2 | 5 ↔ 2 | [1, 2, 5, 9, 8, 7] |
| 3 | 5 | already in place | — |
| 4 | 7 | 9 ↔ 7 | [1, 2, 5, 7, 8, 9] |
| 5 | 8 | already in place | — |

**3 swaps.**

</details>

**F2 (2 marks, NAT).** How many comparisons does insertion sort make on `[8, 5, 2, 9, 1, 7]`?

<details>
<summary>Show solution</summary>

**Answer: 11**

The array has 9 inversions: 8 is bigger than 4 later elements, 5 than 2, 2 than 1, 9 than 2, and 1 than none ($4 + 2 + 1 + 2 + 0 = 9$).

| $i$ | Element | Shifts | Comparisons |
|---|---|---|---|
| 1 | 5 | 1 (reaches the front) | 1 |
| 2 | 2 | 2 (reaches the front) | 2 |
| 3 | 9 | 0 | 1 |
| 4 | 1 | 4 (reaches the front) | 4 |
| 5 | 7 | 2, then stops at 5 | 3 |

Total = **11**.

</details>

**F3 (2 marks, MSQ).** Which statements are true?
(A) Bubble sort with an early-exit flag makes $n - 1$ comparisons on sorted input (B) Insertion sort makes exactly as many swaps as bubble sort on every input (C) Selection sort is stable (D) Merge sort makes $\Theta(n\log n)$ comparisons even on sorted input

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

- **(A)** One pass with no swaps, then it stops. True.
- **(B)** Both equal the number of inversions. True.
- **(C)** Its long-distance swaps can reorder equal keys. False.
- **(D)** Merge sort always splits and merges completely. On sorted input each merge uses about half the maximum comparisons, but that's still $\Theta(n\log n)$. True.

</details>

**F4 (2 marks, NAT).** Run one Lomuto partition (pivot = last element) on `[7, 2, 9, 4, 3, 8, 5]`. Including the final pivot swap, how many swaps actually exchange two different positions?

<details>
<summary>Show solution</summary>

**Answer: 4**

Pivot = 5 and `i = -1`.

| j | A[j] | ≤ 5? | Action | Array |
|---|---|---|---|---|
| 0 | 7 | no | — | [7, 2, 9, 4, 3, 8, 5] |
| 1 | 2 | yes | i = 0, swap A[0] ↔ A[1] | [2, 7, 9, 4, 3, 8, 5] |
| 2 | 9 | no | — | |
| 3 | 4 | yes | i = 1, swap A[1] ↔ A[3] | [2, 4, 9, 7, 3, 8, 5] |
| 4 | 3 | yes | i = 2, swap A[2] ↔ A[4] | [2, 4, 3, 7, 9, 8, 5] |
| 5 | 8 | no | — | |

Final step: swap A[3] ↔ A[6], giving [2, 4, 3, **5**, 9, 8, 7].

Every one of these swaps exchanges two different positions, so the answer is **4**. Don't skip the final pivot swap; it's the step people most often forget.

</details>

**F5 (1 mark, NAT).** What is the maximum number of comparisons needed to merge two sorted lists of sizes 5 and 7?

<details>
<summary>Show solution</summary>

**Answer: 11**

The worst case is when the lists interleave perfectly, and one element is output per comparison until a list runs out: $m + k - 1 = 5 + 7 - 1 = 11$.

</details>

**F6 (2 marks, MCQ).** Quicksort always picks the **median** as its pivot, but finding the median costs $\Theta(n^2)$ per call. What is the total time?
(A) $\Theta(n\log n)$ (B) $\Theta(n^2)$ (C) $\Theta(n^2\log n)$ (D) $\Theta(n^3)$

<details>
<summary>Show solution</summary>

**Answer: (B)**

$T(n) = 2T(n/2) + \Theta(n^2)$. Here $d = 2 > \log_2 2 = 1$, so the root dominates (Master case 1), giving $\Theta(n^2)$.

</details>

**F7 (1 mark, NAT).** A sorted array has 100 elements. What is the maximum number of three-way comparisons binary search makes?

<details>
<summary>Show solution</summary>

**Answer: 7**

$\lfloor\log_2 100\rfloor + 1 = 6 + 1 = 7$.

</details>
