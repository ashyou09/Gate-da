---
title: 4. Propositional logic
description: Syntax and truth tables, the implication and biconditional, standard equivalences, tautology/contradiction/satisfiability, entailment and its tests, translating English, inference rules, CNF and resolution.
sidebar:
  label: 4. Propositional logic
  order: 4
---

**Why it matters:** propositional logic is the **most-asked AI topic** (4 questions):
- 2024 Q29: which formulas are tautologies;
- 2025 Q15: $p \to q \equiv \lnot p \lor q$;
- 2026 Q24: what entailment means;
- 2026 Q38: formalise an English rule.

Each one yields to a **truth table** or **one equivalence**. Every answer here was also checked by brute-force truth tables.

## Topic map

<div class="mindmap">

- **Propositional logic**
  - Syntax
    - atoms, ¬, ∧, ∨, ⇒, ⇔
  - Semantics
    - truth tables; a model = one assignment
    - $p \Rightarrow q$ is false **only** when p is T and q is F
  - Status of a formula
    - valid (tautology), unsatisfiable (contradiction), satisfiable, contingent
  - Equivalences
    - $p \Rightarrow q \equiv \lnot p \lor q \equiv \lnot q \Rightarrow \lnot p$
    - De Morgan, distributive, absorption
  - Entailment
    - $\alpha \models \beta$ ⟺ $\alpha \Rightarrow \beta$ valid ⟺ $\alpha \land \lnot\beta$ unsatisfiable
  - Inference
    - modus ponens / tollens, resolution, CNF
    - Horn clauses, forward / backward chaining

</div>

## 4.1 Syntax and truth tables

Atoms ($p, q, \dots$) are true or false. Formulas are built with the connectives:

<div class="formula">

| $p$ | $q$ | $\lnot p$ | $p \land q$ | $p \lor q$ | $p \Rightarrow q$ | $p \Leftrightarrow q$ |
|---|---|---|---|---|---|---|
| T | T | F | T | T | **T** | T |
| T | F | F | F | T | **F** | F |
| F | T | T | F | T | **T** | F |
| F | F | T | F | F | **T** | T |

</div>

**The implication row to remember:** $p \Rightarrow q$ is false **only** when $p$ is true and $q$ is false. When $p$ is false, the implication is true no matter what $q$ is ("vacuously true"). This one fact settles most tautology questions.

Precedence, from tightest to loosest: $\lnot$, $\land$, $\lor$, $\Rightarrow$, $\Leftrightarrow$.

## 4.2 What a formula can be

| Term | Meaning |
|---|---|
| **Valid** (tautology) | true in **every** model: $p \lor \lnot p$ |
| **Unsatisfiable** (contradiction) | true in **no** model: $p \land \lnot p$ |
| **Satisfiable** | true in **at least one** model |
| **Contingent** | satisfiable but not valid |

$\alpha$ is valid ⟺ $\lnot\alpha$ is unsatisfiable.

**A fast tautology check for $A \Rightarrow B$:** try to make it false. That requires $A$ = T and $B$ = F at the same time. If that's impossible, the formula is a tautology. Usually you just set the variables so that $A$ is true and check $B$.

## 4.3 The equivalences to know cold

<div class="formula">

| Name | Equivalence |
|---|---|
| Implication elimination | $p \Rightarrow q \;\equiv\; \lnot p \lor q$ |
| **Contrapositive** | $p \Rightarrow q \;\equiv\; \lnot q \Rightarrow \lnot p$ |
| Biconditional | $p \Leftrightarrow q \;\equiv\; (p \Rightarrow q) \land (q \Rightarrow p)$ |
| De Morgan | $\lnot(p \land q) \equiv \lnot p \lor \lnot q$, $\lnot(p \lor q) \equiv \lnot p \land \lnot q$ |
| Double negation | $\lnot\lnot p \equiv p$ |
| Distributivity | $p \land (q \lor r) \equiv (p \land q) \lor (p \land r)$ and dually |
| Absorption | $p \lor (p \land q) \equiv p$, $p \land (p \lor q) \equiv p$ |
| Exportation | $(p \land q) \Rightarrow r \;\equiv\; p \Rightarrow (q \Rightarrow r)$ |
| Splitting a conclusion | $p \Rightarrow (q \land r) \;\equiv\; (p \Rightarrow q) \land (p \Rightarrow r)$ |
| Splitting a premise "or" | $(p \lor q) \Rightarrow r \;\equiv\; (p \Rightarrow r) \land (q \Rightarrow r)$ |

**Not** equivalent:

- the **converse** $q \Rightarrow p$ or the **inverse** $\lnot p \Rightarrow \lnot q$, compared with $p \Rightarrow q$;
- $(p \land q) \Rightarrow r$ compared with $(p \Rightarrow r) \land (q \Rightarrow r)$.

</div>

## 4.4 Translating English

| English | Formula |
|---|---|
| if p then q / p implies q / q **if** p | $p \Rightarrow q$ |
| p **only if** q / q is **necessary** for p | $p \Rightarrow q$ |
| p is **sufficient** for q | $p \Rightarrow q$ |
| p **if and only if** q | $p \Leftrightarrow q$ |
| p **unless** q | $\lnot q \Rightarrow p$, equivalently $p \lor q$ |
| neither p nor q | $\lnot p \land \lnot q$ |

**Conditions that apply "within a group":** "A creative person succeeds **if and only if** disciplined" applies only to creative people, so it's $C \Rightarrow (S \Leftrightarrow D)$. It says nothing about people who aren't creative. 2026 Q38 tests exactly this.

## 4.5 Entailment

$\alpha \models \beta$ ($\alpha$ **entails** $\beta$) means: in **every** model where $\alpha$ is true, $\beta$ is true too.

<div class="formula">

$$
\alpha \models \beta \iff (\alpha \Rightarrow \beta) \text{ is valid} \iff (\alpha \land \lnot\beta) \text{ is unsatisfiable}.
$$

The second equivalence is the basis of **proof by refutation**: assume the negation of the goal, and derive a contradiction.

</div>

Entailment doesn't go backwards. $\alpha \models \beta$ doesn't give $\beta \models \alpha$.

## 4.6 Inference

| Rule | From | Conclude |
|---|---|---|
| Modus ponens | $p \Rightarrow q$, $p$ | $q$ |
| Modus tollens | $p \Rightarrow q$, $\lnot q$ | $\lnot p$ |
| And-elimination | $p \land q$ | $p$ |
| **Resolution** | $a \lor p$, $\lnot p \lor b$ | $a \lor b$ |

An inference procedure is **sound** if it derives only entailed sentences, and **complete** if it can derive every entailed sentence. Resolution is sound, and it's **refutation-complete**.

### CNF and resolution

**Conjunctive normal form** is an AND of clauses, each an OR of literals. To convert:

1. Eliminate ⇔, then ⇒ (using $\lnot p \lor q$).
2. Push ¬ inwards with De Morgan, and remove ¬¬.
3. Distribute ∨ over ∧.

**Resolution refutation:** convert KB ∧ ¬goal to clauses and keep resolving pairs. If you reach the **empty clause**, the goal is entailed.

<!-- fig:resolution-tree -->
<figure class="diagram"><svg class="dg" viewBox="0 0 720 250" role="img" aria-label="Resolution refutation tree" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="80" y1="44" x2="155" y2="81"/><line class="ax" x1="230" y1="44" x2="155" y2="81"/><line class="ax" x1="155" y1="109" x2="240" y2="146"/><line class="ax" x1="330" y1="109" x2="240" y2="146"/><line class="ax" x1="240" y1="174" x2="335" y2="211"/><line class="ax" x1="430" y1="174" x2="335" y2="211"/><rect class="box" x="56.0" y="16" width="48" height="28" rx="14" style="stroke:var(--gd-trap);stroke-width:1.6"/><text class="t-warn" x="80" y="35" text-anchor="middle">¬R</text><rect class="box" x="186.0" y="16" width="88" height="28" rx="14" style=""/><text class="title" x="230" y="35" text-anchor="middle">¬Q ∨ R</text><rect class="box" x="131.0" y="81" width="48" height="28" rx="14" style=""/><text class="title" x="155" y="100" text-anchor="middle">¬Q</text><rect class="box" x="286.0" y="81" width="88" height="28" rx="14" style=""/><text class="title" x="330" y="100" text-anchor="middle">¬P ∨ Q</text><rect class="box" x="216.0" y="146" width="48" height="28" rx="14" style=""/><text class="title" x="240" y="165" text-anchor="middle">¬P</text><rect class="box" x="411.0" y="146" width="38" height="28" rx="14" style=""/><text class="title" x="430" y="165" text-anchor="middle">P</text><rect class="box-ink" x="276.0" y="211" width="118" height="28" rx="14" style=""/><text class="on-ink" x="335" y="230" text-anchor="middle">□ (empty)</text><text class="t-warn" x="80" y="62" text-anchor="middle">negated goal</text><text class="t-mut" x="490" y="40">1. clauses: ¬P ∨ Q, ¬Q ∨ R, P</text><text class="t-mut" x="490" y="64">2. add ¬R (negated goal)</text><text class="t-mut" x="490" y="88">3. resolve on R → ¬Q</text><text class="t-mut" x="490" y="112">4. resolve on Q → ¬P</text><text class="t-mut" x="490" y="136">5. resolve on P → □</text><text class="t-ink" x="490" y="160">contradiction ⇒ KB ⊨ R</text></svg><figcaption>Proof by resolution refutation that KB = {P ⇒ Q, Q ⇒ R, P} entails R. Convert the KB to clauses (¬P ∨ Q, ¬Q ∨ R, P), add the negated goal ¬R, and resolve pairs that contain a literal and its negation. Reaching the empty clause □ means KB ∧ ¬R is unsatisfiable, so KB ⊨ R.</figcaption></figure>
<!-- /fig:resolution-tree -->

**Horn clauses** have at most one positive literal (for example $p \land q \Rightarrow r$). With Horn clauses, **forward chaining** (data-driven, firing rules whose premises are known) and **backward chaining** (goal-driven, working back from the query) both run in linear time.

---

## Summary: important points

<div class="formula">

1. $p \Rightarrow q$ is false only for T ⇒ F. When the premise is false, the implication is true.
2. $p \Rightarrow q \equiv \lnot p \lor q \equiv \lnot q \Rightarrow \lnot p$ (the contrapositive). The converse isn't equivalent.
3. To test a tautology, try to make the antecedent T and the consequent F. If you can't, it's a tautology.
4. Valid = true in every model. Unsatisfiable = true in none. Satisfiable = true in some.
5. $\alpha \models \beta$ ⟺ $\alpha \Rightarrow \beta$ is valid ⟺ $\alpha \land \lnot\beta$ is unsatisfiable.
6. "p only if q" is $p \Rightarrow q$. "p unless q" is $p \lor q$.
7. Resolution: from $a \lor p$ and $\lnot p \lor b$, derive $a \lor b$. The empty clause means a contradiction, so the goal is proved.
8. CNF: eliminate ⇔ and ⇒, push ¬ inwards, distribute ∨ over ∧.

</div>

<div class="trap">

- "Only if" points the arrow **towards** the condition: p only if q is $p \Rightarrow q$, not $q \Rightarrow p$.
- $(p \land q) \Rightarrow r$ is weaker than $(p \Rightarrow r) \land (q \Rightarrow r)$.
- Entailment is one-directional.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q29 (1 mark, MSQ)

Which are tautologies?
(A) $(\lnot x \land y) \Rightarrow (y \Rightarrow x)$ (B) $(x \land \lnot y) \Rightarrow (\lnot x \Rightarrow y)$ (C) $(\lnot x \land y) \Rightarrow (\lnot x \Rightarrow y)$ (D) $(x \land \lnot y) \Rightarrow (y \Rightarrow x)$

<details>
<summary>Show solution</summary>

**Answer: B; C; D**

Make each antecedent true and look at the consequent.

- **(A)** The antecedent needs x = F, y = T. Then $y \Rightarrow x$ is T ⇒ F = **F**. Not a tautology.
- **(B)** x = T, y = F. Then $\lnot x \Rightarrow y$ is F ⇒ F = T. ✓
- **(C)** x = F, y = T. Then $\lnot x \Rightarrow y$ is T ⇒ T = T. ✓
- **(D)** x = T, y = F. Then $y \Rightarrow x$ is F ⇒ T = T. ✓

</details>

### GATE DA 2025 Q15 (1 mark, MCQ)

$S_1: p \to q$, $S_2: \lnot p \land q$, $S_3: \lnot p \lor q$, $S_4: \lnot p \lor \lnot q$. Which is correct?
(A) $S_1 \equiv S_3$ (B) $S_2 \equiv S_3$ (C) $S_2 \equiv S_4$ (D) $S_1 \equiv S_4$

<details>
<summary>Show solution</summary>

**Answer: (A)**

This is implication elimination. I confirmed the other three are not equivalent with truth tables.

</details>

### GATE DA 2026 Q24 (1 mark, MSQ)

X entails Y. Which are correct?
(A) $X \Rightarrow Y$ (B) $X \land \lnot Y$ is FALSE (C) if X then Y (D) if Y then X

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

From §4.5: entailment means $X \Rightarrow Y$ is valid ("if X then Y"), and equivalently $X \land \lnot Y$ is unsatisfiable. (D) is the converse.

</details>

### GATE DA 2026 Q38 (2 marks, MCQ)

"A creative person (C) will succeed (S) if the person is also disciplined (D), but will not succeed otherwise." Which formalisations are correct?
(i) $C \land S \Leftrightarrow D$ (ii) $C \Rightarrow (S \Leftrightarrow D)$ (iii) $C \Leftrightarrow ((D \Rightarrow S) \lor \lnot S)$

<details>
<summary>Show solution</summary>

**Answer: (B)** only (ii)

- The sentence says: **for creative people**, success happens exactly when they're disciplined. That's (ii).
- (i) says something about non-creative people too. If C = F and D = T, the left side is F and D is T, so (i) is false, while the original sentence makes no claim. Not equivalent.
- (iii): $(D \Rightarrow S) \lor \lnot S = \lnot D \lor S \lor \lnot S$, which is always T. So (iii) reduces to $C \Leftrightarrow \text{T}$, i.e. just $C$. Wrong.

All three checked by truth table.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, MSQ).** Which are equivalent to $p \Rightarrow q$?
(A) $\lnot q \Rightarrow \lnot p$ (B) $q \Rightarrow p$ (C) $\lnot p \lor q$ (D) $\lnot(p \land \lnot q)$

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(D) is De Morgan applied to (C). (B) is the converse.

</details>

**F2 (1 mark, MCQ).** Which is a tautology?
(A) $(p \Rightarrow q) \Rightarrow p$ (B) $((p \Rightarrow q) \Rightarrow p) \Rightarrow p$ (C) $p \Rightarrow (p \land q)$ (D) $(p \lor q) \Rightarrow p$

<details>
<summary>Show solution</summary>

**Answer: (B)** (Peirce's law)

(A) fails for p = F, since $(F \Rightarrow q) = T$ and $T \Rightarrow F = F$. (C) fails for p = T, q = F. (D) fails for p = F, q = T.

</details>

**F3 (1 mark, NAT).** In how many of the 8 models over $p, q, r$ is $(p \lor q) \land (\lnot p \lor r)$ true?

<details>
<summary>Show solution</summary>

**Answer: 4**

- p = T needs r = T (q is free): 2 models.
- p = F needs q = T (r is free): 2 models.

</details>

**F4 (2 marks, MSQ).** Which equivalences hold?
(A) $(p \land q) \Rightarrow r \equiv p \Rightarrow (q \Rightarrow r)$ (B) $p \Rightarrow (q \land r) \equiv (p \Rightarrow q) \land (p \Rightarrow r)$ (C) $(p \lor q) \Rightarrow r \equiv (p \Rightarrow r) \land (q \Rightarrow r)$ (D) $(p \land q) \Rightarrow r \equiv (p \Rightarrow r) \land (q \Rightarrow r)$

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(D) fails for p = T, q = F, r = F: the left side is T and the right side is F.

</details>

**F5 (1 mark, MCQ).** "You can enter only if you have a ticket" (E = enter, T = ticket). What is the formula?
(A) $T \Rightarrow E$ (B) $E \Rightarrow T$ (C) $E \Leftrightarrow T$ (D) $E \lor T$

<details>
<summary>Show solution</summary>

**Answer: (B)**

Having a ticket is **necessary** for entering.

</details>

**F6 (2 marks, MCQ).** With KB = {¬P ∨ Q, ¬Q ∨ R, P}, what is the minimum number of resolution steps needed to derive the empty clause after adding ¬R?
(A) 1 (B) 2 (C) 3 (D) 4

<details>
<summary>Show solution</summary>

**Answer: (C)**

¬R with ¬Q ∨ R gives ¬Q. ¬Q with ¬P ∨ Q gives ¬P. ¬P with P gives □. That's 3 steps (the figure in §4.6).

</details>
