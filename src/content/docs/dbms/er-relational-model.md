---
title: 1. ER model, relational model, keys & constraints
description: Entities, attributes and relationships, cardinality and participation, converting ER diagrams to tables, relational terminology, super/candidate/primary/foreign keys, and integrity constraints.
sidebar:
  label: 1. ER, keys & constraints
  order: 1
---

**Why it matters:** 2026 Q61 asked for the **minimum number of tables** for an ER diagram. 2025 Q56 and 2026 Q26 asked which **keys** and **foreign-key operations** are valid. These are rule-based questions: learn the mapping rules and the constraint rules, and they're quick marks.

## Topic map

<div class="mindmap">

- **ER & relational model**
  - ER building blocks
    - entity / entity set, attributes (key, composite, multivalued, derived)
    - weak entity + partial key
    - relationship: degree, cardinality (1:1, 1:N, M:N), participation (total / partial)
  - ER → tables
    - one table per strong entity
    - multivalued attribute → its own table
    - 1:N → foreign key on the N side
    - M:N → its own table
  - Relational model
    - relation = set of tuples; degree, cardinality; schema vs instance
  - Keys
    - super ⊇ candidate ⊇ primary; alternate; foreign
    - counting superkeys
  - Integrity constraints
    - domain, entity (PK not NULL), referential (FK)
    - which operations can violate a FK; CASCADE / SET NULL / RESTRICT

</div>

## 1.1 The ER model: describing the world before building tables

The **Entity–Relationship model** describes data at a conceptual level, before any tables exist.

| Concept | Meaning | Chen-notation symbol |
|---|---|---|
| **Entity** | a distinguishable "thing": a student, a course | rectangle |
| **Attribute** | a property of an entity | ellipse |
| Key attribute | uniquely identifies an entity | underlined |
| Composite attribute | made of parts: name = (first, last) | ellipse with sub-ellipses |
| **Multivalued** attribute | can hold several values: phone numbers | **double** ellipse |
| Derived attribute | computable from others: age from DOB | dashed ellipse |
| **Relationship** | an association between entities: *enrolls* | diamond |
| **Weak entity** | can't be identified by its own attributes; depends on an owner | double rectangle, with a **partial key** (dashed underline) |

### Cardinality and participation

- **Cardinality ratio** says how many entities on each side can be linked: **1:1**, **1:N**, or **M:N**.
- **Participation** says whether every entity *must* take part. **Total** participation (a double line) means every entity participates; **partial** (a single line) means some may not.

A weak entity always has **total** participation in its identifying relationship.

<!-- fig:er-q61 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 610 270" role="img" aria-label="ER diagram with many-to-many relationship and multivalued attribute" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="40" y1="45" x2="82.0" y2="110"/><ellipse class="box" cx="40" cy="45" rx="30" ry="15"/><text x="40" y="49" text-anchor="middle" style="text-decoration:underline">A11</text><line class="ax" x1="110" y1="45" x2="110.0" y2="110"/><ellipse class="box" cx="110" cy="45" rx="30" ry="15"/><text x="110" y="49" text-anchor="middle">A12</text><line class="ax" x1="180" y1="45" x2="138.0" y2="110"/><ellipse class="box" cx="180" cy="45" rx="30" ry="15"/><text x="180" y="49" text-anchor="middle">A13</text><line class="ax" x1="400" y1="45" x2="442.0" y2="110"/><ellipse class="box" cx="400" cy="45" rx="30" ry="15"/><text x="400" y="49" text-anchor="middle" style="text-decoration:underline">A21</text><line class="ax" x1="470" y1="45" x2="470.0" y2="110"/><ellipse class="box" cx="470" cy="45" rx="30" ry="15"/><ellipse class="box" style="fill:none" cx="470" cy="45" rx="25" ry="11"/><text x="470" y="49" text-anchor="middle">A22</text><line class="ax" x1="540" y1="45" x2="498.0" y2="110"/><ellipse class="box" cx="540" cy="45" rx="30" ry="15"/><text x="540" y="49" text-anchor="middle">A23</text><line class="ax" x1="155" y1="127" x2="245" y2="127"/><line class="ax" x1="155" y1="133" x2="245" y2="133"/><text class="t-ink" x="200.0" y="120" text-anchor="middle">M</text><line class="ax" x1="425" y1="127" x2="335" y2="127"/><line class="ax" x1="425" y1="133" x2="335" y2="133"/><text class="t-ink" x="380.0" y="120" text-anchor="middle">N</text><polygon class="box" style="stroke:var(--gd-ink);stroke-width:1.6" points="245,130 290,102 335,130 290,158"/><text class="title" x="290" y="135" text-anchor="middle">R12</text><rect class="box" x="65" y="110" width="90" height="40" rx="2" style="stroke:var(--gd-ink);stroke-width:1.6"/><text class="title" x="110" y="135" text-anchor="middle">E1</text><rect class="box" x="425" y="110" width="90" height="40" rx="2" style="stroke:var(--gd-ink);stroke-width:1.6"/><text class="title" x="470" y="135" text-anchor="middle">E2</text><text class="title" x="30" y="205">tables (3NF):</text><rect class="box" x="30" y="215" width="135" height="44" rx="6"/><text class="t-ink" x="97" y="233" text-anchor="middle" style="font-weight:600">E1</text><text x="97" y="250" text-anchor="middle">(A11, A12, A13)</text><rect class="box" x="175" y="215" width="135" height="44" rx="6"/><text class="t-ink" x="242" y="233" text-anchor="middle" style="font-weight:600">E2</text><text x="242" y="250" text-anchor="middle">(A21, A23)</text><rect class="box" x="320" y="215" width="135" height="44" rx="6"/><text class="t-ink" x="387" y="233" text-anchor="middle" style="font-weight:600">E2_A22</text><text x="387" y="250" text-anchor="middle">(A21, A22)</text><rect class="box" x="465" y="215" width="135" height="44" rx="6"/><text class="t-ink" x="532" y="233" text-anchor="middle" style="font-weight:600">R12</text><text x="532" y="250" text-anchor="middle">(A11, A21)</text></svg><figcaption>The ER diagram of 2026 Q61 in Chen notation. Rectangles are entities, the diamond is the relationship, ellipses are attributes (key attributes underlined, the multivalued attribute A22 in a double ellipse). Double lines mean total participation; M and N mark a many-to-many relationship. It needs four 3NF tables.</figcaption></figure>
<!-- /fig:er-q61 -->

## 1.2 Converting an ER diagram into tables

<div class="formula">

| ER construct | Tables produced |
|---|---|
| Strong entity | **one table** with its simple attributes (composite attributes flattened). Primary key = its key |
| **Multivalued attribute** | a **separate table** (entity key, attribute value). Key = both columns together |
| Weak entity | a table with (owner's key + partial key + its attributes). Key = owner key + partial key |
| **1:N** relationship | **no new table**: put the 1-side key into the N-side table as a foreign key (plus the relationship's attributes) |
| **1:1** relationship | no new table: a foreign key on either side, preferably the total-participation side. If **both** sides are total, the two entities can be merged into one table |
| **M:N** relationship | **always a separate table** (key of E1, key of E2, relationship attributes). Key = both foreign keys |
| n-ary relationship | a separate table with all participating keys |

</div>

**Why multivalued attributes and M:N relationships need their own tables:** keeping them inside an entity table would mean repeating that entity's row once per value or partner. That repetition violates 1NF/2NF and creates redundancy (topic 4). Total participation doesn't change this for M:N, because an entity can still have many partners.

**Counting minimum tables** (the GATE question):

1. One table per strong entity, plus one per weak entity.
2. Add one per multivalued attribute.
3. Add one per M:N (and n-ary) relationship.
4. Add none for 1:1 or 1:N (their foreign keys fold in). For a 1:1 with total participation on both sides, the two entities merge, saving a table.

## 1.3 The relational model

A **relation** is a table, more precisely a **set** of tuples over a fixed list of attributes.

| Term | Meaning |
|---|---|
| Tuple | a row |
| Attribute | a named column, with a **domain** (its set of allowed values) |
| Degree (arity) | the number of attributes |
| Cardinality | the number of tuples |
| Schema | the structure: $R(A_1, \dots, A_n)$ |
| Instance | the actual rows at one moment |

In the relational model a relation is a **set**: rows have no order and there are no duplicate rows. (SQL tables are bags and *can* contain duplicates unless a key prevents it.)

## 1.4 Keys

<div class="formula">

- **Superkey:** any set of attributes whose values uniquely identify a tuple.
- **Candidate key:** a **minimal** superkey; no proper subset is a superkey.
- **Primary key:** the candidate key chosen by the designer. It must be **unique and NOT NULL**. The other candidate keys are **alternate keys**.
- **Foreign key:** attribute(s) in one relation that refer to the primary key (or a unique key) of another relation. A foreign-key value must **match an existing referenced value, or be NULL** (unless it's declared NOT NULL).

</div>

**Counting superkeys.** With $n$ attributes and a single candidate key of $k$ attributes, every superset of the key is a superkey: $2^{n-k}$ of them. With two candidate keys $K_1, K_2$, use inclusion–exclusion:

$$
|\text{supersets of } K_1| + |\text{supersets of } K_2| - |\text{supersets of } K_1 \cup K_2| = 2^{n - |K_1|} + 2^{n - |K_2|} - 2^{n - |K_1 \cup K_2|}.
$$

**Declared constraints in SQL:**

- `PRIMARY KEY`: unique and NOT NULL.
- `UNIQUE`: unique, but **NULL is allowed** (standard SQL allows several NULLs). A `UNIQUE NOT NULL` column is effectively a candidate key.
- `NOT NULL`, `CHECK(condition)`, `DEFAULT`.
- A column with **no constraint** can be NULL and can repeat, so it is **not** a key.

## 1.5 Integrity constraints

| Constraint | Rule |
|---|---|
| **Domain** | every value lies in its attribute's domain (type, range, CHECK) |
| **Entity integrity** | no primary-key attribute is NULL |
| **Referential integrity** | every foreign-key value appears as a key in the referenced table (or is NULL) |

### Which operations can break a foreign key?

Let $S.E$ reference $R.A$. $R$ is the **referenced** (parent) table and $S$ is the **referencing** (child) table.

<div class="formula">

| Operation | Can violate the FK? | Why |
|---|---|---|
| Insert into **R** (parent) | **never** | adding a new key can't orphan anything |
| Delete from **S** (child) | **never** | removing a reference can't orphan anything |
| Insert into **S** (child) | yes | the new $E$ value might not exist in $R$ |
| Delete from **R** (parent) | yes | rows in $S$ may still point to the deleted key |
| Update $R.A$ or $S.E$ | yes | the same two reasons |

What happens on a violating delete or update of the parent depends on the rule: `RESTRICT` / `NO ACTION` rejects the operation, `CASCADE` deletes or updates the child rows too, and `SET NULL` / `SET DEFAULT` sets the child's foreign key accordingly.

</div>

---

## Summary: important points

<div class="formula">

1. Entities are rectangles, relationships diamonds, attributes ellipses. Multivalued attributes use a double ellipse; weak entities a double rectangle; total participation a double line.
2. Each strong entity gets a table. Each multivalued attribute gets a table. Each **M:N** relationship gets a table.
3. 1:N: put a foreign key on the N side. 1:1: a foreign key on one side, or merge if both sides are total.
4. Superkey ⊇ candidate key (minimal) ⊇ primary key (chosen; unique and NOT NULL).
5. One candidate key of $k$ out of $n$ attributes gives $2^{n-k}$ superkeys.
6. A foreign key must match an existing referenced value or be NULL.
7. Insert into the parent and delete from the child **never** violate a FK. Insert into the child and delete from the parent can.
8. UNIQUE allows NULL, PRIMARY KEY doesn't. An unconstrained column is not a key.

</div>

<div class="trap">

- Total participation does **not** remove the table for an M:N relationship.
- A foreign key is **not** automatically a candidate key of its own table. It can repeat.
- A relation in the formal model has no duplicate rows. An SQL table can.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q61 (2 marks, NAT)

E1(A11, A12, A13) and E2(A21, A22, A23), with keys A11 and A21. A22 is multivalued. R12 is a many-to-many relationship with total participation on both sides. With no other FDs, what is the minimum number of relations needed so that every relation is in 3NF?

<details>
<summary>Show solution</summary>

**Answer: 4**

1. **E1** → (A11, A12, A13).
2. **E2** without the multivalued attribute → (A21, A23).
3. **Multivalued A22** → (A21, A22), with key (A21, A22).
4. **M:N R12** → (A11, A21), with key (A11, A21).

Total participation can't be used to merge an M:N relationship into either entity, because each E1 row would have to repeat once for every E2 partner.

</details>

### GATE DA 2025 Q56 (2 marks, MSQ)

```sql
Person   (aadhaar CHAR(12) PRIMARY KEY, name VARCHAR(32));
Customer (name VARCHAR(32), email VARCHAR(32) PRIMARY KEY,
          phone CHAR(10), aadhaar CHAR(12),
          FOREIGN KEY (aadhaar) REFERENCES Person(aadhaar));
```

(A) aadhaar is a candidate key in Customer (B) phone can be NULL in Customer (C) aadhaar is a candidate key in Person (D) aadhaar can be NULL in Person

<details>
<summary>Show solution</summary>

**Answer: B; C**

- **(A)** In Customer, aadhaar is only a foreign key. It isn't declared UNIQUE, so two customers may share it (or both have NULL). Not a key.
- **(B)** phone has no NOT NULL constraint, so it can be NULL. True.
- **(C)** It's the primary key of Person, so it's a candidate key. True.
- **(D)** Primary keys can't be NULL (entity integrity). False.

</details>

### GATE DA 2026 Q26 (1 mark, MSQ)

$R(A, B)$ has primary key $A$. $S(E, C)$ has $E$ as a foreign key referencing $A$. Which operations will **never** violate the foreign-key constraint?
(A) inserting into $r$ (B) deleting from $s$ (C) deleting from $r$ (D) inserting into $s$

<details>
<summary>Show solution</summary>

**Answer: A; B**

From the table in §1.5: adding parent rows or removing child rows can't create a dangling reference. Deleting a parent row (C) can orphan child rows, and inserting a child row (D) can reference a non-existent $A$.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** Strong entities Dept(dno, dname) and Emp(eid, name, phones), where phones is multivalued. There's a 1:N relationship WorksIn from Dept to Emp, with partial participation, and a weak entity Dependent(dep_name, age) owned by Emp. What is the minimum number of tables?

<details>
<summary>Show solution</summary>

**Answer: 4**

- Dept and Emp: 2 tables. Emp carries dno as a foreign key (1:N, on the N side).
- Emp_Phone(eid, phone): 1 table.
- Dependent(eid, dep_name, age): 1 table.

Total: **4**.

</details>

**F2 (2 marks, NAT).** $R(A, B, C, D)$ has candidate keys $A$ and $BC$. How many superkeys does it have?

<details>
<summary>Show solution</summary>

**Answer: 10**

$2^{4-1} + 2^{4-2} - 2^{4-3} = 8 + 4 - 2 = 10$. Supersets of {A, B, C} are counted twice, so subtract them once.

</details>

**F3 (1 mark, NAT).** A relation has 5 attributes and exactly one candidate key, made of a single attribute. How many superkeys does it have?

<details>
<summary>Show solution</summary>

**Answer: 16**

$2^{5-1} = 16$: the key plus any subset of the other 4 attributes.

</details>

**F4 (2 marks, MSQ).** Which statements are true?
(A) A primary key column can contain NULL (B) A column declared UNIQUE can contain NULL (C) A foreign-key value may be NULL if the column allows it (D) Every candidate key is a superkey

<details>
<summary>Show solution</summary>

**Answer: B; C; D**

(A) is false: entity integrity forbids NULL in a primary key.

</details>

**F5 (1 mark, MCQ).** Two entities are in a 1:1 relationship with **total** participation on both sides. What is the minimum number of tables?
(A) 1 (B) 2 (C) 3 (D) 4

<details>
<summary>Show solution</summary>

**Answer: (A)**

Every entity on each side is paired with exactly one entity on the other, so the two can be stored as one table without any redundancy.

</details>

**F6 (2 marks, MCQ).** $S.E$ references $R.A$ with `ON DELETE CASCADE`. $R$ has 3 rows with A = 1, 2, 3. $S$ has 5 rows with E = 1, 1, 2, 3, 3. After `DELETE FROM R WHERE A = 3`, how many rows does $S$ have?
(A) 5 (B) 4 (C) 3 (D) 0

<details>
<summary>Show solution</summary>

**Answer: (C)**

CASCADE deletes the two child rows with E = 3, leaving 3 rows.

</details>
