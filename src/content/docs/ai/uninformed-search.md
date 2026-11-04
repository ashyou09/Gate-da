---
title: 1. Uninformed search
description: Search problem formulation, tree vs graph search, BFS, DFS, uniform-cost search, depth-limited and iterative deepening search, with completeness, optimality, time and space compared.
sidebar:
  label: 1. Uninformed search
  order: 1
---

**Why it matters:** 2024 Q44 asked how many states BFS and DFS expand before reaching a goal. 2026 Q13 asked which algorithm is **not** uninformed. The properties table in §1.6 answers most "which algorithm is optimal/complete" MSQs on its own.

## Topic map

<div class="mindmap">

- **Uninformed (blind) search**
  - Problem formulation
    - initial state, actions, transition model, goal test, path cost
    - tree search vs graph search (explored set)
  - Strategies (by frontier data structure)
    - BFS: FIFO queue
    - DFS: LIFO stack
    - UCS: priority queue on path cost $g$
    - depth-limited, iterative deepening (IDS)
  - Evaluation
    - complete? optimal? time? space?
    - $b$ branching factor, $d$ depth of shallowest goal, $m$ max depth

</div>

## 1.1 What a search problem is

<div class="formula">

A search problem has:

1. an **initial state**;
2. **actions** available in each state;
3. a **transition model** (which state an action leads to);
4. a **goal test**;
5. a **path cost** (the sum of step costs).

A **solution** is a sequence of actions from the start to a goal. An **optimal** solution has the lowest path cost.

</div>

Every search algorithm keeps a **frontier** (generated nodes waiting to be expanded). **Expanding** a node means generating its successors. The only difference between the algorithms is **which frontier node they expand next**.

- **Tree search** may revisit the same state many times.
- **Graph search** keeps an **explored set** and skips states it has already expanded. GATE questions usually say which one they mean ("previously expanded states are not added").

**Uninformed** search uses **no knowledge about how close a state is to the goal**, only the problem definition. Using a heuristic estimate $h(n)$ makes a search **informed** (A\*, greedy best-first, topic 2).

## 1.2 Breadth-first search (BFS)

The frontier is a **FIFO queue**, so all nodes at depth $d$ are expanded before any node at depth $d + 1$.

- **Complete** if the branching factor $b$ is finite.
- **Optimal when every step costs the same**, because it finds the **shallowest** goal.
- Time and space are $O(b^d)$. **Memory is the real problem**: BFS stores a whole level.

## 1.3 Depth-first search (DFS)

The frontier is a **LIFO stack** (or recursion). It always expands the deepest node first.

- **Not complete** in infinite or cyclic spaces with tree search, since it can go down forever. It is complete with graph search on a finite space.
- **Not optimal**: it returns whatever goal it reaches first.
- Time $O(b^m)$ with $m$ the maximum depth, but space only **$O(bm)$**: one path plus the siblings along it.

<!-- fig:search-bfs-dfs -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 270" role="img" aria-label="BFS versus DFS expansion order" xmlns="http://www.w3.org/2000/svg"><text class="title" x="155" y="16" text-anchor="middle">BFS (queue)</text><line class="grid" x1="155" y1="40" x2="80.0" y2="102" style="stroke-width:1.4"/><line class="grid" x1="155" y1="40" x2="230.0" y2="102" style="stroke-width:1.4"/><line class="grid" x1="80.0" y1="102" x2="42.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="80.0" y1="102" x2="117.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="42.5" y1="164" x2="23.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="42.5" y1="164" x2="61.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="117.5" y1="164" x2="98.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="117.5" y1="164" x2="136.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="230.0" y1="102" x2="192.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="230.0" y1="102" x2="267.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="192.5" y1="164" x2="173.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="192.5" y1="164" x2="211.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="267.5" y1="164" x2="248.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="267.5" y1="164" x2="286.25" y2="226" style="stroke-width:1.4"/><circle class="box-ink" cx="155" cy="40" r="12"/><text class="on-ink" x="155" y="44" text-anchor="middle">1</text><circle class="box-ink" cx="80.0" cy="102" r="12"/><text class="on-ink" x="80.0" y="106" text-anchor="middle">2</text><circle class="box-ink" cx="42.5" cy="164" r="12"/><text class="on-ink" x="42.5" y="168" text-anchor="middle">4</text><circle class="box" cx="23.75" cy="226" r="12"/><text class="" x="23.75" y="230" text-anchor="middle">8</text><circle class="box" cx="61.25" cy="226" r="12"/><text class="" x="61.25" y="230" text-anchor="middle">9</text><circle class="box-ink" cx="117.5" cy="164" r="12"/><text class="on-ink" x="117.5" y="168" text-anchor="middle">5</text><circle class="box" cx="98.75" cy="226" r="12"/><text class="" x="98.75" y="230" text-anchor="middle">10</text><circle class="box" cx="136.25" cy="226" r="12"/><text class="" x="136.25" y="230" text-anchor="middle">11</text><circle class="box-ink" cx="230.0" cy="102" r="12"/><text class="on-ink" x="230.0" y="106" text-anchor="middle">3</text><circle class="box" cx="192.5" cy="164" r="12"/><text class="" x="192.5" y="168" text-anchor="middle">6</text><circle class="box" cx="173.75" cy="226" r="12"/><text class="" x="173.75" y="230" text-anchor="middle">12</text><circle class="box" cx="211.25" cy="226" r="12"/><text class="" x="211.25" y="230" text-anchor="middle">13</text><circle class="box" cx="267.5" cy="164" r="12"/><text class="" x="267.5" y="168" text-anchor="middle">7</text><circle class="box" cx="248.75" cy="226" r="12"/><text class="" x="248.75" y="230" text-anchor="middle">14</text><circle class="box" cx="286.25" cy="226" r="12"/><text class="" x="286.25" y="230" text-anchor="middle">15</text><text class="title" x="465" y="16" text-anchor="middle">DFS (stack)</text><line class="grid" x1="465" y1="40" x2="390.0" y2="102" style="stroke-width:1.4"/><line class="grid" x1="465" y1="40" x2="540.0" y2="102" style="stroke-width:1.4"/><line class="grid" x1="390.0" y1="102" x2="352.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="390.0" y1="102" x2="427.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="352.5" y1="164" x2="333.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="352.5" y1="164" x2="371.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="427.5" y1="164" x2="408.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="427.5" y1="164" x2="446.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="540.0" y1="102" x2="502.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="540.0" y1="102" x2="577.5" y2="164" style="stroke-width:1.4"/><line class="grid" x1="502.5" y1="164" x2="483.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="502.5" y1="164" x2="521.25" y2="226" style="stroke-width:1.4"/><line class="grid" x1="577.5" y1="164" x2="558.75" y2="226" style="stroke-width:1.4"/><line class="grid" x1="577.5" y1="164" x2="596.25" y2="226" style="stroke-width:1.4"/><circle class="box-ink" cx="465" cy="40" r="12"/><text class="on-ink" x="465" y="44" text-anchor="middle">1</text><circle class="box-ink" cx="390.0" cy="102" r="12"/><text class="on-ink" x="390.0" y="106" text-anchor="middle">2</text><circle class="box-ink" cx="352.5" cy="164" r="12"/><text class="on-ink" x="352.5" y="168" text-anchor="middle">3</text><circle class="box-ink" cx="333.75" cy="226" r="12"/><text class="on-ink" x="333.75" y="230" text-anchor="middle">4</text><circle class="box-ink" cx="371.25" cy="226" r="12"/><text class="on-ink" x="371.25" y="230" text-anchor="middle">5</text><circle class="box" cx="427.5" cy="164" r="12"/><text class="" x="427.5" y="168" text-anchor="middle">6</text><circle class="box" cx="408.75" cy="226" r="12"/><text class="" x="408.75" y="230" text-anchor="middle">7</text><circle class="box" cx="446.25" cy="226" r="12"/><text class="" x="446.25" y="230" text-anchor="middle">8</text><circle class="box" cx="540.0" cy="102" r="12"/><text class="" x="540.0" y="106" text-anchor="middle">9</text><circle class="box" cx="502.5" cy="164" r="12"/><text class="" x="502.5" y="168" text-anchor="middle">10</text><circle class="box" cx="483.75" cy="226" r="12"/><text class="" x="483.75" y="230" text-anchor="middle">11</text><circle class="box" cx="521.25" cy="226" r="12"/><text class="" x="521.25" y="230" text-anchor="middle">12</text><circle class="box" cx="577.5" cy="164" r="12"/><text class="" x="577.5" y="168" text-anchor="middle">13</text><circle class="box" cx="558.75" cy="226" r="12"/><text class="" x="558.75" y="230" text-anchor="middle">14</text><circle class="box" cx="596.25" cy="226" r="12"/><text class="" x="596.25" y="230" text-anchor="middle">15</text><text class="t-mut" x="310" y="262" text-anchor="middle">numbers = expansion order; the first 5 expansions are filled</text></svg><figcaption>The order in which BFS and DFS expand the same binary tree (children visited left to right). BFS goes level by level using a FIFO queue; DFS goes as deep as possible first using a LIFO stack. BFS needs memory for a whole level (b^d nodes); DFS only for one path and its siblings (b·m).</figcaption></figure>
<!-- /fig:search-bfs-dfs -->

## 1.4 Uniform-cost search (UCS)

The frontier is a **priority queue ordered by path cost $g(n)$**. UCS always expands the cheapest node so far, which is Dijkstra's algorithm with a goal test.

- **Optimal for any non-negative step costs**, provided the goal test is applied when a node is **expanded** (popped), not when it's generated.
- Complete if every step cost is $\ge \varepsilon > 0$.
- With equal step costs, UCS behaves like BFS.

<!-- fig:search-ucs -->
<figure class="diagram"><svg class="dg" viewBox="0 0 700 220" role="img" aria-label="Weighted graph comparing BFS and uniform-cost search" xmlns="http://www.w3.org/2000/svg"><line class="hl" x1="63.4" y1="113.3" x2="174.8" y2="57.6" style=""/><path class="hl" style="fill:none" d="M169.4,64.8 L174.8,57.6 L165.9,57.6"/><text class="t-mut" x="124.9" y="98.8" text-anchor="middle">1</text><line class="ax" x1="63.6" y1="126.4" x2="204.6" y2="192.8" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M195.7,193.0 L204.6,192.8 L199.1,185.7"/><text class="t-mut" x="130.3" y="174.0" text-anchor="middle">5</text><line class="hl" x1="205.0" y1="50.0" x2="333.0" y2="50.0" style=""/><path class="hl" style="fill:none" d="M325.0,54.0 L333.0,50.0 L325.0,46.0"/><text class="t-mut" x="270.0" y="65.0" text-anchor="middle">3</text><line class="ax" x1="203.1" y1="57.3" x2="315.1" y2="119.7" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M306.2,119.3 L315.1,119.7 L310.1,112.3"/><text class="t-mut" x="254.6" y="102.6" text-anchor="middle">1</text><line class="ax" x1="234.2" y1="195.3" x2="473.9" y2="115.4" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M467.5,121.7 L473.9,115.4 L465.0,114.1"/><text class="t-mut" x="358.5" y="169.4" text-anchor="middle">2</text><line class="hl" x1="363.8" y1="55.9" x2="474.4" y2="103.3" style=""/><path class="hl" style="fill:none" d="M465.4,103.8 L474.4,103.3 L468.6,96.5"/><text class="t-mut" x="415.7" y="94.1" text-anchor="middle">1</text><line class="ax" x1="344.9" y1="126.3" x2="473.1" y2="111.9" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M465.6,116.8 L473.1,111.9 L464.7,108.8"/><text class="t-mut" x="411.2" y="133.9" text-anchor="middle">6</text><circle class="box-ink" cx="50" cy="120" r="15"/><text class="on-ink" x="50" y="124" text-anchor="middle">S</text><circle class="box-ink" cx="190" cy="50" r="15"/><text class="on-ink" x="190" y="54" text-anchor="middle">A</text><circle class="box" cx="220" cy="200" r="15"/><text class="title" x="220" y="204" text-anchor="middle">B</text><circle class="box-ink" cx="350" cy="50" r="15"/><text class="on-ink" x="350" y="54" text-anchor="middle">C</text><circle class="box" cx="330" cy="128" r="15"/><text class="title" x="330" y="132" text-anchor="middle">D</text><circle class="box-ink" cx="490" cy="110" r="15"/><text class="on-ink" x="490" y="114" text-anchor="middle">G</text><text class="t-mut" x="540" y="60">BFS: S-B-G, cost 7</text><text class="t-ink" x="540" y="84">UCS: S-A-C-G, cost 5</text></svg><figcaption>A weighted graph from S to the goal G. BFS finds the path with the fewest edges, S → B → G (cost 7). Uniform-cost search always expands the cheapest frontier node, so it finds the cheapest path S → A → C → G (cost 5, highlighted).</figcaption></figure>
<!-- /fig:search-ucs -->

UCS trace on this graph, as (node, g) in expansion order: (S,0), (A,1), (D,2), (C,4), (B,5), (G,5). The goal is popped with $g = 5$, via S → A → C → G.

## 1.5 Depth-limited and iterative deepening search

- **Depth-limited search (DLS):** DFS that refuses to go below a depth limit $\ell$. It's incomplete if the goal is deeper than $\ell$.
- **Iterative deepening (IDS):** run DLS with $\ell = 0, 1, 2, \dots$ until a goal is found. It combines DFS's **$O(bd)$ memory** with BFS's **completeness and optimality** for unit costs.

Repeating the shallow levels costs surprisingly little. The nodes generated by IDS are

$$
(d + 1)\,b^0 + d\,b^1 + (d - 1)\,b^2 + \dots + 1\cdot b^d = O(b^d).
$$

For $b = 10$ and $d = 5$, that's 123,456 nodes, versus 111,111 for BFS: only about 11% more.

## 1.6 Comparison table (memorise this)

<div class="formula">

| | BFS | UCS | DFS | DLS | IDS |
|---|---|---|---|---|---|
| Frontier | FIFO queue | priority queue on $g$ | LIFO stack | stack + depth limit | repeated DLS |
| Complete? | yes¹ | yes¹ ² | no (yes on finite graphs with an explored set) | no (if $\ell < d$) | yes¹ |
| Optimal? | yes, for equal step costs | **yes** | no | no | yes, for equal step costs |
| Time | $O(b^d)$ | $O(b^{1 + \lfloor C^*/\varepsilon\rfloor})$ | $O(b^m)$ | $O(b^\ell)$ | $O(b^d)$ |
| Space | $O(b^d)$ | $O(b^{1 + \lfloor C^*/\varepsilon\rfloor})$ | $O(bm)$ | $O(b\ell)$ | $O(bd)$ |

¹ if $b$ is finite. ² if every step cost is $\ge \varepsilon > 0$. $C^*$ is the optimal cost.

</div>

---

## Summary: important points

<div class="formula">

1. The algorithms differ only in which frontier node they expand next: FIFO (BFS), LIFO (DFS), cheapest $g$ (UCS).
2. Uninformed search uses no heuristic. **A\* and greedy best-first are informed.**
3. BFS is complete and optimal for unit costs, but needs $O(b^d)$ memory.
4. DFS is neither complete nor optimal in general, but needs only $O(bm)$ memory.
5. UCS is optimal for non-negative costs when it tests for the goal on expansion.
6. IDS has DFS memory with BFS guarantees, and only a small overhead.
7. Graph search uses an explored set to avoid re-expanding states.

</div>

<div class="trap">

- BFS is optimal only when **all step costs are equal**. Otherwise use UCS.
- Count **expanded** nodes, not generated ones, unless the question says otherwise.
- DFS finds *a* goal, not the shallowest one.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q44 (2 marks, MCQ)

The start state is 1, and the successors of $n$ are $n + 1$ and $n + 2$. States are expanded in ascending order, and previously expanded states are not re-added. When the goal state 6 is reached:
(A) BFS expands more states than DFS (B) DFS expands more than BFS (C) both expand the same number (D) neither reaches 6

<details>
<summary>Show solution</summary>

**Answer: (C)**

- **BFS** (FIFO): it expands 1 (adding 2, 3), then 2 (adding 4), then 3 (adding 5), then 4 (adding 6), then 5, and then reaches 6. That's 5 expansions: 1, 2, 3, 4, 5.
- **DFS** (ascending, so the smaller child first): it goes 1 → 2 → 3 → 4 → 5 → 6, always taking $n + 1$. Again 5 expansions: 1, 2, 3, 4, 5.

Both expand 5 states. If the goal is instead tested when 6 is **generated**, both stop after 4 expansions. They're equal under either convention (I simulated both).

</details>

### GATE DA 2026 Q13 (1 mark, MCQ)

Which of these is **not** an uninformed search?
(A) BFS (B) DFS (C) A* (D) depth-limited search

<details>
<summary>Show solution</summary>

**Answer: (C)**

A* orders its frontier by $f = g + h$, and the heuristic $h$ is problem-specific knowledge. That makes it **informed** search.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, MCQ).** On the graph in §1.4, which path does BFS return, and what does it cost?
(A) S-A-C-G, 5 (B) S-B-G, 7 (C) S-A-D-G, 8 (D) S-B-G, 5

<details>
<summary>Show solution</summary>

**Answer: (B)**

BFS minimises the **number of edges**, which is 2 for S → B → G. Its cost is $5 + 2 = 7$, more than UCS's 5.

</details>

**F2 (2 marks, MSQ).** Which statements are true?
(A) UCS is optimal when every step cost is positive (B) BFS is optimal for arbitrary positive step costs (C) IDS uses $O(bd)$ memory (D) DFS with an explored set is complete on finite graphs

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: with unequal costs, the shallowest goal needn't be the cheapest (see F1).

</details>

**F3 (1 mark, NAT).** With branching factor 10 and the goal at depth 5, how many nodes does IDS generate in total (counting the root once per iteration)?

<details>
<summary>Show solution</summary>

**Answer: 123456**

$6 \cdot 1 + 5 \cdot 10 + 4 \cdot 100 + 3 \cdot 1000 + 2 \cdot 10^4 + 1 \cdot 10^5 = 123456$.

</details>

**F4 (1 mark, MCQ).** Which uninformed strategy uses the least memory and is still complete and optimal for unit step costs?
(A) BFS (B) DFS (C) IDS (D) UCS

<details>
<summary>Show solution</summary>

**Answer: (C)**

IDS has $O(bd)$ space with BFS's guarantees.

</details>

**F5 (2 marks, NAT).** On the graph in §1.4, UCS breaks ties between equal $g$ values alphabetically. How many nodes are popped from the frontier, counting S and G?

<details>
<summary>Show solution</summary>

**Answer: 6**

The pops are S (0), A (1), D (2), C (4), then B and G tie at 5. Alphabetically B comes first, then G. That's **6** pops.

</details>
