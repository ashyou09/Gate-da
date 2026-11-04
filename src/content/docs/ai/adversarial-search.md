---
title: 3. Adversarial search — minimax & alpha-beta
description: Two-player zero-sum games, game trees, the minimax algorithm, alpha-beta pruning with α and β bounds, when a branch is pruned, move ordering and complexity, and depth-limited search with evaluation functions.
sidebar:
  label: 3. Minimax & alpha-beta
  order: 3
---

**Why it matters:** a game-tree question appeared **every year**:
- 2024 Q25: what α and β mean;
- 2025 Q43: for which leaf values a branch is pruned;
- 2026 Q30: MAX's best move.

Each is a short trace, if you know exactly when to prune. Every answer here was also run through a small alpha–beta program.

## Topic map

<div class="mindmap">

- **Adversarial search**
  - Games
    - two players (MAX, MIN), turn-taking, zero-sum, perfect information
    - terminal states with utilities
  - Minimax
    - MAX takes the max of its children, MIN the min
    - optimal against an optimal opponent
    - time $O(b^m)$, space $O(bm)$
  - Alpha–beta
    - α = best value MAX can guarantee so far (lower bound)
    - β = best value MIN can guarantee so far (upper bound)
    - prune when α ≥ β
    - same root value as minimax
    - best ordering $O(b^{m/2})$
  - Practical play
    - depth limit + evaluation function
    - expectimax for chance nodes

</div>

## 3.1 Games as search

A **two-player zero-sum game** has players **MAX** and **MIN** who take turns. One player's gain is the other's loss, so a single number, the **utility** at a terminal state, describes the outcome. MAX wants it high and MIN wants it low.

A **game tree** alternates MAX levels (drawn as △) and MIN levels (▽), with utilities at the leaves.

## 3.2 Minimax

<div class="formula">

$$
\text{MINIMAX}(n) =
\begin{cases}
\text{utility}(n) & n \text{ terminal}\\
\max_{c}\ \text{MINIMAX}(c) & n \text{ is a MAX node}\\
\min_{c}\ \text{MINIMAX}(c) & n \text{ is a MIN node}
\end{cases}
$$

- Compute the values **bottom-up**.
- MAX's best move is the child with the largest minimax value.
- Minimax is optimal **if the opponent plays optimally**. Against a weaker opponent, MAX does at least as well.
- It's a complete depth-first exploration: time $O(b^m)$, space $O(bm)$.

</div>

## 3.3 Alpha–beta pruning

Minimax looks at every leaf. Alpha–beta gets the **same root value** while skipping branches that **can't affect the decision**.

<div class="formula">

- **α** = the **highest** value MAX is already guaranteed along the current path: a lower bound for MAX.
- **β** = the **lowest** value MIN is already guaranteed along the current path: an upper bound for MIN.
- Start with $\alpha = -\infty$ and $\beta = +\infty$, and pass both **down** the tree.
- At a **MAX** node, after each child: $v = \max(v, \text{child})$, $\alpha = \max(\alpha, v)$.
- At a **MIN** node, after each child: $v = \min(v, \text{child})$, $\beta = \min(\beta, v)$.
- **Prune** the remaining children as soon as **$\alpha \ge \beta$**.

</div>

**The intuition behind a prune at a MIN node:** if MIN can already force a value ≤ α, and MAX has a guaranteed α elsewhere, MAX will never come down this branch. So the other children don't matter.

<!-- fig:ab-tree -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 245" role="img" aria-label="Alpha-beta pruning on a two-ply game tree" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="300" y1="46" x2="120" y2="98"/><line class="ax" x1="120" y1="125" x2="68" y2="188"/><rect class="box" x="55" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="68" y="204" text-anchor="middle">3</text><line class="ax" x1="120" y1="125" x2="120" y2="188"/><rect class="box" x="107" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="120" y="204" text-anchor="middle">12</text><line class="ax" x1="120" y1="125" x2="172" y2="188"/><rect class="box" x="159" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="172" y="204" text-anchor="middle">8</text><polygon class="box" points="120,125 104,98 136,98" style="stroke:var(--gd-ink)"/><text class="title" x="120" y="111" text-anchor="middle">3</text><line class="ax" x1="300" y1="46" x2="300" y2="98"/><line class="ax" x1="300" y1="125" x2="248" y2="188"/><rect class="box" x="235" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="248" y="204" text-anchor="middle">2</text><line class="mut" x1="300" y1="125" x2="300" y2="188"/><rect class="grid" x="287" y="188" width="26" height="24" rx="3" style="stroke-dasharray:4 3"/><text class="t-mut" x="300" y="204" text-anchor="middle">4</text><text class="t-warn" x="300" y="228" text-anchor="middle">pruned</text><line class="mut" x1="300" y1="125" x2="352" y2="188"/><rect class="grid" x="339" y="188" width="26" height="24" rx="3" style="stroke-dasharray:4 3"/><text class="t-mut" x="352" y="204" text-anchor="middle">6</text><text class="t-warn" x="352" y="228" text-anchor="middle">pruned</text><polygon class="box" points="300,125 284,98 316,98" style="stroke:var(--gd-ink)"/><text class="title" x="300" y="111" text-anchor="middle">≤2</text><line class="ax" x1="300" y1="46" x2="480" y2="98"/><line class="ax" x1="480" y1="125" x2="428" y2="188"/><rect class="box" x="415" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="428" y="204" text-anchor="middle">14</text><line class="ax" x1="480" y1="125" x2="480" y2="188"/><rect class="box" x="467" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="480" y="204" text-anchor="middle">5</text><line class="ax" x1="480" y1="125" x2="532" y2="188"/><rect class="box" x="519" y="188" width="26" height="24" rx="3" style=""/><text class="title" x="532" y="204" text-anchor="middle">2</text><polygon class="box" points="480,125 464,98 496,98" style="stroke:var(--gd-ink)"/><text class="title" x="480" y="111" text-anchor="middle">2</text><polygon class="box-ink" points="300,19 284,46 316,46" style="stroke:var(--gd-ink)"/><text class="on-ink" x="300" y="39" text-anchor="middle">3</text><text class="t-mut" x="20" y="38">MAX</text><text class="t-mut" x="20" y="114">MIN</text><text class="t-ink" x="345" y="30">α = 3 after the first child</text><text class="t-warn" x="326" y="114" text-anchor="start">2 ≤ α = 3 → stop</text></svg><figcaption>Alpha–beta on the classic tree [[3, 12, 8], [2, 4, 6], [14, 5, 2]], children searched left to right. The first MIN node returns 3, so MAX's α becomes 3. At the second MIN node the first leaf is 2 ≤ α: MIN will return at most 2, which MAX will never choose, so the leaves 4 and 6 are pruned (dashed). The root's minimax value is 3, the same as without pruning.</figcaption></figure>
<!-- /fig:ab-tree -->

### Effect of move ordering

| Ordering | Leaves examined | Effective branching factor |
|---|---|---|
| worst (best moves last) | $O(b^m)$, no pruning | $b$ |
| random | about $O(b^{3m/4})$ | $b^{3/4}$ |
| **perfect** (best moves first) | $O(b^{m/2})$ | $\sqrt b$, which doubles the searchable depth |

Pruning never changes the **root value**. It only changes how much work is done. Internal node values can come out as bounds (like "≤ 2") instead of exact numbers.

## 3.4 Real games: depth limits and chance

- **Depth-limited minimax:** cut the search at depth $d$ and apply an **evaluation function** (an estimate of utility) at the cut-off nodes.
- **Expectimax:** for games with dice, **chance nodes** take the **expected** value $\sum_i p_i\,v_i$ of their children instead of a min or max. Alpha–beta-style pruning is much weaker there.

---

## Summary: important points

<div class="formula">

1. Minimax: MAX nodes take the max of their children, MIN nodes the min. Evaluate bottom-up.
2. α = the highest value guaranteed for MAX (a lower bound). β = the lowest value guaranteed for MIN (an upper bound).
3. Update α at MAX nodes and β at MIN nodes. **Prune when α ≥ β.**
4. At a MIN node: prune once a child's value is ≤ α. At a MAX node: prune once a child's value is ≥ β.
5. Alpha–beta returns the same root value as minimax.
6. With perfect ordering it examines $O(b^{m/2})$ leaves; with the worst ordering, $O(b^m)$.
7. Chance nodes use expected values (expectimax).

</div>

<div class="trap">

- The first child of every node is always examined. Pruning only skips **later** siblings.
- α belongs to MAX (raised by max) and β belongs to MIN (lowered by min). Don't swap them.
- Equality also prunes in the standard version ($\alpha \ge \beta$). Check whether the question uses $>$.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q30 (1 mark, NAT)

MAX moves first with strategies 1, 2 and 3. Then MIN moves with strategies 1, 2 and 3. The leaves are: strategy 1 → (8, 6, −1), strategy 2 → (1, 5, 7), strategy 3 → (−4, −3, −12). What is MAX's best strategy?

<details>
<summary>Show solution</summary>

**Answer: 2**

The MIN values are $\min(8, 6, -1) = -1$, $\min(1, 5, 7) = 1$ and $\min(-4, -3, -12) = -12$. MAX takes the largest, which is 1, from strategy **2**.

(With alpha–beta, the last two leaves of strategy 3 are pruned, because its first leaf −4 is already ≤ α = 1.)

</details>

### GATE DA 2025 Q43 (2 marks, MCQ)

Tree 1: MAX node A has children leaf 2 and MIN node B, where B's children are x and 1. Tree 2: MAX node C has MIN children D (leaves 5, y) and E (leaves 2, …). For which x and y are B's right child and E's right child pruned?
(A) x ∈ [1, ∞), y ∈ (−∞, 2] (B) x ∈ (−∞, 2], y ∈ (−∞, 5] (C) x ∈ (−∞, 2], y ∈ [2, ∞) (D) x ∈ [1, ∞), y ∈ (−∞, 5]

<details>
<summary>Show solution</summary>

**Answer: (C)**

- **Tree 1:** after the leaf 2, A has α = 2. At B, after seeing x, β = x. Prune when $\alpha \ge \beta$, i.e. $2 \ge x$. So **x ≤ 2**.
- **Tree 2:** D's value is $\min(5, y)$, so C's α = $\min(5, y)$. At E, after the leaf 2, β = 2. Prune when $\min(5, y) \ge 2$, i.e. **y ≥ 2**.

I checked x ∈ {0, 2, 3} and y ∈ {1, 2, 6} in code, and the pruning happened exactly where these ranges predict.

</details>

### GATE DA 2024 Q25 (1 mark, MCQ)

"In alpha–beta pruning, α is the (m) value choice found so far along the path for MAX, and β is the (n) value choice found so far for MIN." What are (m) and (n)?

<details>
<summary>Show solution</summary>

**Answer: (C)** (m) = highest, (n) = lowest

MAX keeps the best (highest) value it can guarantee. MIN keeps the best for itself, the lowest.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** For the tree in §3.3, $[[3, 12, 8], [2, 4, 6], [14, 5, 2]]$, how many leaves does alpha–beta prune (left to right)?

<details>
<summary>Show solution</summary>

**Answer: 2**

The leaves 4 and 6 are pruned. At the third MIN node the leaves come in the order 14, 5, 2, so β only reaches 2 at the very last leaf and nothing there is pruned.

</details>

**F2 (2 marks, NAT).** The MAX root has MIN children with leaves [5, 7], [4, 9] and [3, 8]. How many leaves does alpha–beta prune?

<details>
<summary>Show solution</summary>

**Answer: 2**

After the first child, α = 5. The second MIN node sees 4 ≤ 5, so its 9 is pruned. The third sees 3 ≤ 5, so its 8 is pruned. The best child comes first, so pruning is maximal.

</details>

**F3 (2 marks, NAT).** Same leaves, but the children come in the order [3, 8], [4, 9], [5, 7]. How many leaves are pruned?

<details>
<summary>Show solution</summary>

**Answer: 0**

α rises 3 → 4 → 5 one step at a time. Each MIN node's first leaf (4, then 5) is **greater** than the current α, so there's never a cut. This is the worst ordering.

</details>

**F4 (2 marks, NAT).** A three-level tree: MAX root → two MIN nodes → each MIN node has two MAX children → leaves. The leaves, left to right, are (3, 5), (6, 9), (1, 2), (0, −1). What is the minimax value of the root?

<details>
<summary>Show solution</summary>

**Answer: 5**

- MAX level: $\max(3, 5) = 5$, $\max(6, 9) = 9$, $\max(1, 2) = 2$, $\max(0, -1) = 0$.
- MIN level: $\min(5, 9) = 5$, $\min(2, 0) = 0$.
- Root: $\max(5, 0) = 5$.

(Alpha–beta prunes 3 leaves here: 9, and both leaves of (0, −1).)

</details>

**F5 (1 mark, MCQ).** With perfect move ordering, how many leaves does alpha–beta examine, as a function of $b$ and $m$?
(A) $O(b^m)$ (B) $O(b^{3m/4})$ (C) $O(b^{m/2})$ (D) $O(\log b^m)$

<details>
<summary>Show solution</summary>

**Answer: (C)**

</details>
