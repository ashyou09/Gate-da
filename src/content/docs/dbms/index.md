---
title: DBMS & Warehousing
description: Every DBMS and data-warehousing question from GATE DA 2024–2026, mapped to topics, with the official answers.
sidebar:
  label: Overview & PYQ map
  order: 0
---

DBMS jumped from **8 and 9 marks** in 2024–25 to **18 marks** in 2026. Almost every question is a **small worked instance**: evaluate this query on this table, find the keys of this schema, insert into this B+ tree. Very few questions ask for definitions alone.

## Official syllabus

> ER-model, relational model: relational algebra, tuple calculus, SQL, integrity constraints, normal form, file organization, indexing, data types, data transformation such as normalization, discretization, sampling, compression; data warehouse modelling: schema for multidimensional data models, concept hierarchies, measures: categorization and computations.

## Every DBMS question, 2024–2026

| Year | Q | Marks | Type | Topic | What it tested | Answer |
|---|---|---|---|---|---|---|
| 2024 | 26 | 1 | MCQ | Relational algebra | "Every Team name is in Defender or Forward" as set difference | C |
| 2024 | 27 | 1 | MCQ | Data transformation | z-score normalization | 0.476 |
| 2024 | 31 | 1 | NAT | SQL | Join + WHERE row count | 3 |
| 2024 | 46 | 2 | MSQ | FDs | Which FDs follow (closure) | A;B;D |
| 2024 | 55 | 2 | MSQ | Indexing | Hash vs B+ tree for range / equality predicates | A;B |
| 2025 | 16 | 1 | MCQ | Normalization | Non-dependency-preserving decomposition needs joins | Join |
| 2025 | 17 | 1 | MCQ | Relational algebra | Read a select–join–project expression | C |
| 2025 | 33 | 1 | NAT | SQL | Subquery with MAX | 3 |
| 2025 | 46 | 2 | MCQ | OLAP | Rows produced by GROUP BY CUBE | 12 |
| 2025 | 56 | 2 | MSQ | Keys & constraints | Primary / foreign keys, NULLs | B;C |
| 2025 | 57 | 2 | MSQ | Normalization | Candidate keys, BCNF | B;D |
| 2025 | 62 | 2 | NAT | Relational algebra | Division | 1 |
| 2026 | 17 | 1 | MCQ | Normalization | Candidate keys from FDs | AD, ED, CD |
| 2026 | 18 | 1 | MCQ | OLAP | Country → State is drill-down | D |
| 2026 | 26 | 1 | MSQ | Integrity constraints | Operations that never violate a foreign key | A;B |
| 2026 | 32 | 1 | NAT | B+ trees | Order of a non-leaf node from sizes | 195 |
| 2026 | 41 | 2 | MCQ | B+ trees | Root after an insertion with splits | 5 |
| 2026 | 42 | 2 | MCQ | Relational algebra | Natural joins + selection on a table | 0 rows |
| 2026 | 43 | 2 | MCQ | Data warehousing | Number of cuboids from concept hierarchies | $4^3$ |
| 2026 | 51 | 2 | MSQ | SQL | Correct query for team size (GROUP BY + join) | A |
| 2026 | 59 | 2 | NAT | Tuple calculus | Evaluate a TRC expression | 2 |
| 2026 | 60 | 2 | NAT | SQL | Correlated subqueries with COUNT | 3 |
| 2026 | 61 | 2 | NAT | ER → relational | Minimum 3NF tables (M:N + multivalued attribute) | 4 |

## What the table says

| Topic | Questions | Verdict |
|---|---|---|
| Relational algebra & tuple calculus | **5** | <span class="tag high">Every year</span> Evaluate the expression on the given tables. |
| SQL | **4** | <span class="tag high">Every year</span> Count the rows a query returns. |
| FDs & normalization | **4** | <span class="tag high">Every year</span> Closure → candidate keys → normal form. |
| ER, keys & constraints | 3 | <span class="tag med">2 of 3 yrs</span> |
| Indexing & B+ trees | 3 | <span class="tag med">2 of 3 yrs</span> 2026 had two. |
| Data warehousing & OLAP | 3 | <span class="tag med">2 of 3 yrs</span> CUBE counts, cuboids, drill-down. |
| Data transformation | 1 | <span class="tag med">Once</span> z-score / min-max. |

:::tip[The skill being tested]
Nearly every DBMS mark comes from **executing something by hand**: a query, a closure, a B+ tree insertion. Write the intermediate tables down. Don't evaluate a three-table join in your head.
:::

## Study material in the repo

- [revision-sheet.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/dbms/revision-sheet.pdf)
- [question-bank.pdf](https://github.com/ashyou09/Gate-da/blob/main/subjects/dbms/question-bank.pdf)
