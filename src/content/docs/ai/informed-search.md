---
title: 2. Informed search & A*
description: Heuristic functions, greedy best-first search, A* with f = g + h, admissible and consistent heuristics, optimality conditions, dominance and combining heuristics, and tracing A* by hand.
sidebar:
  label: 2. Informed search & A*
  order: 2
---

**Why it matters:** 2025 Q44 gave a weighted graph with heuristic values and asked for the **A\* expansion order**. 2024 Q23 asked which combination of admissible heuristics stays admissible. Both depend on the exact definitions on this page.

## Topic map

<div class="mindmap">

- **Informed search**
  - Heuristic $h(n)$
    - estimated cost from $n$ to the nearest goal
  - Greedy best-first
    - expand the lowest $h$: fast, not optimal
  - A*
    - expand the lowest $f(n) = g(n) + h(n)$
    - goal test when popped
  - Heuristic properties
    - admissible: $h \le h^*$ → optimal (tree search)
    - consistent: $h(n) \le c(n, n') + h(n')$ → optimal graph search, $f$ never decreases
    - consistent ⇒ admissible
  - Designing heuristics
    - relaxed problems, dominance, max of admissible heuristics

</div>

## 2.1 Heuristics

A **heuristic** $h(n)$ estimates the cheapest cost from node $n$ to a goal, using knowledge about the problem: straight-line distance on a map, or the number of misplaced tiles in a puzzle. It must satisfy $h(\text{goal}) = 0$. Write $h^*(n)$ for the **true** cheapest cost.

Search algorithms rank frontier nodes with an **evaluation function** $f(n)$:

| Algorithm | $f(n)$ | Optimal? |
|---|---|---|
| Uniform-cost | $g(n)$ | yes |
| Greedy best-first | $h(n)$ | **no**: it rushes towards whatever looks closest |
| **A\*** | $g(n) + h(n)$ | **yes**, with an admissible (tree) or consistent (graph) $h$ |

$g(n)$ is the cost already paid to reach $n$, and $h(n)$ is the estimate of what's left. So $f(n)$ estimates the cost of the cheapest solution **through** $n$.

## 2.2 A* by hand

1. Put the start on the frontier with $f = h(\text{start})$.
2. **Pop** the node with the smallest $f$. If it's the goal, stop. (Test the goal **when popping**, not when generating.)
3. Generate its successors with $g' = g + c$ and $f' = g' + h$. In graph search, skip states already expanded and keep only the best $g$ for each state on the frontier.
4. Repeat.

**Keep a table** of (node, g, h, f) for the frontier, and cross nodes off as you pop them. That's what makes 2025 Q44 quick.

<!-- fig:astar-q44 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 258" role="img" aria-label="A* search on the 2025 Q44 graph" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="52.1" y1="141.2" x2="136.3" y2="80.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M132.1,87.9 L136.3,80.0 L127.4,81.5"/><text class="t-mut" x="101.5" y="122.9" text-anchor="middle">4</text><line class="hl" x1="54.8" y1="152.7" x2="133.3" y2="167.0" style=""/><path class="hl" style="fill:none" d="M124.7,169.5 L133.3,167.0 L126.1,161.6"/><text class="t-mut" x="93.0" y="174.8" text-anchor="middle">1</text><line class="ax" x1="165.0" y1="70.0" x2="243.0" y2="70.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M235.0,74.0 L243.0,70.0 L235.0,66.0"/><text class="t-mut" x="205.0" y="85.0" text-anchor="middle">2</text><line class="ax" x1="275.0" y1="70.0" x2="353.0" y2="70.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M345.0,74.0 L353.0,70.0 L345.0,66.0"/><text class="t-mut" x="315.0" y="85.0" text-anchor="middle">2</text><line class="hl" x1="163.7" y1="163.8" x2="354.5" y2="77.0" style=""/><path class="hl" style="fill:none" d="M348.9,84.0 L354.5,77.0 L345.6,76.7"/><text class="t-mut" x="264.6" y="134.0" text-anchor="middle">2</text><line class="hl" x1="381.7" y1="79.4" x2="456.7" y2="139.4" style=""/><path class="hl" style="fill:none" d="M448.0,137.5 L456.7,139.4 L453.0,131.3"/><text class="t-mut" x="413.1" y="122.6" text-anchor="middle">3</text><line class="hl" x1="485.0" y1="150.0" x2="553.0" y2="150.0" style=""/><path class="hl" style="fill:none" d="M545.0,154.0 L553.0,150.0 L545.0,146.0"/><text class="t-mut" x="520.0" y="165.0" text-anchor="middle">3</text><circle class="box-ink" cx="40" cy="150" r="15"/><text class="on-ink" x="40" y="154" text-anchor="middle">S</text><text class="t-hl" x="40" y="129" text-anchor="middle">h=–</text><circle class="box" cx="150" cy="70" r="15"/><text class="title" x="150" y="74" text-anchor="middle">A</text><text class="t-hl" x="150" y="49" text-anchor="middle">h=2</text><circle class="box" cx="260" cy="70" r="15"/><text class="title" x="260" y="74" text-anchor="middle">B</text><text class="t-hl" x="260" y="49" text-anchor="middle">h=2</text><circle class="box-ink" cx="370" cy="70" r="15"/><text class="on-ink" x="370" y="74" text-anchor="middle">C</text><text class="t-hl" x="370" y="49" text-anchor="middle">h=6</text><circle class="box-ink" cx="150" cy="170" r="15"/><text class="on-ink" x="150" y="174" text-anchor="middle">E</text><text class="t-hl" x="150" y="149" text-anchor="middle">h=6</text><circle class="box-ink" cx="470" cy="150" r="15"/><text class="on-ink" x="470" y="154" text-anchor="middle">D</text><text class="t-hl" x="470" y="129" text-anchor="middle">h=2</text><circle class="box-ink" cx="570" cy="150" r="15"/><text class="on-ink" x="570" y="154" text-anchor="middle">G</text><text class="t-hl" x="570" y="129" text-anchor="middle">h=0</text><text class="title" x="40" y="225">pop order</text><rect class="box" x="102" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="132" y="225" text-anchor="middle" style="font-weight:700">1. S</text><text class="t-mut" x="132" y="240" text-anchor="middle">f=0</text><rect class="box" x="170" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="200" y="225" text-anchor="middle" style="font-weight:700">2. A</text><text class="t-mut" x="200" y="240" text-anchor="middle">f=6</text><rect class="box" x="238" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="268" y="225" text-anchor="middle" style="font-weight:700">3. E</text><text class="t-mut" x="268" y="240" text-anchor="middle">f=7</text><rect class="box" x="306" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="336" y="225" text-anchor="middle" style="font-weight:700">4. B</text><text class="t-mut" x="336" y="240" text-anchor="middle">f=8</text><rect class="box" x="374" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="404" y="225" text-anchor="middle" style="font-weight:700">5. C</text><text class="t-mut" x="404" y="240" text-anchor="middle">f=9</text><rect class="box" x="442" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="472" y="225" text-anchor="middle" style="font-weight:700">6. D</text><text class="t-mut" x="472" y="240" text-anchor="middle">f=8</text><rect class="box" x="510" y="210" width="60" height="36" rx="6"/><text class="t-ink" x="540" y="225" text-anchor="middle" style="font-weight:700">7. G</text><text class="t-mut" x="540" y="240" text-anchor="middle">f=9</text></svg><figcaption>The 2025 Q44 graph redrawn with step costs on the edges and h above each node. A* pops nodes in order of f = g + h: S(0), A(6), E(7), B(8), C(9), D(8), G(9). The optimal path S → E → C → D → G (cost 9) is highlighted. Note h(C) = 6 > c(C,D) + h(D) = 5, so this h is admissible but not consistent: f drops from 9 at C to 8 at D.</figcaption></figure>
<!-- /fig:astar-q44 -->

## 2.3 Admissible and consistent heuristics

<div class="formula">

**Admissible:** $h$ never **over**estimates: $0 \le h(n) \le h^*(n)$ for every $n$.
→ A\* **tree** search is optimal.

**Consistent (monotone):** for every edge $n \to n'$ with cost $c$:

$$
h(n) \le c(n, n') + h(n'), \qquad h(\text{goal}) = 0.
$$

→ $f$ never decreases along a path, the first time a node is popped its $g$ is already optimal, and A\* **graph** search is optimal without re-opening nodes.

**Consistent ⇒ admissible** (by induction along the optimal path). The converse is false.

</div>

In 2025 Q44, $h(C) = 6 > c(C, D) + h(D) = 3 + 2 = 5$, so $h$ is **admissible but not consistent**, and $f$ drops from 9 at C to 8 at D. A\* still found the optimal path here, but with inconsistent heuristics, graph search may have to re-open nodes to guarantee it.

**Why admissibility gives optimality, intuitively:** suppose a sub-optimal goal $G_2$ is on the frontier. Some node $n$ on the optimal path is also on the frontier, with $f(n) = g(n) + h(n) \le g(n) + h^*(n) = C^* < g(G_2) = f(G_2)$. So $n$ is always popped before $G_2$, and A\* reaches the optimal goal first.

## 2.4 Comparing and combining heuristics

<div class="formula">

- **Dominance:** if $h_2(n) \ge h_1(n)$ for all $n$ and both are admissible, then $h_2$ is **better informed**: A\* with $h_2$ expands no more nodes than with $h_1$.
- If $h_1$ and $h_2$ are admissible, then $\max(h_1, h_2)$, $\min(h_1, h_2)$, any convex combination $\lambda h_1 + (1 - \lambda)h_2$, and $|h_1 - h_2|$ are **admissible**.
- **Not** guaranteed admissible: $h_1 + h_2$, $h_1 \times h_2$, $h_1/h_2$, or $c\cdot h_1$ with $c > 1$.
- $h = 0$ is admissible and consistent, and turns A\* into UCS. $h = h^*$ is perfect: A\* expands only nodes on an optimal path.

</div>

**Why $|h_1 - h_2|$ works:** both are non-negative, so $|h_1 - h_2| \le \max(h_1, h_2) \le h^*$.

### Designing heuristics: relaxed problems

Remove a rule from the problem, and the true cost of the **easier** problem is an admissible heuristic for the real one. For the 8-puzzle:

- **$h_1$ = number of misplaced tiles** (relaxation: a tile can jump anywhere);
- **$h_2$ = total Manhattan distance** (relaxation: tiles can slide over each other).

$h_2 \ge h_1$ always, so $h_2$ dominates.

## 2.5 Other informed methods (one line each)

- **Weighted A\*:** $f = g + w\,h$ with $w > 1$. Faster, but the solution can cost up to $w$ times the optimum.
- **IDA\*:** iterative deepening on an $f$-bound, which saves memory.
- **Hill climbing / local search:** keep only the current state and move to the best neighbour. It can get stuck at local maxima.

---

## Summary: important points

<div class="formula">

1. $f = g + h$ for A\*, $f = h$ for greedy, $f = g$ for UCS.
2. Pop the smallest $f$, and test for the goal **on pop**.
3. Admissible: $h \le h^*$. Then A\* tree search is optimal.
4. Consistent: $h(n) \le c(n, n') + h(n')$. Then $f$ is non-decreasing and graph search is optimal. Consistent ⇒ admissible.
5. Max, min, convex combinations and $|h_1 - h_2|$ of admissible heuristics are admissible. Sums and products may not be.
6. A larger admissible heuristic dominates and expands fewer nodes.
7. Relaxed-problem costs are admissible: misplaced tiles ≤ Manhattan distance ≤ true cost.

</div>

<div class="trap">

- Greedy best-first is **not** optimal, even with an admissible heuristic.
- Admissibility is about **underestimating** the remaining cost, not about $h$ being small at the start.
- In a trace, update a frontier node's $g$ when a cheaper path to it is found.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q44 (2 marks, MCQ)

The graph in §2.2: S→A 4, S→E 1, A→B 2, B→C 2, E→C 2, C→D 3, D→G 3, with h(A)=2, h(B)=2, h(C)=6, h(E)=6, h(D)=2, h(G)=0. In what order does A\* expand the nodes?
(A) S,A,E,C,B,D,G (B) S,E,A,C,B,D,G (C) S,A,E,B,C,D,G (D) S,A,B,E,C,D,G

<details>
<summary>Show solution</summary>

**Answer: (C)**

| Pop | g | f | Frontier afterwards (f) |
|---|---|---|---|
| S | 0 | – | A(4+2=6), E(1+6=7) |
| **A** | 4 | 6 | E(7), B(6+2=8) |
| **E** | 1 | 7 | B(8), C(3+6=9) |
| **B** | 6 | 8 | C(9). C via B would have g = 8, worse than 3, so it's ignored |
| **C** | 3 | 9 | D(6+2=8) |
| **D** | 6 | 8 | G(9+0=9) |
| **G** | 9 | 9 | done: S → E → C → D → G, cost 9 |

</details>

### GATE DA 2024 Q23 (1 mark, MCQ)

$h_1$ and $h_2$ are admissible heuristics. Which is **always** admissible?
(A) $h_1 + h_2$ (B) $h_1 \times h_2$ (C) $h_1/h_2$ (D) $|h_1 - h_2|$

<details>
<summary>Show solution</summary>

**Answer: (D)**

$|h_1 - h_2| \le \max(h_1, h_2) \le h^*$. The others can overestimate. For example, with $h_1 = h_2 = h^* = 3$, the sum is 6 and the product is 9.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** 8-puzzle start state `7 2 4 / 5 _ 6 / 8 3 1`, goal `_ 1 2 / 3 4 5 / 6 7 8`. What is the total Manhattan-distance heuristic $h_2$?

<details>
<summary>Show solution</summary>

**Answer: 18**

Tile by tile: 7 → 3, 2 → 1, 4 → 2, 5 → 2, 6 → 3, 8 → 2, 3 → 2, 1 → 3. The sum is 18. (Misplaced tiles: $h_1 = 8$, every tile. $h_2 \ge h_1$, as dominance says it should be.)

</details>

**F2 (2 marks, NAT).** Edges S→A 2, S→B 3, A→C 2, A→G 7, B→C 2, B→D 4, C→G 4, D→G 2. Heuristics h(S)=5, h(A)=4, h(B)=4, h(C)=3, h(D)=1, h(G)=0. What is the cost of the path A\* returns?

<details>
<summary>Show solution</summary>

**Answer: 8**

The pops are S (f 5), A (f 6), B (f 7), C (f 7, g 4), D (f 8), G (f 8, g 8). The path is S → A → C → G with cost $2 + 2 + 4 = 8$. The other paths cost 9.

This $h$ is consistent, and $h \le h^*$ everywhere ($h^*$: S 8, A 6, B 6, C 4, D 2), so A\* is guaranteed optimal.

</details>

**F3 (2 marks, MSQ).** $h_1$ and $h_2$ are admissible. Which are always admissible?
(A) $\max(h_1, h_2)$ (B) $\min(h_1, h_2)$ (C) $(h_1 + h_2)/2$ (D) $2h_1$

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

$2h_1$ can be up to $2h^*$, so it can overestimate.

</details>

**F4 (1 mark, MCQ).** On the 2025 Q44 graph, which edge makes $h$ inconsistent?
(A) S→A (B) E→C (C) C→D (D) D→G

<details>
<summary>Show solution</summary>

**Answer: (C)**

$h(C) = 6 > 3 + h(D) = 5$. Every other edge satisfies $h(n) \le c + h(n')$.

</details>

**F5 (2 marks, MSQ).** Which statements are true?
(A) Every consistent heuristic is admissible (B) Greedy best-first search with an admissible heuristic is optimal (C) A\* with $h = 0$ behaves like uniform-cost search (D) If $h_2 \ge h_1$ and both are admissible, A\* with $h_2$ expands no more nodes than with $h_1$

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: greedy ignores $g$, so it can return an expensive path.

</details>
