---
title: 7. Data warehousing & OLAP
description: OLTP vs OLAP, warehouse properties and ETL, fact and dimension tables, star/snowflake/fact-constellation schemas, data cubes and cuboid counts, CUBE and ROLLUP, concept hierarchies, roll-up/drill-down/slice/dice/pivot, and measure categories.
sidebar:
  label: 7. Data warehousing & OLAP
  order: 7
---

**Why it matters:** this is the DA-specific part of DBMS, and it's growing:
- 2025 Q46: rows produced by `GROUP BY CUBE`;
- 2026 Q18: Country → State is which OLAP operation;
- 2026 Q43: number of cuboids from concept hierarchies.

Each needs one formula or one definition.

## Topic map

<div class="mindmap">

- **Data warehousing**
  - OLTP vs OLAP
  - Warehouse
    - subject-oriented, integrated, time-variant, non-volatile
    - ETL, data marts
  - Multidimensional model
    - fact table (measures + FKs), dimension tables
    - star, snowflake, fact constellation
  - Data cube
    - cuboids: $2^n$ without hierarchies, $\prod (L_i + 1)$ with them
    - CUBE, ROLLUP, GROUPING SETS row counts
  - OLAP operations
    - roll-up, drill-down, slice, dice, pivot
  - Measures
    - distributive, algebraic, holistic
    - additive, semi-additive, non-additive

</div>

## 7.1 OLTP vs OLAP

| | OLTP (operational DB) | OLAP (data warehouse) |
|---|---|---|
| Purpose | run the business: orders, payments | analyse the business: trends, reports |
| Queries | short reads and writes of a few rows | long, read-mostly aggregations over many rows |
| Data | current, detailed | historical, summarized |
| Design | normalized (3NF/BCNF) | denormalized (star schema) |
| Users | many clerks and apps | a few analysts |

A **data warehouse** (Inmon) is **subject-oriented** (organised around sales or customers, not around applications), **integrated** (consistent names and units across sources), **time-variant** (keeps history) and **non-volatile** (loaded and read, rarely updated). Data arrives through **ETL**: Extract from sources, Transform (clean, integrate, convert), Load. A **data mart** is a smaller, department-level warehouse.

## 7.2 The multidimensional model

- **Fact table:** one row per event (a sale). It contains numeric **measures** (units, revenue) and a **foreign key to each dimension**. It's large and narrow.
- **Dimension tables:** descriptive context (time, item, location). They're small and wide, and they hold the **concept hierarchies**.

<!-- fig:dw-star -->
<figure class="diagram"><svg class="dg" viewBox="0 0 600 265" role="img" aria-label="Star schema with one fact table and four dimensions" xmlns="http://www.w3.org/2000/svg"><line class="ax" x1="300" y1="130" x2="110" y2="45"/><line class="ax" x1="300" y1="130" x2="490" y2="45"/><line class="ax" x1="300" y1="130" x2="110" y2="215"/><line class="ax" x1="300" y1="130" x2="490" y2="215"/><rect class="box" x="40" y="13" width="140" height="70" rx="6"/><text class="t-ink" x="110" y="31" text-anchor="middle" style="font-weight:700">Time</text><text class="t-mut" x="110" y="49" text-anchor="middle">time_key</text><text class="t-mut" x="110" y="63" text-anchor="middle">day, month</text><text class="t-mut" x="110" y="77" text-anchor="middle">quarter, year</text><rect class="box" x="420" y="13" width="140" height="70" rx="6"/><text class="t-ink" x="490" y="31" text-anchor="middle" style="font-weight:700">Item</text><text class="t-mut" x="490" y="49" text-anchor="middle">item_key</text><text class="t-mut" x="490" y="63" text-anchor="middle">name, brand</text><text class="t-mut" x="490" y="77" text-anchor="middle">type</text><rect class="box" x="40" y="183" width="140" height="70" rx="6"/><text class="t-ink" x="110" y="201" text-anchor="middle" style="font-weight:700">Location</text><text class="t-mut" x="110" y="219" text-anchor="middle">location_key</text><text class="t-mut" x="110" y="233" text-anchor="middle">city, state</text><text class="t-mut" x="110" y="247" text-anchor="middle">country</text><rect class="box" x="420" y="183" width="140" height="70" rx="6"/><text class="t-ink" x="490" y="201" text-anchor="middle" style="font-weight:700">Branch</text><text class="t-mut" x="490" y="219" text-anchor="middle">branch_key</text><text class="t-mut" x="490" y="233" text-anchor="middle">name</text><text class="t-mut" x="490" y="247" text-anchor="middle">type</text><rect class="box-ink" x="215" y="78" width="170" height="104" rx="8"/><text class="on-ink" x="300" y="98" text-anchor="middle" style="font-weight:700">Sales (fact)</text><text class="on-ink" x="300" y="113" text-anchor="middle" style="font-weight:400">time_key</text><text class="on-ink" x="300" y="128" text-anchor="middle" style="font-weight:400">item_key</text><text class="on-ink" x="300" y="143" text-anchor="middle" style="font-weight:400">location_key</text><text class="on-ink" x="300" y="158" text-anchor="middle" style="font-weight:400">branch_key</text><text class="on-ink" x="300" y="173" text-anchor="middle" style="font-weight:400">units_sold, revenue</text></svg><figcaption>A star schema for sales. The central fact table holds the measures (units sold, revenue) and one foreign key per dimension. Each dimension table is denormalized: it holds a whole hierarchy (day → month → quarter → year) in one table. A snowflake schema would split those hierarchies into further normalized tables.</figcaption></figure>
<!-- /fig:dw-star -->

| Schema | Dimensions | Trade-off |
|---|---|---|
| **Star** | one denormalized table per dimension | fewest joins, fastest queries, some redundancy |
| **Snowflake** | dimensions normalized into sub-tables (city → state table → country table) | less redundancy, more joins |
| **Fact constellation** (galaxy) | **several fact tables** share dimension tables | models several business processes |

## 7.3 Data cubes and cuboids

A **cuboid** is one group-by: the data aggregated over some subset of the dimensions.

<!-- fig:dw-lattice -->
<figure class="diagram"><svg class="dg" viewBox="0 0 620 240" role="img" aria-label="Lattice of cuboids for three dimensions" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="310.0" y1="42" x2="120.0" y2="80"/><line class="grid" x1="310.0" y1="42" x2="310.0" y2="80"/><line class="grid" x1="310.0" y1="42" x2="500.0" y2="80"/><line class="grid" x1="120.0" y1="104" x2="120.0" y2="142"/><line class="grid" x1="120.0" y1="104" x2="310.0" y2="142"/><line class="grid" x1="310.0" y1="104" x2="120.0" y2="142"/><line class="grid" x1="310.0" y1="104" x2="500.0" y2="142"/><line class="grid" x1="500.0" y1="104" x2="310.0" y2="142"/><line class="grid" x1="500.0" y1="104" x2="500.0" y2="142"/><line class="grid" x1="120.0" y1="166" x2="310.0" y2="204"/><line class="grid" x1="310.0" y1="166" x2="310.0" y2="204"/><line class="grid" x1="500.0" y1="166" x2="310.0" y2="204"/><rect class="box-ink" x="255.0" y="17" width="110" height="26" rx="13"/><text class="on-ink" x="310.0" y="34" text-anchor="middle">all (apex)</text><text class="t-mut" x="20" y="34">0-D</text><rect class="box" x="92.0" y="79" width="56" height="26" rx="13"/><text class="" x="120.0" y="96" text-anchor="middle">time</text><rect class="box" x="282.0" y="79" width="56" height="26" rx="13"/><text class="" x="310.0" y="96" text-anchor="middle">item</text><rect class="box" x="454.0" y="79" width="92" height="26" rx="13"/><text class="" x="500.0" y="96" text-anchor="middle">location</text><text class="t-mut" x="20" y="96">1-D</text><rect class="box" x="65.0" y="141" width="110" height="26" rx="13"/><text class="" x="120.0" y="158" text-anchor="middle">time, item</text><rect class="box" x="237.0" y="141" width="146" height="26" rx="13"/><text class="" x="310.0" y="158" text-anchor="middle">time, location</text><rect class="box" x="427.0" y="141" width="146" height="26" rx="13"/><text class="" x="500.0" y="158" text-anchor="middle">item, location</text><text class="t-mut" x="20" y="158">2-D</text><rect class="box-ink" x="178.5" y="203" width="263" height="26" rx="13"/><text class="on-ink" x="310.0" y="220" text-anchor="middle">time, item, location (base)</text><text class="t-mut" x="20" y="220">3-D</text></svg><figcaption>The lattice of cuboids for three dimensions (time, item, location) with no hierarchies: 2³ = 8 group-bys. The base cuboid at the bottom groups by all three; the apex at the top is the grand total. Moving up is roll-up (aggregate away a dimension); moving down is drill-down.</figcaption></figure>
<!-- /fig:dw-lattice -->

<div class="formula">

- $n$ dimensions with **no** hierarchies give $2^n$ cuboids (every subset of dimensions).
- With **concept hierarchies**, where dimension $i$ has $L_i$ levels (not counting the virtual top level "all"):

$$
\text{total cuboids} = \prod_{i=1}^{n} (L_i + 1).
$$

The $+1$ is the option of aggregating that dimension away completely ("all").

- The **base cuboid** groups by all dimensions at their finest level. The **apex cuboid** is the single grand total.

</div>

### CUBE, ROLLUP and GROUPING SETS in SQL

```sql
SELECT D1, D2, SUM(val) FROM Facts GROUP BY CUBE (D1, D2);
-- = union of GROUP BY (D1,D2), (D1), (D2), ()
SELECT D1, D2, SUM(val) FROM Facts GROUP BY ROLLUP (D1, D2);
-- = union of GROUP BY (D1,D2), (D1), ()   (hierarchical prefixes only)
```

<div class="formula">

If dimension $D_i$ has $v_i$ distinct values and **all combinations are present**:

$$
\#\text{rows of CUBE} = \prod_i (v_i + 1) \qquad\qquad
\#\text{rows of ROLLUP}(D_1, \dots, D_n) = 1 + v_1 + v_1v_2 + \dots + v_1v_2\cdots v_n
$$

In the CUBE output, a NULL in a dimension column means "all values of that dimension" (a subtotal row).

</div>

For $v_1 = 3$ and $v_2 = 2$: CUBE gives $(3+1)(2+1) = 12$ rows, made up of 6 detail rows, 3 per-D1 subtotals, 2 per-D2 subtotals and 1 grand total. ROLLUP gives $1 + 3 + 6 = 10$.

## 7.4 OLAP operations

<div class="formula">

| Operation | What it does | Example |
|---|---|---|
| **Roll-up** (drill-up) | aggregate to a **coarser** level of a hierarchy, or drop a dimension | city → country; month → year |
| **Drill-down** | go to a **finer** level, or add a dimension | country → state; year → month |
| **Slice** | fix **one** dimension to a single value, giving a cube with one fewer dimension | time = "Q1" |
| **Dice** | select **ranges or sets on two or more** dimensions; the dimensions stay | time ∈ {Q1, Q2} and city ∈ {Pune, Delhi} |
| **Pivot** (rotate) | swap axes to view the data differently | rows ↔ columns |

</div>

**Direction check:** in the hierarchy Country → State → City, going **towards City** is drill-down (more detail), and going **towards Country** is roll-up.

## 7.5 Measures

<div class="formula">

**By how they can be computed from partitions:**

| Category | Definition | Examples |
|---|---|---|
| **Distributive** | combine the per-partition results with the same function | count, sum, min, max |
| **Algebraic** | computed from a **fixed number** of distributive values | avg $= $ sum/count, standard deviation, min-N |
| **Holistic** | no constant-size summary works | **median**, mode, rank |

**By whether they can be summed across dimensions:**

| Category | Meaning | Example |
|---|---|---|
| Additive | sums correctly across **all** dimensions | revenue, units sold |
| Semi-additive | sums across some dimensions, **not time** | account balance, stock level |
| Non-additive | never sums | ratios, percentages, unit price |

</div>

Distributive and algebraic measures make cubes cheap to pre-compute, because the coarser cuboids can be built from finer ones. Holistic measures can't be built this way.

**Storage choices:** **ROLAP** stores the cube in relational tables (scales well). **MOLAP** stores it in multidimensional arrays (fast but can be sparse). **HOLAP** combines the two.

---

## Summary: important points

<div class="formula">

1. OLAP: historical, summarized, read-mostly, denormalized. OLTP: current, detailed, many small transactions.
2. A warehouse is subject-oriented, integrated, time-variant and non-volatile, and is fed by ETL.
3. Fact table = measures + foreign keys. Dimensions hold the hierarchies. Star (denormalized) vs snowflake (normalized) vs constellation (many facts).
4. Cuboids: $2^n$ without hierarchies, $\prod(L_i + 1)$ with $L_i$ levels each.
5. CUBE rows $= \prod(v_i + 1)$ when all combinations exist. ROLLUP rows $= 1 + v_1 + v_1v_2 + \dots$
6. Roll-up goes coarser, drill-down finer. Slice fixes one dimension; dice selects on several.
7. Distributive (sum, count), algebraic (avg, std), holistic (median, mode).
8. Semi-additive measures (balances) can't be summed over time.

</div>

<div class="trap">

- In the cuboid formula, $L_i$ counts real levels. The $+1$ is for "all". Don't add it twice.
- Slice reduces the number of dimensions; dice doesn't.
- Average is **algebraic**, not distributive. You can't average the averages of unequal groups.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q46 (2 marks, MCQ)

Facts(D1, D2, val). D1 takes 3 values and D2 takes 2, and all combinations are present. How many tuples does `SELECT D1, D2, SUM(val) FROM Facts GROUP BY CUBE(D1, D2)` return?
(A) 1 (B) 6 (C) 9 (D) 12

<details>
<summary>Show solution</summary>

**Answer: (D) 12**

The grouping sets are (D1, D2): 6 rows, (D1): 3, (D2): 2, and (): 1. Total: $6 + 3 + 2 + 1 = 12 = (3+1)(2+1)$.

</details>

### GATE DA 2026 Q43 (2 marks, MCQ)

Three concept hierarchies: Day → Month → Year, City → State → Country, Item → Item Type → Item Category. How many data cuboids are possible?
(A) $4^3$ (B) $2^3$ (C) $2!$ (D) $4!$

<details>
<summary>Show solution</summary>

**Answer: (A) $4^3 = 64$**

Each dimension has 3 levels, plus "all", which is 4 choices. With 3 independent dimensions, that's $4 \times 4 \times 4$. ($2^3$ would ignore the hierarchies.)

</details>

### GATE DA 2026 Q18 (1 mark, MCQ)

A cube shows Sales Quantity by (Product Type, Month, **Country**). We now want it by (Product Type, Month, **State**). Which OLAP operation is this?
(A) Slicing (B) Dicing (C) Roll-up (D) Drill-down

<details>
<summary>Show solution</summary>

**Answer: (D) Drill-down**

State is a **finer** level than Country in the location hierarchy, so we're adding detail.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** A fact table has dimensions with 2, 3 and 4 distinct values, and all combinations are present. How many rows does `GROUP BY CUBE` on all three produce?

<details>
<summary>Show solution</summary>

**Answer: 60**

$(2+1)(3+1)(4+1) = 3 \times 4 \times 5 = 60$.

</details>

**F2 (1 mark, NAT).** For 2025 Q46's table, how many rows does `GROUP BY ROLLUP(D1, D2)` produce?

<details>
<summary>Show solution</summary>

**Answer: 10**

$1 + 3 + 3 \times 2 = 10$. The (D2)-only subtotals are **not** included in ROLLUP.

</details>

**F3 (1 mark, NAT).** Time has 4 levels (day, month, quarter, year) and Location has 2 (city, state). How many cuboids are there?

<details>
<summary>Show solution</summary>

**Answer: 15**

$(4 + 1)(2 + 1) = 15$.

</details>

**F4 (2 marks, MSQ).** Which matches of action and operation are correct?
(A) monthly sales → yearly sales: roll-up (B) show only the quarter Q1: slice (C) restrict to quarters Q1–Q2 and cities {Pune, Delhi}: dice (D) swap rows and columns of a report: drill-down

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

(D) is a **pivot**.

</details>

**F5 (2 marks, MSQ).** Which classifications are correct?
(A) SUM: distributive (B) AVERAGE: algebraic (C) MEDIAN: holistic (D) account balance: additive over time

<details>
<summary>Show solution</summary>

**Answer: A; B; C**

An account balance is **semi-additive**. Adding balances across days is meaningless.

</details>

**F6 (1 mark, MCQ).** Which schema normalizes the dimension tables into multiple related tables?
(A) star (B) snowflake (C) fact constellation (D) none

<details>
<summary>Show solution</summary>

**Answer: (B)**

</details>
