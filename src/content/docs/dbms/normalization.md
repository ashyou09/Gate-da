---
title: 4. Functional dependencies & normalization
description: Anomalies, functional dependencies, Armstrong's axioms, attribute closure, finding candidate keys, 1NF/2NF/3NF/BCNF, highest normal form, lossless-join and dependency-preserving decomposition.
sidebar:
  label: 4. FDs & normalization
  order: 4
---

**Why it matters:** normalization appeared **every year**:
- 2024 Q46: which FDs can be derived;
- 2025 Q16: a non-dependency-preserving decomposition forces joins;
- 2025 Q57: candidate keys and BCNF;
- 2026 Q17: candidate keys.

The single tool behind all four is **attribute closure**. Every answer on this page was also checked with a small closure program.

## Topic map

<div class="mindmap">

- **Normalization**
  - Why
    - redundancy → insert / delete / update anomalies
  - Functional dependencies
    - $X \to Y$: equal X values force equal Y values
    - Armstrong: reflexivity, augmentation, transitivity
    - derived: union, decomposition, pseudo-transitivity
  - Attribute closure $X^+$
    - test $X \to Y$: is $Y \subseteq X^+$?
    - superkey test: $X^+ = R$
  - Candidate keys
    - attributes never on a RHS are in **every** key
  - Normal forms
    - 1NF ⊃ 2NF ⊃ 3NF ⊃ BCNF
    - prime attribute = part of some candidate key
  - Decomposition
    - lossless: $(R_1 \cap R_2) \to R_1$ or $\to R_2$
    - dependency preserving
    - BCNF: lossless, maybe not preserving; 3NF: both possible

</div>

## 4.1 Why normalize? Anomalies

Store student, course and instructor in one table, where each course has one instructor:

| student | course | instructor |
|---|---|---|
| Asha | DBMS | Rao |
| Ravi | DBMS | Rao |
| Asha | ML | Iyer |

"DBMS is taught by Rao" is stored **twice**. That redundancy causes three problems:

- **Update anomaly:** change DBMS's instructor in one row and forget the other, and the data contradicts itself.
- **Insert anomaly:** you can't record a new course's instructor until some student enrols.
- **Delete anomaly:** if the last ML student drops out, you also lose the fact that Iyer teaches ML.

The cause is the dependency course → instructor, where course isn't a key. **Normalization** splits the table so that every fact is stored once.

## 4.2 Functional dependencies

$X \to Y$ ("X determines Y") means: any two tuples that agree on X must agree on Y. It's **trivial** if $Y \subseteq X$.

<div class="formula">

**Armstrong's axioms** (sound and complete: they derive exactly the implied FDs):

| Rule | Statement |
|---|---|
| Reflexivity | $Y \subseteq X \Rightarrow X \to Y$ |
| Augmentation | $X \to Y \Rightarrow XZ \to YZ$ |
| Transitivity | $X \to Y,\ Y \to Z \Rightarrow X \to Z$ |
| *Union* (derived) | $X \to Y,\ X \to Z \Rightarrow X \to YZ$ |
| *Decomposition* (derived) | $X \to YZ \Rightarrow X \to Y$ and $X \to Z$ |
| *Pseudo-transitivity* (derived) | $X \to Y,\ WY \to Z \Rightarrow WX \to Z$ |

**Not valid:** $XY \to Z$ does **not** give $X \to Z$. You can't split the left-hand side.

</div>

## 4.3 Attribute closure: the key algorithm

$X^+$ is the set of all attributes determined by $X$.

1. Start with $X^+ = X$.
2. Repeat: for each FD $L \to R$, if $L \subseteq X^+$, add $R$ to $X^+$.
3. Stop when nothing changes.

<div class="formula">

- **$X \to Y$ follows from F** $\iff$ $Y \subseteq X^+$.
- **$X$ is a superkey** $\iff$ $X^+ = $ all attributes.
- **$X$ is a candidate key** $\iff$ $X$ is a superkey **and** no proper subset is.

</div>

**Example.** $R(A, B, C, D, E)$ with $A \to B$, $B \to C$, $CD \to E$.

- $A^+$: start with $\{A\}$; $A \to B$ adds B; $B \to C$ adds C. $CD \to E$ needs D, which we don't have. So $A^+ = \{A, B, C\}$. Not a key.
- $AD^+ = \{A, D, B, C, E\}$, everything. **AD is a key**, and it's the only one.

## 4.4 Finding all candidate keys quickly

1. Put each attribute in a class:
   - **only on left-hand sides** (or in no FD at all): it must be in **every** key;
   - **only on right-hand sides**: it's in **no** key;
   - **on both sides**: it might be.
2. Take the "must" attributes as the core and compute the core's closure. If it covers all of R, that's the **only** key.
3. Otherwise, add "might" attributes one at a time, then in pairs, and so on. Keep only **minimal** sets.

For 2026 Q17 with $A \to BC$, $CD \to E$, $E \to A$: **D** is never on a right-hand side, so every key contains D. $D^+ = \{D\}$, not enough. Try adding one attribute: $AD^+$, $CD^+$ and $ED^+$ all give R; $BD^+ = \{B, D\}$ doesn't. So the keys are **AD, CD, ED**.

## 4.5 Normal forms

A **prime** attribute is one that belongs to **some** candidate key.

<!-- fig:nf-ladder -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 270" role="img" aria-label="Nested normal forms" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="10" y="10.0" width="600" height="250.0" rx="10" style=""/><text class="t-ink" x="24" y="32.0" style="font-weight:700">1NF</text><text class="t-mut" x="80" y="32.0">every attribute value is atomic (no lists or repeating groups)</text><rect class="box" x="42" y="37.2" width="536" height="195.6" rx="10" style=""/><text class="t-ink" x="56" y="59.2" style="font-weight:700">2NF</text><text class="t-mut" x="112" y="59.2">no non-prime A depends on a proper part of a candidate key</text><rect class="box" x="74" y="64.4" width="472" height="141.2" rx="10" style=""/><text class="t-ink" x="88" y="86.4" style="font-weight:700">3NF</text><text class="t-mut" x="144" y="86.4">X is a superkey, or A is prime (part of some candidate key)</text><rect class="box-ink" x="106" y="91.6" width="408" height="86.8" rx="10" style="opacity:.9"/><text class="on-ink" x="120" y="113.6" style="font-weight:700">BCNF</text><text class="on-ink" x="176" y="113.6">X is a superkey, for every non-trivial X → A</text></svg><figcaption>Each normal form is stricter than the one outside it: every BCNF relation is in 3NF, every 3NF relation is in 2NF, and so on. For each non-trivial FD X → A, the rule at each level says what is allowed.</figcaption></figure>
<!-- /fig:nf-ladder -->

<div class="formula">

For every non-trivial FD $X \to A$ that holds:

| Normal form | Condition |
|---|---|
| **1NF** | all values are atomic |
| **2NF** | 1NF, and no non-prime $A$ depends on a **proper subset** of a candidate key (no partial dependency) |
| **3NF** | $X$ is a superkey **or** $A$ is prime |
| **BCNF** | $X$ is a superkey |

</div>

**Finding the highest normal form:**

1. Find **all** candidate keys and the set of prime attributes.
2. For each FD $X \to A$ (split right-hand sides into single attributes):
   - Is $X$ a superkey? Then it's fine for every normal form.
   - If not, and $A$ is prime: BCNF is violated, 3NF is fine.
   - If not, and $A$ is non-prime: 3NF is violated. If $X$ is also a **proper part of a key**, 2NF is violated too.
3. The highest normal form is the strictest one with no violations.

Quick checks:

- A relation with **only two attributes** is always in BCNF.
- If **every attribute is prime**, the relation is at least in 3NF.
- If every candidate key is a **single attribute**, 2NF holds automatically: there's no "part of a key".

## 4.6 Decomposition: what makes a split good

Split $R$ into $R_1, R_2$. Two properties matter:

<div class="formula">

**Lossless join** (essential): joining $R_1 \bowtie R_2$ gives back exactly $R$, with no spurious tuples. Test for a binary split:

$$
(R_1 \cap R_2) \to R_1 \quad\text{or}\quad (R_1 \cap R_2) \to R_2,
$$

i.e. the common attributes form a superkey of one side.

**Dependency preserving** (desirable): every FD of $F$ can be checked within a single $R_i$. Formally, $(F_1 \cup F_2)^+ = F^+$, where $F_i$ is the projection of $F^+$ onto $R_i$.

</div>

| Target | Lossless? | Dependency preserving? |
|---|---|---|
| **BCNF** decomposition | always achievable | **not always** |
| **3NF** synthesis | always | **always** |

**Why lost dependencies cost joins (2025 Q16):** if an FD's attributes now sit in different tables, the only way to check it on each update is to **join** those tables back together first.

Classic example: $R(A, B, C)$ with $AB \to C$ and $C \to B$. The keys are AB and AC, so every attribute is prime and $R$ is in **3NF**. But $C \to B$ violates **BCNF**. The BCNF split into $(A, C)$ and $(C, B)$ is lossless, since $C \to CB$, but it **loses** $AB \to C$.

---

## Summary: important points

<div class="formula">

1. Redundancy causes update, insert and delete anomalies.
2. Armstrong's axioms: reflexivity, augmentation, transitivity. Union and decomposition apply to the right-hand side only.
3. $X \to Y$ holds iff $Y \subseteq X^+$. $X$ is a superkey iff $X^+ = R$.
4. Attributes never on a right-hand side belong to every candidate key.
5. 2NF: no partial dependency of a non-prime attribute. 3NF: $X$ superkey **or** $A$ prime. BCNF: $X$ superkey.
6. BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF. A two-attribute relation is always in BCNF.
7. Lossless split: the common attributes determine one side.
8. 3NF synthesis is always lossless and dependency preserving. BCNF may lose dependencies, and checking a lost FD needs a join.

</div>

<div class="trap">

- Find **all** candidate keys before you judge primeness. Missing one key can make an attribute look non-prime.
- $XY \to Z$ doesn't give $X \to Z$.
- 3NF allows $X \to A$ with $X$ not a superkey **only if** $A$ is prime.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q46 (2 marks, MSQ)

$R(U, V, W, X, Y, Z)$ with $U \to V$, $U \to W$, $WX \to Y$, $WX \to Z$, $V \to X$. Which FDs can be derived?
(A) $VW \to YZ$ (B) $WX \to YZ$ (C) $VW \to U$ (D) $VW \to Y$

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

$VW^+$: start with $\{V, W\}$. $V \to X$ adds X, then $WX \to Y$ and $WX \to Z$ add Y and Z. So $VW^+ = \{V, W, X, Y, Z\}$, with **no U**.

- (A) and (D) hold.
- (C) fails, because U isn't in $VW^+$.
- (B) is the union rule applied to $WX \to Y$ and $WX \to Z$.

</details>

### GATE DA 2025 Q57 (2 marks, MSQ)

$R(A, B, C, D, E, F, G)$ with $A \to BCEF$, $E \to DG$, $BC \to A$. Which are correct?
(A) A is the only candidate key (B) A and BC are the candidate keys (C) A, BC and E are the candidate keys (D) R is not in BCNF

<details>
<summary>Show solution</summary>

**Answer: B; D**

- $A^+$: A gives BCEF, then E gives DG, so everything. A is a key.
- $BC^+$: BC gives A, then everything. BC is a key. $B^+$ and $C^+$ alone are just themselves, so BC is minimal.
- $E^+ = \{E, D, G\}$, so E is not a key.

$E \to DG$ has a left side that isn't a superkey, so R is **not in BCNF**. (D and G aren't prime, so R isn't in 3NF either. It is in 2NF, because E isn't part of any key.)

</details>

### GATE DA 2026 Q17 (1 mark, MCQ)

$R(A, B, C, D, E)$ with $F = \{A \to BC,\ CD \to E,\ E \to A\}$. What are the candidate keys?
(A) AD, ED and CD only (B) AD and ED only (C) A, E and CD only (D) A and CD only

<details>
<summary>Show solution</summary>

**Answer: (A)**

See §4.4. D never appears on a right-hand side, so every key contains D. $AD^+$, $CD^+$ and $ED^+$ each equal R, while $D^+$ and $BD^+$ don't.

</details>

### GATE DA 2025 Q16 (1 mark, MCQ)

If a decomposition is **not** dependency-preserving, which operator has to be executed more often to maintain the dependencies?
(A) Selection (B) Projection (C) Join (D) Set union

<details>
<summary>Show solution</summary>

**Answer: (C)**

A lost FD involves attributes from more than one relation. Checking it requires joining those relations back together.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, MCQ).** In $R(A, B, C, D, E)$ with $A \to B$, $B \to C$, $CD \to E$, what is $A^+$?
(A) {A, B} (B) {A, B, C} (C) {A, B, C, E} (D) {A, B, C, D, E}

<details>
<summary>Show solution</summary>

**Answer: (B)**

$CD \to E$ can't fire, because D isn't available.

</details>

**F2 (2 marks, MCQ).** $R(A, B, C, D)$ with $AB \to C$ and $C \to D$. What is the highest normal form?
(A) 1NF (B) 2NF (C) 3NF (D) BCNF

<details>
<summary>Show solution</summary>

**Answer: (B)**

The only key is AB. $C \to D$ is a **transitive** dependency: C isn't a superkey and D isn't prime, so 3NF fails. There's no partial dependency, because neither A nor B alone determines anything, so 2NF holds.

</details>

**F3 (2 marks, MCQ).** $R(A, B, C)$ with $AB \to C$ and $C \to B$. What is the highest normal form?
(A) 1NF (B) 2NF (C) 3NF (D) BCNF

<details>
<summary>Show solution</summary>

**Answer: (C)**

The keys are AB and AC, so every attribute is prime and 3NF holds. $C \to B$ has a left side that isn't a superkey, so BCNF fails.

</details>

**F4 (2 marks, MCQ).** $R(A, B, C, D)$ with $AB \to C$ and $B \to D$. Which FD violates 2NF?
(A) $AB \to C$ (B) $B \to D$ (C) both (D) neither

<details>
<summary>Show solution</summary>

**Answer: (B)**

The key is AB. D is non-prime and depends only on B, which is part of the key. That's a partial dependency.

</details>

**F5 (2 marks, MSQ).** $R(A, B, C, D, E)$ with $A \to B$, $B \to C$, $CD \to E$. Which decompositions are lossless?
(A) $(A, B)$ and $(A, C, D, E)$ (B) $(A, B, C)$ and $(C, D, E)$ (C) $(A, B, C)$ and $(A, D, E)$ (D) none of these

<details>
<summary>Show solution</summary>

**Answer: A; C**

- (A): the common attribute is A, and $A^+ \supseteq \{A, B\}$, so A determines the first side. ✓
- (B): the common attribute is C, and $C^+ = \{C\}$ determines neither side. ✗
- (C): the common attribute is A, and $A^+ = \{A, B, C\}$, which covers the first side. ✓

</details>

**F6 (1 mark, NAT).** How many candidate keys does $R(A, B, C, D)$ have, with $A \to B$, $B \to C$, $C \to D$, $D \to A$?

<details>
<summary>Show solution</summary>

**Answer: 4**

The FDs form a cycle, so each single attribute determines all the others. A, B, C and D are each a candidate key.

</details>
