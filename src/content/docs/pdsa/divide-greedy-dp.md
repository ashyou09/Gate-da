---
title: 9. Divide & conquer, greedy & DP basics
description: Recognising the algorithm paradigm, classic divide-and-conquer recurrences, greedy choices that work and fail, and filling DP tables for LCS, knapsack and coin change.
sidebar:
  label: 9. D&C, greedy & DP
  order: 9
---

**Why it matters:** this chapter hasn't been asked directly yet, but its ideas sit underneath questions that were: quicksort's recurrence (2026 Q15), binary search (2024 Q40) and the exponential call tree of naive recursion (2026 Q39). The syllabus names **divide and conquer**. Greedy and DP are the natural "why" behind Dijkstra, Prim and memoisation, and a table-filling NAT is a likely future question.

## Topic map

<div class="mindmap">

- **Algorithm design**
  - Divide & conquer
    - split → solve independent parts → combine
    - merge sort, quicksort, binary search, fast power
    - cost from a recurrence (Master theorem)
  - Greedy
    - take the locally best choice, never undo it
    - works: activity selection, fractional knapsack, Huffman, Dijkstra, Prim, Kruskal
    - fails: 0/1 knapsack, coin change with odd denominations
  - Dynamic programming
    - overlapping subproblems + optimal substructure
    - memoisation (top-down) or a table (bottom-up)
    - cost = states × work per state
    - LCS, 0/1 knapsack, coin change

</div>

## 9.1 How to recognise the paradigm

Ask two questions about the problem:

1. **Do the subproblems overlap?** That is, does the same smaller problem get solved again and again?
   - **No** → divide and conquer.
   - **Yes** → dynamic programming. Memoise it.
2. **Is one locally best choice always safe?** That is, can you commit to a choice without ever needing to undo it?
   - **Yes** (and you can argue why) → greedy.
   - **Not sure** → DP is the safe choice.

| Paradigm | Subproblems | Choice | Typical cost |
|---|---|---|---|
| Divide & conquer | independent | none: solve them all | recurrence $aT(n/b) + f(n)$ |
| Greedy | one remaining subproblem | commit to the best-looking option | usually a sort, $O(n\log n)$ |
| Dynamic programming | overlapping | try every option and keep the best | states × work per state |

## 9.2 Divide and conquer

**Split** the input into smaller independent parts, **solve** each recursively, then **combine** the results.

| Problem | Recurrence | Time |
|---|---|---|
| Binary search | $T(n/2) + 1$ | $\Theta(\log n)$ |
| Merge sort | $2T(n/2) + n$ | $\Theta(n\log n)$ |
| Quicksort (balanced) | $2T(n/2) + n$ | $\Theta(n\log n)$ |
| Max / min by halving | $2T(n/2) + 1$ | $\Theta(n)$ |
| Fast power $x^n$ | $T(n/2) + 1$ | $\Theta(\log n)$ |
| Karatsuba multiplication | $3T(n/2) + n$ | $\Theta(n^{\log_2 3}) \approx n^{1.585}$ |
| Strassen matrix multiplication | $7T(n/2) + n^2$ | $\Theta(n^{\log_2 7}) \approx n^{2.81}$ |
| Counting inversions (merge-sort based) | $2T(n/2) + n$ | $\Theta(n\log n)$ |

**Counting inversions with merge sort:** while merging, each time you take an element from the **right** half, it forms an inversion with every element still waiting in the left half. Add those counts up. This connects to the bubble and insertion swap counts on the [sorting page](/pdsa/searching-sorting/).

**Finding both max and min:** pairing elements up takes $\lceil 3n/2 \rceil - 2$ comparisons, compared with $2n - 2$ done naively.

## 9.3 Greedy algorithms

At each step, take the option that looks best right now, and never reconsider it. This is fast, but it's **correct only for problems with the greedy-choice property**.

### Problems where greedy works

**Activity selection:** sort the activities by **finish time**, then repeatedly pick the next one that starts after the last chosen one finishes. Finishing earliest leaves the most room for the rest.

**Fractional knapsack:** sort items by **value/weight**, take whole items in that order, and take a fraction of the last one.

**Huffman coding:** repeatedly merge the **two least frequent** symbols. The total encoded length equals the **sum of all merged weights**.

**Graph algorithms:** Dijkstra (closest unfinished vertex), Prim (cheapest edge leaving the tree), Kruskal (cheapest edge that doesn't form a cycle).

### Problems where greedy fails (the classic MSQ traps)

- **0/1 knapsack:** you can't take fractions, so the best ratio isn't always optimal.
- **Coin change with denominations {1, 3, 4} for amount 6:** greedy picks 4 + 1 + 1 (3 coins), but 3 + 3 uses only **2**. (Greedy does work for "canonical" systems like {1, 2, 5, 10}.)

## 9.4 Dynamic programming

DP applies when a problem has

1. **optimal substructure:** an optimal solution is built from optimal solutions to subproblems, and
2. **overlapping subproblems:** the same subproblems recur.

Then you solve each distinct subproblem **once** and store the answer.

<div class="formula">

$$
\text{DP running time} = (\text{number of distinct states}) \times (\text{work per state})
$$

- **Top-down:** write the recursion and add a memo dictionary.
- **Bottom-up:** fill a table in an order where each entry's dependencies are already filled.

</div>

### Longest common subsequence (LCS)

$L[i][j]$ is the LCS length of the first $i$ characters of $X$ and the first $j$ characters of $Y$.

$$
L[i][j] =
\begin{cases}
0 & i = 0 \text{ or } j = 0\\
L[i-1][j-1] + 1 & X_i = Y_j\\
\max(L[i-1][j],\; L[i][j-1]) & \text{otherwise}
\end{cases}
\qquad \Theta(mn) \text{ time}
$$

A **subsequence** keeps the order but can skip characters. A **substring** must be contiguous. Don't mix them up.

### 0/1 knapsack

$K[i][c]$ is the best value using the first $i$ items with capacity $c$:

$$
K[i][c] = \max\big(K[i-1][c],\; v_i + K[i-1][c - w_i]\big) \quad (\text{the second option only if } w_i \le c)
\qquad \Theta(nW)
$$

$\Theta(nW)$ is **pseudo-polynomial**: it's polynomial in the *value* $W$, not in the number of bits needed to write $W$.

### Coin change

- **Number of ways:** $\text{ways}[x] \mathrel{+}= \text{ways}[x - c]$, with the **outer loop over coins** so each combination is counted once regardless of order.
- **Minimum coins:** $\text{best}[x] = 1 + \min_{c \le x} \text{best}[x - c]$.

---

## Summary: important points

<div class="formula">

1. Independent subproblems → D&C. Overlapping subproblems → DP. A provably safe local choice → greedy.
2. D&C cost comes from a recurrence: merge sort $\Theta(n\log n)$, Karatsuba $n^{\log_2 3}$, Strassen $n^{\log_2 7}$.
3. Activity selection: sort by **finish** time. Fractional knapsack: sort by **value/weight**. Huffman: merge the two smallest.
4. Greedy **fails** on 0/1 knapsack and on coins like {1, 3, 4}.
5. DP cost = states × work per state. LCS $\Theta(mn)$, knapsack $\Theta(nW)$.
6. Memoisation turns naive Fibonacci from exponential into $\Theta(n)$.

</div>

<div class="trap">

- Sorting activities by **start** time or by **duration** gives wrong answers. Sort by **finish** time.
- Huffman's total cost is the sum of the **merged** weights, not the sum of the original frequencies.
- Subsequence ≠ substring.

</div>

---

## Test yourself (A): previous-year questions

No PDSA question has targeted this chapter directly yet. The closest ones, solved elsewhere on this site:

- **2026 Q15:** expected-time recurrence of quicksort, a divide-and-conquer analysis. See [Complexity & recurrences](/pdsa/complexity-recurrences/).
- **2024 Q40:** binary search as $F(n) = F(\lfloor n/2 \rfloor) + 1$, the simplest D&C recurrence. Same page.
- **2026 Q39:** counting the calls of naive two-branch recursion, which is exactly what memoisation removes. See [Recursion & call counting](/pdsa/recursion-tracing/).

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** What is the length of the LCS of `ABCBDAB` and `BDCABA`?

<details>
<summary>Show solution</summary>

**Answer: 4**

Fill the $7 \times 6$ table using the recurrence. The bottom-right cell is 4. One LCS is `BCBA`: B, C, B, A appear in this order in both strings.

</details>

**F2 (2 marks, NAT).** 0/1 knapsack with capacity 7 and items (weight, value) = (1, 1), (3, 4), (4, 5), (5, 7). What is the maximum value?

<details>
<summary>Show solution</summary>

**Answer: 9**

Compare the feasible subsets with weight $\le 7$:

- {3, 4}: weight 7, value 9
- {1, 5}: weight 6, value 8
- {1, 3}: weight 4, value 5
- {5}: weight 5, value 7

The best is **9**. Note that greedy-by-ratio picks the weight-5 item first (ratio 1.4), then the weight-1 item, getting only 8. That's greedy failing on 0/1 knapsack.

</details>

**F3 (2 marks, MSQ).** Capacity 50, items (weight, value) = (10, 60), (20, 100), (30, 120). Which statements are true?
(A) The fractional optimum is 240 (B) The 0/1 optimum is 220 (C) Greedy by value/weight is optimal for 0/1 here (D) Greedy by value/weight is optimal for the fractional version

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

The ratios are 6, 5 and 4.

- **Fractional:** take the 10 and the 20 (value 160), then 20 of the 30 ($\frac{2}{3} \times 120 = 80$). Total **240**.
- **0/1:** greedy takes 10 + 20 = 160, and the 30 no longer fits. But taking 20 + 30 gives **220**, which is better. So greedy isn't optimal for 0/1, and (C) is false.

</details>

**F4 (2 marks, NAT).** Six characters have frequencies 45, 13, 12, 16, 9, 5. What is the total number of bits in the Huffman encoding (sum of frequency × code length)?

<details>
<summary>Show solution</summary>

**Answer: 224**

Merge the two smallest each time and add up the merged weights:

| Merge | New weight |
|---|---|
| 5 + 9 | 14 |
| 12 + 13 | 25 |
| 14 + 16 | 30 |
| 25 + 30 | 55 |
| 45 + 55 | 100 |

Sum of merged weights: $14 + 25 + 30 + 55 + 100 = $ **224**.

</details>

**F5 (1 mark, NAT).** Activities given as (start, finish): (1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16). What is the maximum number of non-overlapping activities?

<details>
<summary>Show solution</summary>

**Answer: 4**

Sort by finish time and pick greedily:

- (1, 4)
- next start $\ge 4$: (5, 7)
- next start $\ge 7$: (8, 11)
- next start $\ge 11$: (12, 16)

That's **4** activities.

</details>

**F6 (2 marks, MSQ).** For coin denominations {1, 3, 4} and amount 6, which statements are true?
(A) Greedy (largest coin first) uses 3 coins (B) The minimum number of coins is 2 (C) Greedy is optimal for this coin system (D) DP finds the minimum in $O(\text{amount} \times \text{number of coins})$

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

- Greedy: $4 + 1 + 1$, which is 3 coins.
- Optimal: $3 + 3$, which is **2** coins. So greedy isn't optimal, and (C) is false.
- The DP has $6$ states, each trying 3 coins, which is $O(\text{amount} \times k)$.

</details>

**F7 (1 mark, MCQ).** Karatsuba multiplies two $n$-digit numbers with 3 recursive half-size multiplications plus linear work. What is its running time?
(A) $\Theta(n\log n)$ (B) $\Theta(n^{\log_2 3})$ (C) $\Theta(n^2)$ (D) $\Theta(n^{1.5})$

<details>
<summary>Show solution</summary>

**Answer: (B)**

$T(n) = 3T(n/2) + n$. Here $\log_2 3 \approx 1.585 > 1$, so the leaves dominate, giving $\Theta(n^{\log_2 3})$.

</details>
