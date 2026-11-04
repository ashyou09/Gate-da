---
title: 5. First-order (predicate) logic
description: Objects, predicates, functions and quantifiers; translating English with ∀⇒ and ∃∧; quantifier order and negation; validity; universal and existential instantiation; unification; forward/backward chaining and resolution.
sidebar:
  label: 5. First-order logic
  order: 5
---

**Why it matters:** first-order logic appeared in 2024 and twice in 2026:
- 2024 Q54: translate "all balls are round except rugby balls";
- 2026 Q14: ∀ must pair with ⇒;
- 2026 Q48: which quantified sentences are not valid.

Nearly every FOL mark comes from **two translation rules** and **two negation rules**. Every validity claim on this page was checked by searching all interpretations over domains of size 1–3 for counterexamples.

## Topic map

<div class="mindmap">

- **First-order logic**
  - Vocabulary
    - constants, variables, predicates, functions
    - ∀ (for all), ∃ (there exists), scope
  - Translation
    - "All P are Q": $\forall x\,(P(x) \Rightarrow Q(x))$
    - "Some P is Q": $\exists x\,(P(x) \land Q(x))$
    - "No P is Q", "only", "except"
  - Quantifier rules
    - $\lnot\forall x\,P \equiv \exists x\,\lnot P$
    - order matters for mixed ∀∃
    - ∀ distributes over ∧, ∃ over ∨
  - Validity
    - true in every interpretation (non-empty domain)
  - Inference
    - universal / existential instantiation (Skolem constants)
    - unification and the most general unifier
    - generalized modus ponens, forward/backward chaining, resolution

</div>

## 5.1 Why go beyond propositional logic?

Propositional logic can't say "**every** student who studies passes" without listing every student. First-order logic adds:

| Element | Example | Denotes |
|---|---|---|
| Constant | `Ravi`, `2` | a specific object |
| Variable | $x, y$ | any object |
| Predicate | `Student(x)`, `Loves(x, y)` | a property or relation, either true or false |
| Function | `Mother(x)` | another object |
| Quantifiers | $\forall x$, $\exists x$ | for all / for some object |

An **interpretation** fixes a non-empty **domain** of objects and gives every symbol a meaning. A sentence is **valid** if it's true in **every** interpretation.

## 5.2 Translating English: the two golden rules

<div class="formula">

| English | Formula | Common wrong version |
|---|---|---|
| All P are Q | $\forall x\,(P(x) \Rightarrow Q(x))$ | $\forall x\,(P(x) \land Q(x))$: "everything is both P and Q" |
| Some P is Q | $\exists x\,(P(x) \land Q(x))$ | $\exists x\,(P(x) \Rightarrow Q(x))$: true as soon as **anything** is not P |
| No P is Q | $\forall x\,(P(x) \Rightarrow \lnot Q(x))$, or $\lnot\exists x\,(P(x) \land Q(x))$ | |
| Not all P are Q | $\exists x\,(P(x) \land \lnot Q(x))$ | |
| Only P are Q | $\forall x\,(Q(x) \Rightarrow P(x))$ | |
| All P are Q except R | $\forall x\,(P(x) \Rightarrow (Q(x) \Leftrightarrow \lnot R(x)))$ | |

**∀ goes with ⇒, ∃ goes with ∧.**

</div>

**"All balls are round except rugby balls"** (2024 Q54) means: a ball that isn't used in rugby is round, **and** a rugby ball isn't round. That's $\forall b\,(\lnot G(b) \Rightarrow R(b)) \land \forall b\,(G(b) \Rightarrow \lnot R(b))$. A **contrapositive** is equivalent to the original, so either half can be replaced by its contrapositive.

## 5.3 Negation and order of quantifiers

<div class="formula">

**Negation (De Morgan for quantifiers):**

$$
\lnot\forall x\,P(x) \equiv \exists x\,\lnot P(x) \qquad\qquad \lnot\exists x\,P(x) \equiv \forall x\,\lnot P(x)
$$

**Distribution:**

- $\forall x\,(P \land Q) \equiv \forall x\,P \land \forall x\,Q$
- $\exists x\,(P \lor Q) \equiv \exists x\,P \lor \exists x\,Q$
- Only **one direction** holds for the other pairs: $\forall x\,P \lor \forall x\,Q \Rightarrow \forall x\,(P \lor Q)$ and $\exists x\,(P \land Q) \Rightarrow \exists x\,P \land \exists x\,Q$.

**Order:** quantifiers of the **same** kind commute ($\forall x \forall y \equiv \forall y \forall x$). **Mixed** ones don't:

$$
\exists y\,\forall x\,L(x, y) \;\Rightarrow\; \forall x\,\exists y\,L(x, y) \quad\text{(valid)},
$$

but the converse is not valid.

</div>

<!-- fig:fol-quantifier-order -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 248" role="img" aria-label="Quantifier order in first-order logic" xmlns="http://www.w3.org/2000/svg"><text class="title" x="160" y="18" text-anchor="middle">∀x ∃y Loves(x, y)</text><text class="t-mut" x="70" y="40" text-anchor="middle">x</text><text class="t-mut" x="250" y="40" text-anchor="middle">y</text><line class="hl" x1="85" y1="60" x2="232" y2="115"/><path class="hl" style="fill:none" d="M224,110 L233,115 L224,120" transform="rotate(0 250 115)"/><line class="hl" x1="85" y1="115" x2="232" y2="170"/><path class="hl" style="fill:none" d="M224,165 L233,170 L224,175" transform="rotate(0 250 170)"/><line class="hl" x1="85" y1="170" x2="232" y2="60"/><path class="hl" style="fill:none" d="M224,55 L233,60 L224,65" transform="rotate(0 250 60)"/><circle class="box" cx="70" cy="60" r="14"/><text class="title" x="70" y="64" text-anchor="middle">a</text><circle class="box" cx="250" cy="60" r="14"/><text class="title" x="250" y="64" text-anchor="middle">a</text><circle class="box" cx="70" cy="115" r="14"/><text class="title" x="70" y="119" text-anchor="middle">b</text><circle class="box" cx="250" cy="115" r="14"/><text class="title" x="250" y="119" text-anchor="middle">b</text><circle class="box" cx="70" cy="170" r="14"/><text class="title" x="70" y="174" text-anchor="middle">c</text><circle class="box" cx="250" cy="170" r="14"/><text class="title" x="250" y="174" text-anchor="middle">c</text><text class="t-mut" x="160" y="235" text-anchor="middle">each x has its own y</text><text class="title" x="470" y="18" text-anchor="middle">∃y ∀x Loves(x, y)</text><text class="t-mut" x="380" y="40" text-anchor="middle">x</text><text class="t-mut" x="560" y="40" text-anchor="middle">y</text><line class="hl" x1="395" y1="60" x2="542" y2="115"/><path class="hl" style="fill:none" d="M534,110 L543,115 L534,120" transform="rotate(0 560 115)"/><line class="hl" x1="395" y1="115" x2="542" y2="115"/><path class="hl" style="fill:none" d="M534,110 L543,115 L534,120" transform="rotate(0 560 115)"/><line class="hl" x1="395" y1="170" x2="542" y2="115"/><path class="hl" style="fill:none" d="M534,110 L543,115 L534,120" transform="rotate(0 560 115)"/><circle class="box" cx="380" cy="60" r="14"/><text class="title" x="380" y="64" text-anchor="middle">a</text><circle class="box" cx="560" cy="60" r="14"/><text class="title" x="560" y="64" text-anchor="middle">a</text><circle class="box" cx="380" cy="115" r="14"/><text class="title" x="380" y="119" text-anchor="middle">b</text><circle class="box-ink" cx="560" cy="115" r="14"/><text class="on-ink" x="560" y="119" text-anchor="middle">b</text><circle class="box" cx="380" cy="170" r="14"/><text class="title" x="380" y="174" text-anchor="middle">c</text><circle class="box" cx="560" cy="170" r="14"/><text class="title" x="560" y="174" text-anchor="middle">c</text><text class="t-mut" x="470" y="235" text-anchor="middle">one y (b) works for every x</text></svg><figcaption>Quantifier order changes meaning. Left: ∀x ∃y Loves(x, y), meaning everyone loves someone, possibly a different person each. Right: ∃y ∀x Loves(x, y), meaning there is one person whom everyone loves. The right-hand situation implies the left, but not the other way round.</figcaption></figure>
<!-- /fig:fol-quantifier-order -->

## 5.4 Validity facts that GATE tests

With a **non-empty** domain (the standard assumption):

| Sentence | Valid? | Why |
|---|---|---|
| $\forall x\,P(x) \Rightarrow \exists x\,P(x)$ | **yes** | the domain has at least one element |
| $\exists x\,P(x) \Rightarrow \forall x\,P(x)$ | no | one P object doesn't make all objects P |
| $\exists x\,P(x) \Leftrightarrow \forall x\,P(x)$ | no | its ⇒ direction already fails |
| $\forall x\,P(x) \Rightarrow \exists x\,\lnot P(x)$ | no | false whenever everything is P |
| $\forall x\,P(x) \Rightarrow \lnot\exists x\,\lnot P(x)$ | **yes** | it's just quantifier negation |
| $\forall x\,\forall y\,(C(x, y) \Rightarrow C(y, x))$ | not valid in general | it states **symmetry**, a fact about C, which an arbitrary C needn't have |

## 5.5 Inference in FOL

- **Universal instantiation:** from $\forall x\,P(x)$, infer $P(c)$ for **any** ground term $c$.
- **Existential instantiation:** from $\exists x\,P(x)$, infer $P(k)$ for a **new** constant $k$ (a **Skolem constant**). Inside a ∀, use a Skolem **function**: $\forall x\,\exists y\,L(x, y)$ becomes $\forall x\,L(x, F(x))$.
- **Unification:** find a substitution that makes two expressions identical. The **most general unifier (MGU)** commits to as little as possible.
  - $\text{Knows}(\text{John}, x)$ and $\text{Knows}(y, \text{Mother}(y))$: MGU $= \{y/\text{John},\ x/\text{Mother}(\text{John})\}$.
  - $\text{Knows}(\text{John}, x)$ and $\text{Knows}(x, \text{Elizabeth})$: **fails**, since x can't be both. Renaming one variable apart fixes it.
  - **Occurs check:** $x$ can't unify with $F(x)$.
- **Generalized modus ponens:** from $p_1', \dots, p_n'$ and $(p_1 \land \dots \land p_n \Rightarrow q)$, infer $q\theta$, where $\theta$ unifies each $p_i'$ with $p_i$.
- **Forward chaining** (data-driven) and **backward chaining** (goal-driven, as in Prolog) work over definite clauses.
- **Resolution:** convert to CNF (eliminate ⇒, move ¬ inwards, standardise variables, Skolemize, drop ∀, distribute), then resolve using unification. It's refutation-complete.

---

## Summary: important points

<div class="formula">

1. "All P are Q" is $\forall x\,(P \Rightarrow Q)$. "Some P is Q" is $\exists x\,(P \land Q)$. ∀ goes with ⇒, ∃ with ∧.
2. $\lnot\forall x\,P \equiv \exists x\,\lnot P$ and $\lnot\exists x\,P \equiv \forall x\,\lnot P$.
3. "No P is Q": $\forall x\,(P \Rightarrow \lnot Q)$. "Not all P are Q": $\exists x\,(P \land \lnot Q)$.
4. Same quantifiers commute. $\exists\forall \Rightarrow \forall\exists$ is valid; the converse isn't.
5. $\forall x\,P \Rightarrow \exists x\,P$ is valid (non-empty domain). $\exists x\,P \Rightarrow \forall x\,P$ isn't.
6. ∀ distributes over ∧, ∃ over ∨.
7. Skolemize: ∃ inside ∀ becomes a function of the ∀ variables.
8. The MGU is the most general substitution that makes two atoms identical. The occurs check blocks $x = F(x)$.

</div>

<div class="trap">

- $\forall x\,(\text{King}(x) \land \text{Person}(x))$ says **everything** is a king. That's wrong for "each king is a person" (2026 Q14).
- $\exists x\,(P(x) \Rightarrow Q(x))$ is almost always true, so it's useless for "some P is Q".
- Swapping $\forall x\,\exists y$ to $\exists y\,\forall x$ changes the meaning.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q48 (2 marks, MSQ)

Which are **not** valid in first-order logic?
(A) $\forall x\,P(x) \Rightarrow \exists x\,P(x)$ (B) $\exists x\,P(x) \Rightarrow \forall x\,P(x)$ (C) $\exists x\,P(x) \Leftrightarrow \forall x\,P(x)$ (D) $\forall x\,P(x) \Rightarrow \exists x\,\lnot P(x)$

<details>
<summary>Show solution</summary>

**Answer: B; C; D**

See the table in §5.4. The only valid one is (A).

</details>

### GATE DA 2026 Q14 (1 mark, MCQ)

Which statement is NOT true?
(A) $\forall x\,\forall y\,\text{Classmate}(x, y) \Rightarrow \text{Classmate}(y, x)$ (B) $\forall x\,\text{Likes}(x, \text{Icecream}) \Rightarrow \lnot\exists x\,\lnot\text{Likes}(x, \text{Icecream})$ (C) "Each king is a person" is $\forall x\,\text{IsKing}(x) \land \text{IsPerson}(x)$ (D) "All humans are mortal" is $\forall x\,\text{IsHuman}(x) \Rightarrow \text{IsMortal}(x)$

<details>
<summary>Show solution</summary>

**Answer: (C)**

With ∧, (C) claims everything is a king and a person. The correct form is $\forall x\,(\text{IsKing}(x) \Rightarrow \text{IsPerson}(x))$.

- (B) is quantifier negation, so it's valid.
- (D) is correct.
- (A) correctly expresses that "classmate" is a symmetric relation.

</details>

### GATE DA 2024 Q54 (2 marks, MSQ)

$s_1: \forall b\,\lnot G(b) \Rightarrow R(b)$, $s_2: \forall b\,\lnot R(b) \Rightarrow G(b)$, $s_3: \forall b\,G(b) \Rightarrow \lnot R(b)$, $s_4: \forall b\,R(b) \Rightarrow \lnot G(b)$, where G = "used in rugby" and R = "round". Which represent "All balls are round except balls used in rugby"?
(A) $s_1 \land s_3$ (B) $s_1 \land s_2$ (C) $s_2 \land s_3$ (D) $s_3 \land s_4$

<details>
<summary>Show solution</summary>

**Answer: A; C**

The assertion needs both "non-rugby balls are round" ($s_1$) and "rugby balls are not round" ($s_3$).

- $s_2$ is the contrapositive of $s_1$, so $s_2 \land s_3 \equiv s_1 \land s_3$.
- $s_4$ is the contrapositive of $s_3$, so (D) is just $s_3$ said twice, and (B) is just $s_1$ said twice.

I checked all four combinations against the target truth table.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, MCQ).** Which formula says "Every student who studies passes"?
(A) $\forall x\,(S(x) \land T(x) \land P(x))$ (B) $\forall x\,((S(x) \land T(x)) \Rightarrow P(x))$ (C) $\exists x\,(S(x) \land T(x) \Rightarrow P(x))$ (D) $\forall x\,(S(x) \Rightarrow (T(x) \land P(x)))$

<details>
<summary>Show solution</summary>

**Answer: (B)**

(D) would say that every student studies.

</details>

**F2 (1 mark, MCQ).** Which formula is equivalent to $\lnot\forall x\,(P(x) \Rightarrow Q(x))$?
(A) $\forall x\,(P(x) \land \lnot Q(x))$ (B) $\exists x\,(P(x) \land \lnot Q(x))$ (C) $\exists x\,(\lnot P(x) \Rightarrow Q(x))$ (D) $\forall x\,(\lnot P(x) \lor Q(x))$

<details>
<summary>Show solution</summary>

**Answer: (B)**

$\lnot\forall x\,(\lnot P \lor Q) \equiv \exists x\,(P \land \lnot Q)$.

</details>

**F3 (2 marks, MSQ).** Which are valid?
(A) $\exists x\,\forall y\,L(x, y) \Rightarrow \forall y\,\exists x\,L(x, y)$ (B) $\forall y\,\exists x\,L(x, y) \Rightarrow \exists x\,\forall y\,L(x, y)$ (C) $\forall x\,P(x) \lor \forall x\,Q(x) \Rightarrow \forall x\,(P(x) \lor Q(x))$ (D) $\forall x\,(P(x) \lor Q(x)) \Rightarrow \forall x\,P(x) \lor \forall x\,Q(x)$

<details>
<summary>Show solution</summary>

**Answer: A; C**

Counterexample for (D): a domain {1, 2} with P true only of 1 and Q true only of 2. Every object is P or Q, but neither "all P" nor "all Q" holds. The model search confirms that (B) and (D) fail.

</details>

**F4 (2 marks, MCQ).** What is the MGU of $\text{Knows}(\text{John}, x)$ and $\text{Knows}(y, \text{Mother}(y))$?
(A) $\{x/\text{John}, y/\text{Mother}(y)\}$ (B) $\{y/\text{John}, x/\text{Mother}(\text{John})\}$ (C) $\{y/x\}$ (D) they don't unify

<details>
<summary>Show solution</summary>

**Answer: (B)**

Match the first arguments: y = John. Then the second argument becomes Mother(John), so x = Mother(John).

</details>

**F5 (1 mark, MCQ).** "No student is lazy." Which formula?
(A) $\forall x\,(S(x) \Rightarrow \lnot L(x))$ (B) $\forall x\,(S(x) \land \lnot L(x))$ (C) $\exists x\,(S(x) \land \lnot L(x))$ (D) $\lnot\forall x\,(S(x) \Rightarrow L(x))$

<details>
<summary>Show solution</summary>

**Answer: (A)**

It's equivalent to $\lnot\exists x\,(S(x) \land L(x))$. (D) means "not every student is lazy", which is much weaker.

</details>

**F6 (1 mark, MCQ).** What is the Skolemized form of $\forall x\,\exists y\,\text{Parent}(y, x)$?
(A) $\text{Parent}(c, x)$ (B) $\forall x\,\text{Parent}(F(x), x)$ (C) $\exists y\,\text{Parent}(y, c)$ (D) $\forall x\,\forall y\,\text{Parent}(y, x)$

<details>
<summary>Show solution</summary>

**Answer: (B)**

$y$ depends on $x$, so it becomes a function $F(x)$ rather than a single constant.

</details>
