---
title: 6. Bayesian networks & conditional independence
description: Conditional independence, the chain rule, Bayesian networks as DAGs with CPTs, factorising the joint, parameter counts, chains/forks/colliders, d-separation, Markov blanket, and computing probabilities from CPTs.
sidebar:
  label: 6. Bayesian networks
  order: 6
---

**Why it matters:** 2024 Q24 asked which conditional-independence statement is **false** for a given factorisation. 2024 Q64 asked for a **joint probability** from CPTs. The syllabus phrase "conditional independence representation" means exactly this page. Both answers were also checked numerically from the full joint distribution.

## Topic map

<div class="mindmap">

- **Bayesian networks**
  - Independence
    - $X \perp Y$: $P(x, y) = P(x)P(y)$
    - $X \perp Y \mid Z$: $P(x, y \mid z) = P(x \mid z)P(y \mid z)$
  - Representation
    - DAG + one CPT per node: $P(X \mid \text{Parents}(X))$
    - joint $= \prod_i P(X_i \mid \text{Parents}(X_i))$
    - parameters grow with parents, not with all variables
  - Reading independences
    - each node ⊥ its non-descendants given its parents
    - chain, fork, collider
    - d-separation, explaining away
    - Markov blanket
  - Computing
    - joint = product of CPT entries
    - marginals by summing

</div>

## 6.1 Conditional independence

<div class="formula">

$$
X \perp Y \iff P(X, Y) = P(X)P(Y)
\qquad\qquad
X \perp Y \mid Z \iff P(X, Y \mid Z) = P(X \mid Z)\,P(Y \mid Z)
$$

Equivalently, $P(X \mid Y, Z) = P(X \mid Z)$: once you know $Z$, $Y$ tells you nothing more about $X$.

</div>

Independence and conditional independence **don't imply each other**:

- Two coin flips are independent, but given "exactly one head" they become dependent.
- Rain and wet shoes are dependent, but given "the road is wet" they may be independent.

## 6.2 From the chain rule to a Bayesian network

The **chain rule** factorises any joint distribution:

$$
P(X_1, \dots, X_n) = \prod_{i=1}^{n} P(X_i \mid X_1, \dots, X_{i-1}).
$$

A **Bayesian network** assumes that each variable depends directly only on a few **parents**:

<div class="formula">

$$
P(X_1, \dots, X_n) = \prod_{i=1}^{n} P\big(X_i \mid \text{Parents}(X_i)\big).
$$

- The structure is a **DAG** (directed acyclic graph) with one node per variable.
- Each node stores a **CPT**: $P(X_i \mid \text{parents})$ for every combination of parent values.
- **Parameters:** a node with $k$ values whose parents have $m$ value combinations needs $(k - 1)\cdot m$ numbers. For $n$ binary variables, the full joint needs $2^n - 1$.

</div>

Reading a factorisation as a graph: each factor $P(X \mid \text{parents})$ gives arrows from the parents into $X$. For example, $P(U)P(V)P(W \mid U, V)P(X \mid W)P(Y \mid W)$ means U → W ← V, W → X and W → Y.

<!-- fig:bn-q24 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 560 215" role="img" aria-label="Bayesian network of 2024 Q24" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="102.8" y1="51.2" x2="155.7" y2="97.5" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M147.0,95.2 L155.7,97.5 L152.3,89.2"/><line class="ax" x1="237.2" y1="51.2" x2="184.3" y2="97.5" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M187.7,89.2 L184.3,97.5 L193.0,95.2"/><line class="ax" x1="158.0" y1="122.0" x2="113.4" y2="166.6" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M116.3,158.1 L113.4,166.6 L121.9,163.7"/><line class="ax" x1="182.0" y1="122.0" x2="226.6" y2="166.6" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M218.1,163.7 L226.6,166.6 L223.7,158.1"/><circle class="box" cx="90" cy="40" r="17"/><text class="title" x="90" y="44" text-anchor="middle">U</text><circle class="box" cx="250" cy="40" r="17"/><text class="title" x="250" y="44" text-anchor="middle">V</text><circle class="box-ink" cx="170" cy="110" r="17"/><text class="on-ink" x="170" y="114" text-anchor="middle">W</text><circle class="box" cx="100" cy="180" r="17"/><text class="title" x="100" y="184" text-anchor="middle">X</text><circle class="box" cx="240" cy="180" r="17"/><text class="title" x="240" y="184" text-anchor="middle">Y</text><text class="t-mut" x="320" y="50">given W:</text><text class="t-ink" x="320" y="80">X ⊥ U  ✓</text><text class="t-ink" x="320" y="110">Y ⊥ V  ✓</text><text class="t-ink" x="320" y="140">X ⊥ Y  ✓ (fork blocked)</text><text class="t-warn" x="320" y="170">U ⊥ V  ✗ (collider opened)</text></svg><figcaption>The network for 2024 Q24: P(U)P(V)P(W | U, V)P(X | W)P(Y | W). W is a collider for U and V, and a fork for X and Y. Given W: X ⊥ U, Y ⊥ V and X ⊥ Y all hold, but U and V become dependent.</figcaption></figure>
<!-- /fig:bn-q24 -->

## 6.3 Reading independences: chain, fork, collider

<!-- fig:bn-structures -->
<figure class="diagram"><svg class="dg" viewBox="0 0 630 185" role="img" aria-label="Chain, fork and collider structures" xmlns="http://www.w3.org/2000/svg"><text class="title" x="110" y="20" text-anchor="middle">chain  A → B → C</text><line class="ax" x1="61.0" y1="100.0" x2="92.0" y2="100.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M84.0,104.0 L92.0,100.0 L84.0,96.0"/><line class="ax" x1="126.0" y1="100.0" x2="157.0" y2="100.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M149.0,104.0 L157.0,100.0 L149.0,96.0"/><circle class="box" cx="45" cy="100" r="16"/><text class="title" x="45" y="104" text-anchor="middle">A</text><circle class="box-ink" cx="110" cy="100" r="16"/><text class="on-ink" x="110" y="104" text-anchor="middle">B</text><circle class="box" cx="175" cy="100" r="16"/><text class="title" x="175" y="104" text-anchor="middle">C</text><text class="t-mut" x="110" y="150" text-anchor="middle">observe B → blocked</text><text class="t-mut" x="110" y="170" text-anchor="middle">A, C dependent if B unseen</text><text class="title" x="315" y="20" text-anchor="middle">fork  A ← B → C</text><line class="ax" x1="301.7" y1="68.9" x2="270.0" y2="90.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M274.4,82.2 L270.0,90.0 L278.9,88.9"/><line class="ax" x1="328.3" y1="68.9" x2="360.0" y2="90.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M351.1,88.9 L360.0,90.0 L355.6,82.2"/><circle class="box" cx="255" cy="100" r="16"/><text class="title" x="255" y="104" text-anchor="middle">A</text><circle class="box-ink" cx="315" cy="60" r="16"/><text class="on-ink" x="315" y="64" text-anchor="middle">B</text><circle class="box" cx="375" cy="100" r="16"/><text class="title" x="375" y="104" text-anchor="middle">C</text><text class="t-mut" x="315" y="150" text-anchor="middle">observe B → blocked</text><text class="t-mut" x="315" y="170" text-anchor="middle">A, C dependent if B unseen</text><text class="title" x="520" y="20" text-anchor="middle">collider  A → B ← C</text><line class="ax" x1="473.3" y1="91.1" x2="505.0" y2="70.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M500.6,77.8 L505.0,70.0 L496.1,71.1"/><line class="ax" x1="566.7" y1="91.1" x2="535.0" y2="70.0" style="stroke-width:1.4"/><path class="ax" style="fill:none" d="M543.9,71.1 L535.0,70.0 L539.4,77.8"/><circle class="box" cx="460" cy="100" r="16"/><text class="title" x="460" y="104" text-anchor="middle">A</text><circle class="box-ink" cx="520" cy="60" r="16"/><text class="on-ink" x="520" y="64" text-anchor="middle">B</text><circle class="box" cx="580" cy="100" r="16"/><text class="title" x="580" y="104" text-anchor="middle">C</text><text class="t-warn" x="520" y="150" text-anchor="middle">observe B → OPENED</text><text class="t-mut" x="520" y="170" text-anchor="middle">A ⊥ C unconditionally</text></svg><figcaption>The three ways two variables A and C can connect through B. In a chain and a fork, A and C are dependent until B is observed, and observing B blocks the path. In a collider (common effect), A and C are independent until B (or any descendant of B) is observed; observing it opens the path ('explaining away').</figcaption></figure>
<!-- /fig:bn-structures -->

<div class="formula">

| Structure | Without observing B | Observing B |
|---|---|---|
| Chain A → B → C | A, C dependent | **A ⊥ C \| B** (blocked) |
| Fork A ← B → C (common cause) | A, C dependent | **A ⊥ C \| B** (blocked) |
| **Collider** A → B ← C (common effect) | **A ⊥ C** | A, C **dependent** given B or any descendant of B |

</div>

**Explaining away** (the collider case): an alarm (B) can be caused by a burglary (A) or an earthquake (C). These two are independent. But once you know the alarm rang, learning there was an earthquake makes a burglary **less** likely. Observing the common effect couples its causes.

### d-separation

Sets X and Y are **d-separated** by Z (so $X \perp Y \mid Z$) if **every** undirected path between them is **blocked**. A path is blocked if it contains:

- a chain or fork node that **is in Z**, or
- a collider that is **not** in Z and has **no descendant** in Z.

**Local Markov property:** each node is independent of its **non-descendants** given its **parents**.

**Markov blanket** of X: its **parents**, its **children**, and its **children's other parents**. Given its Markov blanket, X is independent of every other node in the network.

## 6.4 Computing probabilities

**A full assignment:** multiply one CPT entry per node.

$$
P(U = 1, V = 1, W = 1, Z = 1) = P(U{=}1)\,P(V{=}1 \mid U{=}1)\,P(W{=}1 \mid U{=}1)\,P(Z{=}1 \mid V{=}1, W{=}1).
$$

**A marginal or partial query:** sum the joint over the variables you don't care about. That can mean exponentially many terms, which is why we need **variable elimination** (topic 7).

**Naive Bayes is a Bayesian network:** the class $C$ is the only parent of every feature, $C \to X_1, \dots, C \to X_n$. So the features are conditionally independent given the class (ML topic 6).

---

## Summary: important points

<div class="formula">

1. $X \perp Y \mid Z$ ⟺ $P(x, y \mid z) = P(x \mid z)P(y \mid z)$. It's not the same as $X \perp Y$.
2. BN joint $= \prod_i P(X_i \mid \text{Parents}(X_i))$. Each factor's conditioning variables are that node's parents.
3. CPT size: $(k - 1) \times$ (number of parent combinations). The full joint over $n$ binary variables needs $2^n - 1$.
4. Chain and fork: observing the middle **blocks** the path. Collider: observing it, or a descendant, **opens** the path.
5. d-separation: X ⊥ Y | Z if every path between them is blocked.
6. Each node is independent of its non-descendants given its parents.
7. Markov blanket = parents + children + children's other parents.
8. For a full assignment, multiply one CPT entry per node. For marginals, sum out the rest.

</div>

<div class="trap">

- Two causes of a common effect are **independent** until the effect is observed. Conditioning on the effect makes them **dependent**.
- Observing a **descendant** of a collider also opens it.
- Look up each CPT entry using the parents' **actual** values in the assignment.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q24 (1 mark, MCQ)

$P(U, V, W, X, Y) = P(U)P(V)P(W \mid U, V)P(X \mid W)P(Y \mid W)$. Which statement is **false**?
(A) $Y \perp V \mid W$ (B) $X \perp U \mid W$ (C) $U \perp V \mid W$ (D) $Y \perp X \mid W$

<details>
<summary>Show solution</summary>

**Answer: (C)**

The graph is U → W ← V, W → X, W → Y.

- **(A), (B), (D):** every path goes through W as a chain or a fork, so observing W blocks it. True.
- **(C):** W is a **collider** on U → W ← V, and observing it **opens** the path, so U and V become dependent. False.

I verified this numerically: with random CPTs, (A), (B) and (D) hold exactly, while (C) fails. (U ⊥ V does hold when W isn't observed.)

</details>

### GATE DA 2024 Q64 (2 marks, NAT)

Binary U, V, W, Z with P(U=1) = 0.5, P(V=1 | U) = 0.5 for either U, P(W=1 | U=0) = 0, P(W=1 | U=1) = 1, and P(Z=1 | V, W) = 0.5, 0, 0, 0.5 for (V, W) = (0,0), (0,1), (1,0), (1,1). What is $P(U = 1, V = 1, W = 1, Z = 1)$? (3 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.125**

$P(U{=}1) \cdot P(V{=}1 \mid U{=}1) \cdot P(W{=}1 \mid U{=}1) \cdot P(Z{=}1 \mid V{=}1, W{=}1) = 0.5 \times 0.5 \times 1 \times 0.5 = 0.125$.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Binary network A → C ← B, C → D. How many independent parameters do its CPTs need?

<details>
<summary>Show solution</summary>

**Answer: 8**

A: 1. B: 1. C has 2 binary parents, so 4 combinations: 4. D has 1 parent: 2. Total: $1 + 1 + 4 + 2 = 8$, compared with $2^4 - 1 = 15$ for the full joint.

</details>

**F2 (2 marks, NAT).** In the network of 2024 Q64, what is $P(Z = 1)$? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.25**

W is a copy of U.

- U = 0 (so W = 0): $P(Z{=}1) = 0.5 \times 0.5 + 0.5 \times 0 = 0.25$, averaging over V.
- U = 1 (so W = 1): $0.5 \times 0 + 0.5 \times 0.5 = 0.25$.

So $P(Z{=}1) = 0.25$.

</details>

**F3 (2 marks, MSQ).** In the DAG A → B → C, A → D ← E, which statements are true?
(A) A ⊥ C | B (B) A ⊥ E (C) A ⊥ E | D (D) B ⊥ D | A

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

- (A): a chain blocked by B.
- (B): D is an unobserved collider.
- (C): observing D opens the collider, so this is false.
- (D): B ← A → D is a fork, blocked by A.

</details>

**F4 (1 mark, MCQ).** In A → C ← B, C → D, D ← E, what is the Markov blanket of C?
(A) {A, B} (B) {A, B, D} (C) {A, B, D, E} (D) {D, E}

<details>
<summary>Show solution</summary>

**Answer: (C)**

Parents {A, B}, child {D}, and the child's other parent {E}.

</details>

**F5 (2 marks, MCQ).** Burglary (B) and Earthquake (E) are independent causes of Alarm (A). Which statement is true?
(A) B ⊥ E | A (B) P(B | A, E) ≤ P(B | A) in the usual alarm model (C) B and E are dependent when A is unobserved (D) A ⊥ B

<details>
<summary>Show solution</summary>

**Answer: (B)**

Once the alarm has rung, also knowing there was an earthquake **explains away** the alarm and lowers the probability of a burglary. (A) and (C) have collider behaviour backwards.

</details>
