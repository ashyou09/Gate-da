---
title: 2. Relational algebra & tuple calculus
description: Selection, projection, rename, set operations, Cartesian product, theta/equi/natural/outer joins, division, cardinality bounds, reading expressions, and tuple relational calculus.
sidebar:
  label: 2. Relational algebra & TRC
  order: 2
---

**Why it matters:** this is the **most-asked DBMS topic** (5 PYQs):
- 2024 Q26: express "every … appears in …" with set difference;
- 2025 Q17: read an expression;
- 2025 Q62: division on real tables;
- 2026 Q42: joins and selections on real tables;
- 2026 Q59: evaluate a tuple-calculus formula.

The skill is evaluating operators **exactly** on small tables.

## Topic map

<div class="mindmap">

- **Relational algebra**
  - Unary
    - σ (select rows), π (project columns, removes duplicates), ρ (rename)
  - Set operations (union-compatible)
    - ∪, ∩, −
  - Combining
    - × (Cartesian product)
    - θ-join, equi-join, natural join ⋈
    - outer joins (left, right, full) pad with NULL
  - Division ÷
    - "for all": $x$ related to **every** $y$
  - Cardinality bounds
  - Tuple relational calculus
    - $\{t \mid P(t)\}$ with ∃ and ∀
    - safe expressions; same power as RA

</div>

## 2.1 The basic operators

Relational algebra takes relations in and gives relations out. A relation is a **set**, so results have **no duplicate rows**.

<div class="formula">

| Operator | Notation | Result |
|---|---|---|
| Selection | $\sigma_{\text{cond}}(R)$ | the rows of $R$ that satisfy the condition. Same columns |
| Projection | $\pi_{A, B}(R)$ | only columns A and B, **with duplicate rows removed** |
| Rename | $\rho_{S(A', B')}(R)$ | the same data under new names |
| Union | $R \cup S$ | rows in either. $R$ and $S$ must be **union-compatible** (same arity, compatible domains) |
| Intersection | $R \cap S$ | rows in both. Also $R \cap S = R - (R - S)$ |
| Difference | $R - S$ | rows in $R$ but not in $S$ |
| Cartesian product | $R \times S$ | every row of $R$ paired with every row of $S$ |

</div>

The **basic** (complete) set is $\{\sigma, \pi, \cup, -, \times, \rho\}$. Intersection, joins and division can all be written using these.

## 2.2 Joins

<div class="formula">

| Join | Definition | Notes |
|---|---|---|
| θ-join | $R \bowtie_\theta S = \sigma_\theta(R \times S)$ | any condition |
| Equi-join | θ-join whose condition uses only $=$ | both copies of the join columns are kept |
| **Natural join** | $R \bowtie S$: equate **all same-named** attributes, keep **one** copy of each | no common attributes means it becomes $R \times S$ |
| Left outer join | $R ⟕ S$ | all rows of $R$; unmatched ones padded with NULL on $S$'s side |
| Right / full outer | $R ⟖ S$, $R ⟗ S$ | keep unmatched rows of $S$ / of both |

</div>

**Watch out:**

- A natural join matches on **every** shared column name. In 2026 Q42, $X \bowtie Y$ joins on **both** P and Q.
- **NULL never equals anything**, not even another NULL, so a row with NULL in a join column never matches in an inner or natural join.

## 2.3 Division: the "for all" operator

$R(X, Y) \div S(Y)$ returns the $X$ values that appear in $R$ paired with **every** $Y$ in $S$.

Typical question: "students who took **all** required courses" is $\text{Takes}(\text{student}, \text{course}) \div \text{Required}(\text{course})$.

<!-- fig:ra-division -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 232" role="img" aria-label="Relational division as a grid" xmlns="http://www.w3.org/2000/svg"><text class="title" x="175.0" y="38" text-anchor="middle">Banjara Hills</text><text class="title" x="285.0" y="38" text-anchor="middle">Kondapur</text><text class="title" x="395.0" y="38" text-anchor="middle">SR Nagar</text><text class="title" x="505.0" y="38" text-anchor="middle">Balanagar</text><text class="" x="108" y="71.0" text-anchor="end" style="font-weight:400">Anand</text><rect class="box" x="161.0" y="55" width="28" height="24" rx="4"/><text class="t-ink" x="175.0" y="72.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="271.0" y="55" width="28" height="24" rx="4"/><rect class="box" x="381.0" y="55" width="28" height="24" rx="4"/><rect class="box" x="491.0" y="55" width="28" height="24" rx="4"/><text class="t-mut" x="570" y="71.0">1/4</text><text class="" x="108" y="105.0" text-anchor="end" style="font-weight:400">Ankita</text><rect class="box" x="161.0" y="89" width="28" height="24" rx="4"/><rect class="box" x="271.0" y="89" width="28" height="24" rx="4"/><rect class="box" x="381.0" y="89" width="28" height="24" rx="4"/><text class="t-ink" x="395.0" y="106.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="491.0" y="89" width="28" height="24" rx="4"/><text class="t-mut" x="570" y="105.0">1/4</text><text class="" x="108" y="139.0" text-anchor="end" style="font-weight:400">Gopal</text><rect class="box" x="161.0" y="123" width="28" height="24" rx="4"/><rect class="box" x="271.0" y="123" width="28" height="24" rx="4"/><rect class="box" x="381.0" y="123" width="28" height="24" rx="4"/><text class="t-ink" x="395.0" y="140.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="491.0" y="123" width="28" height="24" rx="4"/><text class="t-mut" x="570" y="139.0">1/4</text><rect class="box-ink" x="20" y="154" width="630" height="30" rx="6" style="opacity:.22"/><text class="t-ink" x="108" y="173.0" text-anchor="end" style="font-weight:600">Karteek</text><rect class="box" x="161.0" y="157" width="28" height="24" rx="4"/><text class="t-ink" x="175.0" y="174.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="271.0" y="157" width="28" height="24" rx="4"/><text class="t-ink" x="285.0" y="174.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="381.0" y="157" width="28" height="24" rx="4"/><text class="t-ink" x="395.0" y="174.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="491.0" y="157" width="28" height="24" rx="4"/><text class="t-ink" x="505.0" y="174.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><text class="t-ink" x="570" y="173.0">4/4  → kept</text><text class="" x="108" y="207.0" text-anchor="end" style="font-weight:400">Sunil</text><rect class="box" x="161.0" y="191" width="28" height="24" rx="4"/><rect class="box" x="271.0" y="191" width="28" height="24" rx="4"/><text class="t-ink" x="285.0" y="208.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><rect class="box" x="381.0" y="191" width="28" height="24" rx="4"/><rect class="box" x="491.0" y="191" width="28" height="24" rx="4"/><text class="t-ink" x="505.0" y="208.0" text-anchor="middle" style="font-size:14px;font-weight:700">✓</text><text class="t-mut" x="570" y="207.0">2/4</text></svg><figcaption>Division in 2025 Q62. Each tick is a (branch, customer) pair from π(branch, customer)(Loan ⋈ Borrower). Dividing by π(branch)(Loan) keeps a customer only if their row is ticked in every branch column. Only Karteek's row is complete, so the result has 1 tuple.</figcaption></figure>
<!-- /fig:ra-division -->

Expressed with the basic operators:

$$
R \div S = \pi_X(R) - \pi_X\big((\pi_X(R) \times S) - R\big).
$$

Read it as: take all candidate $x$ values, then remove every $x$ that is **missing** some $y$. The term $(\pi_X(R) \times S) - R$ lists exactly the missing $(x, y)$ pairs.

## 2.4 Expressing "every …" with set difference

"Every name in A appears in B or C" means **there's no name in A outside B ∪ C**:

$$
\pi_{\text{name}}(A) - \big(\pi_{\text{name}}(B) \cup \pi_{\text{name}}(C)\big) = \emptyset.
$$

General pattern: **"all of X are in Y" ⟺ X − Y = ∅.** Use ∪ for "in B **or** C" and ∩ for "in B **and** C".

## 2.5 Cardinality bounds (MSQ favourites)

<div class="formula">

| Expression | Number of rows |
|---|---|
| $\sigma(R)$ | $0$ to $|R|$ |
| $\pi(R)$ | $1$ to $|R|$ (if $R$ is non-empty), since duplicates collapse |
| $R \times S$ | exactly $|R|\cdot|S|$ |
| $R \bowtie S$ | $0$ to $|R|\cdot|S|$ |
| $R \bowtie S$ on a foreign key of $R$ (not NULL) referencing the key of $S$ | exactly $|R|$ |
| $R \cup S$ | $\max(|R|, |S|)$ to $|R| + |S|$ |
| $R \cap S$ | $0$ to $\min(|R|, |S|)$ |
| $R - S$ | $0$ to $|R|$ |
| $R ⟕ S$ | at least $|R|$ |

</div>

## 2.6 Reading an expression: inside out

Evaluate the **innermost** part first and say in words what each step produces.

$\pi_{\text{owner}}\big(\text{Own} \bowtie \sigma_{\text{color} = \text{red}}(\text{Car} \bowtie \sigma_{\text{maker} = \text{ABC}}\,\text{Make})\big)$:

1. $\sigma_{\text{maker} = \text{ABC}}\,\text{Make}$: the models made by ABC.
2. $\text{Car} \bowtie (\dots)$: the cars of those models.
3. $\sigma_{\text{color} = \text{red}}$: the red ones among them.
4. $\text{Own} \bowtie (\dots)$, then $\pi_{\text{owner}}$: who owns them.

So the expression means **owners of a red car made by ABC**. Each condition narrows the same set of cars, so they combine with **and**, not or.

## 2.7 Tuple relational calculus (TRC)

TRC is **declarative**: you describe the rows you want, not how to compute them.

$$
\{\,t \mid P(t)\,\}
$$

means all tuples $t$ that make the formula $P$ true. $P$ is built from $t \in R$, comparisons such as $t[A] = s[B]$, the connectives $\land, \lor, \lnot, \Rightarrow$, and the quantifiers $\exists s \in R$ and $\forall s \in R$.

- $\exists m \in Y\,(m[P] = t[P] \land m[S] > 1)$ means **some** row of Y matches $t$ on P and has $S > 1$. It acts like a **semi-join** filter.
- $\forall$ expresses division-style conditions.
- **Safe expressions** only return values that appear in the database. $\{t \mid \lnot(t \in R)\}$ is **unsafe**, because it describes an infinite set.
- Codd's theorem: relational algebra, safe TRC and safe domain calculus have **the same expressive power**. A language with this power is called **relationally complete**.

Evaluate TRC row by row: for each candidate $t$, check every clause.

---

## Summary: important points

<div class="formula">

1. σ filters rows, π keeps columns and **removes duplicates**, × pairs every row with every row.
2. Natural join matches on **all** common attribute names and keeps one copy. NULL never matches.
3. Outer joins keep unmatched rows and pad them with NULL.
4. Division $R \div S$: the $x$ values paired with **every** $y$ in $S$. $= \pi_X(R) - \pi_X((\pi_X(R) \times S) - R)$.
5. "All of X are in Y" ⟺ $X - Y = \emptyset$.
6. $|R \times S| = |R||S|$. A join has between 0 and $|R||S|$ rows. A FK–PK join returns exactly the number of child rows.
7. Read nested expressions from the inside out.
8. TRC: $\{t \mid P(t)\}$, with ∃ and ∀. Safe TRC has the same power as RA.

</div>

<div class="trap">

- Natural join on two shared columns needs **both** to match.
- In "in B **or** C", use ∪, not ∩.
- Projection removes duplicates in RA, but not in SQL (unless you write `DISTINCT`).

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q62 (2 marks, NAT)

Loan(loan_num, branch, amount) and Borrower(customer, loan_num), as in the paper. How many tuples does $\pi_{\text{branch}, \text{customer}}(\text{Loan} \bowtie \text{Borrower}) \div \pi_{\text{branch}}(\text{Loan})$ return?

<details>
<summary>Show solution</summary>

**Answer: 1**

There are 4 branches: Banjara Hills, Kondapur, SR Nagar and Balanagar. The join gives these (branch, customer) pairs (the grid in §2.3):

- Anand: Banjara
- Ankita: SR Nagar
- Gopal: SR Nagar
- **Karteek**: Banjara (L11), Kondapur (L14), SR Nagar (L22), Balanagar (L23). That's all 4.
- Sunil: Balanagar, Kondapur

Only Karteek is paired with every branch, so the result is 1 tuple.

</details>

### GATE DA 2026 Q42 (2 marks, MCQ)

X(P, Q, R): (P1,Q1,R1), (P2,Q2,R2), (P3,Q3,R2). Y(P, Q, S): (P1,Q1,2), (P1,Q2,5), (P2,Q1,6), (P3,Q3,1). Z(P, T): (P1,T1), (P3,T2), (P4,T3), (P4,NULL). Evaluate
$\pi_{PRS}\big[\sigma_{Q = Q3 \lor R = R2}(X \bowtie Y) \bowtie \sigma_{S > 1}(Y \bowtie Z)\big]$.

<details>
<summary>Show solution</summary>

**Answer: (D) zero rows**

1. $X \bowtie Y$ matches on **(P, Q)**: (P1,Q1,R1,2) and (P3,Q3,R2,1). (P2,Q2) isn't in Y.
2. Selecting $Q = Q3 \lor R = R2$ leaves **(P3, Q3, R2, 1)**.
3. $Y \bowtie Z$ matches on P: (P1,Q1,2,T1), (P1,Q2,5,T1), (P3,Q3,1,T2).
4. Selecting $S > 1$ leaves (P1,Q1,2,T1) and (P1,Q2,5,T1).
5. The final natural join matches on **P, Q, S**. The left side has P3 and the right side only P1, so there are **no matches**.

</details>

### GATE DA 2026 Q59 (2 marks, NAT)

X(P, Q, R) as above. Y(P, S): (P1,10), (P1,15), (P2,20), (P3,1). Evaluate $\{t \mid t \in X \land \exists z \in X(t[P] = z[P]) \land \exists m \in Y(m[P] = t[P] \land m[S] > 1)\}$.

<details>
<summary>Show solution</summary>

**Answer: 2**

The middle clause is always true (take $z = t$). The last clause asks for a Y row with the same P and $S > 1$:

- P1 has 10 ✓
- P2 has 20 ✓
- P3 has only 1 ✗

So the rows (P1,Q1,R1) and (P2,Q2,R2) are returned: **2** tuples.

</details>

### GATE DA 2024 Q26 (1 mark, MCQ)

Defender(name, …), Forward(name, …), Team(name, …). Which expression checks that every name in Team appears in Defender **or** Forward?

<details>
<summary>Show solution</summary>

**Answer: (C)** $\pi_{\text{name}}(\text{Team}) - \big(\pi_{\text{name}}(\text{Defender}) \cup \pi_{\text{name}}(\text{Forward})\big) = \emptyset$

Use the pattern from §2.4. (A) uses ∩, which would mean "in both". (B) and (D) subtract in the wrong direction.

</details>

### GATE DA 2025 Q17 (1 mark, MCQ)

What does $\pi_{\text{owner}}(\text{Own} \bowtie (\sigma_{\text{color} = \text{"red"}}(\text{Car} \bowtie (\sigma_{\text{maker} = \text{"ABC"}}\,\text{Make}))))$ compute?

<details>
<summary>Show solution</summary>

**Answer: (C)** all owners of a red car made by ABC

See §2.6. (A) uses "or", which is wrong. (B) adds a condition the expression doesn't have. (D) returns cars, not owners.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** R(A, B) = {(1,a), (2,a), (3,b)} and S(B, C) = {(a,x), (a,y), (b,z), (c,w)}. How many rows does $R \bowtie S$ have?

<details>
<summary>Show solution</summary>

**Answer: 5**

- B = a: 2 rows of R × 2 rows of S = 4.
- B = b: 1 × 1 = 1.
- B = c: no R rows.

Total: **5**.

</details>

**F2 (2 marks, NAT).** Takes(student, course) = {(s1,c1), (s1,c2), (s1,c3), (s2,c1), (s2,c3), (s3,c1), (s3,c2), (s4,c2), (s4,c1), (s4,c3)}. Required = {c1, c3}. How many tuples does Takes ÷ Required return?

<details>
<summary>Show solution</summary>

**Answer: 3**

s1, s2 and s4 took both c1 and c3. s3 is missing c3.

</details>

**F3 (2 marks, NAT).** R(A, B) = {(1,a), (2,b), (3,c), (4,c)} and S(B, C) = {(a,10), (a,20), (c,30)}. How many rows does $R ⟕ S$ (left outer join on B) have?

<details>
<summary>Show solution</summary>

**Answer: 5**

- (1,a) matches 2 rows.
- (2,b) matches none, so it's kept with NULL: 1 row.
- (3,c) and (4,c) match 1 row each.

Total: $2 + 1 + 1 + 1 = 5$.

</details>

**F4 (2 marks, MSQ).** $|R| = 10$ and $|S| = 4$, and the relations are union-compatible. Which are always true?
(A) $|R \cup S| \ge 10$ (B) $|R \cap S| \le 4$ (C) $|R \times S| = 40$ (D) $|R - S| \ge 6$

<details>
<summary>Show solution</summary>

**Answer: A; B; C; D**

(D): at most 4 rows of R can also be in S, so at least 6 remain.

</details>

**F5 (1 mark, MCQ).** Which expression is equivalent to $R \cap S$?
(A) $R - (R - S)$ (B) $R \cup S - (R - S)$ (C) $(R - S) \cup (S - R)$ (D) $R \times S$

<details>
<summary>Show solution</summary>

**Answer: (A)**

Removing from $R$ everything that is **not** in $S$ leaves exactly the common rows. (C) is the symmetric difference.

</details>

**F6 (2 marks, MCQ).** Emp(eid, dept) and Dept(dept, budget), where dept in Emp is a non-NULL foreign key into Dept. Emp has 50 rows and Dept has 8. How many rows does $\text{Emp} \bowtie \text{Dept}$ have?
(A) 8 (B) 50 (C) 400 (D) between 8 and 50

<details>
<summary>Show solution</summary>

**Answer: (B)**

Every employee matches exactly one department, since the foreign key is non-NULL and points to a key.

</details>
