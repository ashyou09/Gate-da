---
title: 3. SQL
description: SELECT-FROM-WHERE, the logical evaluation order, joins, GROUP BY and HAVING, aggregates and NULL, nested, correlated and derived-table subqueries, IN / EXISTS / ALL / ANY, and set operations.
sidebar:
  label: 3. SQL
  order: 3
---

**Why it matters:** an SQL question appeared **every year**:
- 2024 Q31: rows returned by a join with filters;
- 2025 Q33: a subquery with MAX;
- 2026 Q51: which queries give the team size;
- 2026 Q60: correlated COUNT subqueries.

All of them are "**run this query in your head**". Every query on this page was also run in SQLite to confirm the answer.

## Topic map

<div class="mindmap">

- **SQL**
  - Query skeleton
    - SELECT · FROM · WHERE · GROUP BY · HAVING · ORDER BY
    - logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
  - Joins
    - comma + WHERE, JOIN … ON, NATURAL JOIN, LEFT/RIGHT/FULL OUTER
  - Aggregation
    - COUNT(*), COUNT(col), SUM, AVG, MIN, MAX
    - aggregates ignore NULL (except COUNT(*))
    - WHERE vs HAVING
  - Subqueries
    - scalar, IN / NOT IN, EXISTS, ALL / ANY
    - correlated: re-run for every outer row
    - derived tables in FROM
  - NULL
    - three-valued logic; NOT IN with NULL returns nothing
  - Set operations
    - UNION (removes duplicates), UNION ALL, INTERSECT, EXCEPT

</div>

## 3.1 The query skeleton and its real evaluation order

```sql
SELECT   dept, AVG(salary) AS avg_sal
FROM     Emp
WHERE    salary > 30
GROUP BY dept
HAVING   COUNT(*) >= 2
ORDER BY avg_sal DESC;
```

<!-- fig:sql-order -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 244" role="img" aria-label="Logical evaluation order of an SQL query" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="20" y="20" width="140" height="62" rx="8"/><text class="t-ink" x="32" y="42" style="font-weight:700">1. FROM / JOIN</text><text class="t-mut" x="32" y="64">combine rows</text><path class="ax" d="M162,51.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box-ink" x="174" y="20" width="140" height="62" rx="8"/><text class="on-ink" x="186" y="42" style="font-weight:700">2. WHERE</text><text class="on-ink" x="186" y="64">filter rows</text><path class="ax" d="M316,51.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box" x="328" y="20" width="140" height="62" rx="8"/><text class="t-ink" x="340" y="42" style="font-weight:700">3. GROUP BY</text><text class="t-mut" x="340" y="64">make groups</text><path class="ax" d="M470,51.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box-ink" x="482" y="20" width="140" height="62" rx="8"/><text class="on-ink" x="494" y="42" style="font-weight:700">4. HAVING</text><text class="on-ink" x="494" y="64">filter groups</text><rect class="box" x="20" y="122" width="140" height="62" rx="8"/><text class="t-ink" x="32" y="144" style="font-weight:700">5. SELECT</text><text class="t-mut" x="32" y="166">pick columns</text><path class="ax" d="M162,153.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box" x="174" y="122" width="140" height="62" rx="8"/><text class="t-ink" x="186" y="144" style="font-weight:700">6. DISTINCT</text><text class="t-mut" x="186" y="166">drop duplicates</text><path class="ax" d="M316,153.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box" x="328" y="122" width="140" height="62" rx="8"/><text class="t-ink" x="340" y="144" style="font-weight:700">7. ORDER BY</text><text class="t-mut" x="340" y="166">sort rows</text><path class="ax" d="M470,153.0 h10 m-5,-4 l5,4 l-5,4"/><rect class="box" x="482" y="122" width="140" height="62" rx="8"/><text class="t-ink" x="494" y="144" style="font-weight:700">8. LIMIT</text><text class="t-mut" x="494" y="166">keep n rows</text><path class="ax" d="M552.0,84 v14 H90.0 v14 m-4,-5 l4,5 l4,-5"/><text class="t-mut" x="20" y="232">written order: SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT</text></svg><figcaption>The logical order in which SQL evaluates a query, which is not the order you write it in. WHERE filters rows before grouping (so it cannot use aggregates); HAVING filters groups after aggregation; SELECT aliases exist only from the SELECT step onward, so ORDER BY can use them but WHERE cannot.</figcaption></figure>
<!-- /fig:sql-order -->

This order explains most rules:

- **WHERE can't use aggregates.** Groups don't exist yet at that step. Use HAVING.
- **Every SELECT column must be grouped or aggregated** once GROUP BY is used. A bare `eid` with `GROUP BY dept` is an error, because one group has many eids.
- **SQL keeps duplicates** unless you write `DISTINCT`, unlike relational algebra's π.

## 3.2 Joins in SQL

```sql
-- old style: Cartesian product + condition
SELECT * FROM Raider, Team WHERE Raider.ID = Team.ID;
-- explicit
SELECT * FROM Raider JOIN Team ON Raider.ID = Team.ID;
-- keep unmatched Raiders, padding Team columns with NULL
SELECT * FROM Raider LEFT JOIN Team ON Raider.ID = Team.ID;
```

`SELECT *` over a join returns the columns of **both** tables, so ID appears twice unless you use `NATURAL JOIN` or `USING (ID)`.

## 3.3 Aggregates and NULL

<div class="formula">

| Expression | Counts / uses |
|---|---|
| `COUNT(*)` | **all rows**, NULLs included |
| `COUNT(col)` | rows where `col` is **not NULL** |
| `COUNT(DISTINCT col)` | distinct non-NULL values |
| `SUM`, `AVG`, `MIN`, `MAX` | **ignore NULLs**. `AVG(10, NULL, 20) = 15`, not 10 |
| Aggregate over zero rows | `COUNT` → 0, the others → NULL |

**GROUP BY puts all NULLs in one group.**

</div>

Example: Emp(eid, dept, salary) = (1,CS,50), (2,CS,70), (3,EE,40), (4,EE,60), (5,EE,80), (6,ME,30), (7,NULL,90).

- `SELECT COUNT(*), COUNT(dept), COUNT(DISTINCT dept) FROM Emp` → **7, 6, 3**.
- `GROUP BY dept` → groups CS (2), EE (3), ME (1) and **NULL (1)**.

## 3.4 NULL and three-valued logic

Any comparison with NULL gives **UNKNOWN**, and WHERE keeps only rows that are **TRUE**.

- `dept <> 'CS'` is UNKNOWN for the NULL row, so that row is **dropped**. This returns 4 rows, not 5.
- Use `IS NULL` / `IS NOT NULL`, never `= NULL`.
- **The `NOT IN` trap:** `x NOT IN (a, NULL)` means `x <> a AND x <> NULL`. The second part is never TRUE, so **no rows are returned**.

## 3.5 Subqueries

<div class="formula">

| Form | Meaning |
|---|---|
| `x > (SELECT MAX(…) …)` | **scalar** subquery: it must return one value |
| `x IN (SELECT …)` | $x$ equals some returned value |
| `EXISTS (SELECT …)` | the subquery returns at least one row |
| `x > ALL (SELECT …)` | greater than **every** value, i.e. `> MAX` (TRUE if the subquery is empty) |
| `x > ANY (SELECT …)` | greater than **at least one**, i.e. `> MIN` |
| **Correlated** subquery | refers to the outer row, so it's **re-evaluated for each outer row** |
| Derived table | a subquery in FROM with an alias, used like a table |

</div>

**Evaluating a correlated query** (2026 Q60 style): make a small table with one line per outer row, compute the inner result **for that row**, and test the condition.

Two common correlated patterns:

```sql
-- employees paid more than their department's average
SELECT eid FROM Emp e
WHERE salary > (SELECT AVG(salary) FROM Emp x WHERE x.dept = e.dept);   -- returns 2, 5

-- second-highest salary
SELECT MAX(salary) FROM Emp WHERE salary < (SELECT MAX(salary) FROM Emp);   -- 80
```

## 3.6 Set operations

`UNION`, `INTERSECT` and `EXCEPT` (`MINUS` in Oracle) need union-compatible SELECT lists, and they **remove duplicates**. `UNION ALL` keeps them.

---

## Summary: important points

<div class="formula">

1. Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.
2. WHERE filters rows (no aggregates). HAVING filters groups.
3. With GROUP BY, SELECT may only contain grouped columns and aggregates.
4. `COUNT(*)` counts rows. `COUNT(col)` skips NULLs. SUM, AVG, MIN and MAX ignore NULL.
5. Comparisons with NULL are UNKNOWN and get filtered out. `NOT IN` with a NULL in the list returns nothing.
6. A scalar subquery returns one value. `> ALL` = `> MAX`, `> ANY` = `> MIN`.
7. A correlated subquery is re-run per outer row: tabulate it.
8. SQL keeps duplicates unless you use DISTINCT. UNION removes them, UNION ALL keeps them.

</div>

<div class="trap">

- `SELECT *` over a comma join repeats the join column.
- A self-join condition like `A.EmpID = B.EmpID` matches each row only with **itself**, so any count is 1.
- A derived table can only be joined on columns it actually outputs (2026 Q51 option D).

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2024 Q31 (1 mark, NAT)

Raider(ID, Name, Raids, RaidPoints) with RaidPoints 250, 219, 200, 190, 220, 215 for IDs 1–6. Team(City, ID, BidPoints): Jaipur has IDs 2, 1 and 6; Patna has 3 and 4; Hyderabad has 5.

```sql
SELECT * FROM Raider, Team
WHERE Raider.ID = Team.ID AND City = 'Jaipur' AND RaidPoints > 200;
```

How many rows are returned?

<details>
<summary>Show solution</summary>

**Answer: 3**

- RaidPoints > 200: IDs 1 (250), 2 (219), 5 (220), 6 (215).
- Jaipur IDs: 2, 1, 6.
- Both conditions: IDs 1, 2, 6, so **3 rows**.

</details>

### GATE DA 2025 Q33 (1 mark, NAT)

Loan amounts: L11 90000, L14 50000, L15 40000 (SR Nagar), L22 25000 (SR Nagar), L23 80000, L25 70000, L19 65000 (SR Nagar).

```sql
SELECT L1.loan_number FROM Loan L1
WHERE L1.amount > (SELECT MAX(L2.amount) FROM Loan L2 WHERE L2.branch_name = 'SR Nagar');
```

<details>
<summary>Show solution</summary>

**Answer: 3**

The subquery returns the largest SR Nagar amount, which is 65000. Amounts above 65000: 90000 (L11), 80000 (L23), 70000 (L25). That's 3 rows.

</details>

### GATE DA 2026 Q60 (2 marks, NAT)

Account balances: A1 5000, A2 5000, A3 10000, A4 15000, A5 18000.

```sql
SELECT AccNo FROM Account AS A
WHERE (SELECT COUNT(*) FROM Account AS B WHERE A.Balance < B.Balance)
   >= (SELECT COUNT(*) FROM Account AS C WHERE A.Balance > C.Balance);
```

<details>
<summary>Show solution</summary>

**Answer: 3**

For each row, count the accounts that are richer and the accounts that are poorer:

| AccNo | # with higher balance | # with lower balance | richer ≥ poorer? |
|---|---|---|---|
| A1 (5000) | 3 | 0 | ✓ |
| A2 (5000) | 3 | 0 | ✓ (the tie with A1 counts in neither) |
| A3 (10000) | 2 | 2 | ✓ |
| A4 (15000) | 1 | 3 | ✗ |
| A5 (18000) | 0 | 4 | ✗ |

**3 rows** are returned (A1, A2, A3): the "lower half" of the table.

</details>

### GATE DA 2026 Q51 (2 marks, MSQ)

Employee(EmpID, TeamID), with TeamID NOT NULL. Which query outputs each employee's team size (3, 3, 3, 2, 2, 1 for the sample data)?

<details>
<summary>Show solution</summary>

**Answer: (A) only**

- **(A)** The derived table B computes (TeamID, COUNT) per team, then joins it back on TeamID. ✓ It gives 3, 3, 3, 2, 2, 1.
- **(B)** `A.EmpID = B.EmpID` pairs each employee only with themselves, so every count is **1**. ✗
- **(C)** `GROUP BY EmpID` makes one group per employee, so again every count is 1. ✗
- **(D)** The derived table only outputs TeamSize, so `B.TeamID` doesn't exist and the query is an **error**. ✗ (SQLite reports "no such column: B.TeamID".)

</details>

---

## Test yourself (B): predicted 2027-style questions

Use the Emp table from §3.3: (1,CS,50), (2,CS,70), (3,EE,40), (4,EE,60), (5,EE,80), (6,ME,30), (7,NULL,90).

**F1 (2 marks, NAT).** How many rows does this return?

```sql
SELECT dept, AVG(salary) FROM Emp WHERE dept IS NOT NULL
GROUP BY dept HAVING COUNT(*) >= 2;
```

<details>
<summary>Show solution</summary>

**Answer: 2**

CS (2 rows) and EE (3 rows) pass the HAVING condition. ME has only 1 row.

</details>

**F2 (1 mark, NAT).** What does `SELECT COUNT(*) FROM Emp WHERE dept NOT IN ('CS', NULL);` return?

<details>
<summary>Show solution</summary>

**Answer: 0**

`dept <> NULL` is never TRUE, so the whole condition is never TRUE. This is the NOT IN trap from §3.4.

</details>

**F3 (1 mark, NAT).** What does `SELECT COUNT(*) FROM Emp WHERE dept <> 'CS';` return?

<details>
<summary>Show solution</summary>

**Answer: 4**

The EE (3) and ME (1) rows qualify. For the NULL row, the comparison is UNKNOWN, so it's excluded.

</details>

**F4 (2 marks, NAT).** How many employees earn more than the average salary of their own department? (`x.dept = e.dept`)

<details>
<summary>Show solution</summary>

**Answer: 2**

- CS average 60: eid 2 (70) qualifies.
- EE average 60: eid 5 (80) qualifies.
- ME average 30: nobody is strictly above.
- eid 7: `x.dept = NULL` matches nothing, so the inner AVG is NULL and the comparison is UNKNOWN.

Result: {2, 5}, so **2**.

</details>

**F5 (2 marks, MSQ).** Which statements are true?
(A) `salary > ALL (SELECT salary FROM Emp WHERE dept='EE')` is true for exactly 1 employee (B) `salary > ANY (…same…)` is true for exactly 5 employees (C) `COUNT(dept)` equals `COUNT(*)` on Emp (D) `AVG(salary)` ignores NULL salaries

<details>
<summary>Show solution</summary>

**Answer: A; B; D**

- (A): `> ALL` means > 80, so only 90 (eid 7).
- (B): `> ANY` means > 40: 50, 70, 60, 80, 90.
- (C) is false: the counts are 6 vs 7.

</details>

**F6 (1 mark, MCQ).** Which query is invalid in standard SQL?
(A) `SELECT dept, COUNT(*) FROM Emp GROUP BY dept` (B) `SELECT dept FROM Emp GROUP BY dept HAVING AVG(salary) > 50` (C) `SELECT dept, eid FROM Emp GROUP BY dept` (D) `SELECT COUNT(*) FROM Emp WHERE salary > 50`

<details>
<summary>Show solution</summary>

**Answer: (C)**

eid is neither grouped nor aggregated, and a group holds several eids.

</details>
