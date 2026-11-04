---
title: 5. File organization, indexing & B+ trees
description: Blocks and blocking factor, heap, sorted and hashed files, primary/clustering/secondary and dense/sparse indexes, multilevel indexes, B+ tree order calculations, insertion with splits, and choosing hash vs B+ tree indexes.
sidebar:
  label: 5. Indexing & B+ trees
  order: 5
---

**Why it matters:** 2026 had **two** B+ tree questions: Q32 (maximum pointers in a node, from byte sizes) and Q41 (the root after an insertion). 2024 Q55 asked which indexes speed up a query with a **range** condition and an **equality** condition. These are mechanical once you know the formulas and the split rules.

## Topic map

<div class="mindmap">

- **Storage & indexing**
  - Disk basics
    - cost = number of block transfers
    - blocking factor $bf = \lfloor B/R \rfloor$, blocks $= \lceil r/bf \rceil$
  - File organizations
    - heap (unordered), sorted, hashed
  - Index types
    - primary (sparse), clustering, secondary (dense)
    - dense vs sparse; clustered vs unclustered
    - multilevel index: fan-out, levels
  - B+ tree
    - all data pointers in the leaves; linked leaves → range scans
    - order from byte sizes
    - insertion: leaf split (copy up), internal split (push up)
  - Choosing an index
    - hash → equality only
    - B+ tree → equality **and** range

</div>

## 5.1 The cost model: blocks

Data lives on disk in fixed-size **blocks** (pages). Reading one block is one I/O, and I/O dominates query time. So we measure cost in **block accesses**, not comparisons.

<div class="formula">

- **Blocking factor** (records per block): $bf = \lfloor B/R \rfloor$ for block size $B$ and record size $R$ (unspanned records).
- **Blocks for $r$ records:** $b = \lceil r/bf \rceil$.

</div>

## 5.2 File organizations

| Organization | Equality search | Range search | Insert |
|---|---|---|---|
| **Heap** (unordered) | linear scan: $b/2$ blocks on average, $b$ worst | full scan | $O(1)$, append at the end |
| **Sorted** on key | binary search: $\lceil\log_2 b\rceil$ | binary search, then read sequentially | expensive (keep it sorted) |
| **Hashed** on key | about 1 block | **no help** (hashing scatters nearby keys) | about 1 block |

## 5.3 Indexes

An index is a small sorted file of (search key, pointer) entries.

<div class="formula">

| Index | Built on | Dense or sparse | Entries |
|---|---|---|---|
| **Primary** | the **ordering key** of a sorted file | sparse | one per **data block** |
| **Clustering** | an ordering **non-key** field | sparse | one per distinct value |
| **Secondary** | any **non-ordering** field | **dense** | one per **record** (key field) |

- **Dense:** an entry for every record. **Sparse:** an entry for only some records (one per block).
- **Clustered:** the data file is physically ordered like the index, so there can be **at most one** per table. Unclustered (secondary) indexes can be many.
- Search with a single-level index $= \lceil\log_2 b_i\rceil + 1$, where $b_i$ is the number of index blocks and the $+1$ reads the data block.
- **Multilevel index:** index the index. The fan-out is $fo = \lfloor B/(\text{key} + \text{pointer})\rfloor$, and the number of levels is the smallest $t$ with $fo^t \ge$ the number of first-level entries. Search costs $t + 1$ block accesses.

</div>

**Worked example.** 30,000 records of 100 bytes, block size 1024 bytes, 9-byte key, 6-byte pointer.

- $bf = 10$, so the file has **3000 blocks**. Binary search on the sorted file: $\lceil\log_2 3000\rceil = 12$ accesses.
- Primary index: 3000 entries of 15 bytes. Index $bf = \lfloor 1024/15 \rfloor = 68$, so $\lceil 3000/68\rceil = 45$ index blocks. Search: $\lceil\log_2 45\rceil + 1 = 7$ accesses.
- Multilevel: the fan-out is 68. Level 1 has 45 blocks; level 2 needs 1 block. So 2 levels, and **3 accesses** (2 index + 1 data).

## 5.4 B+ trees

A B+ tree is a balanced multilevel index that **grows and shrinks** gracefully with inserts and deletes.

- **Internal nodes** hold only keys and child pointers, used to route searches.
- **Leaves** hold all the keys with their **data pointers**, and each leaf points to the **next leaf**. That makes **range queries** easy: find the start, then walk along the leaves.
- Every leaf is at the same depth. Each node except the root is **at least half full**: an internal node has at least $\lceil p/2\rceil$ pointers, and the root has at least 2.
- Searching costs (height + 1) block reads, and the height is about $\log_{\text{fan-out}}(\text{keys})$, which is very small.

**B-tree vs B+ tree:** a B-tree stores data pointers in **internal nodes too**, so each internal node holds fewer keys (lower fan-out), and there's no linked leaf level for range scans.

### Order from byte sizes

<div class="formula">

**Internal node** with $p$ child pointers and $p - 1$ keys:

$$
p \cdot P_{\text{node}} + (p - 1)\cdot K \le B
$$

**Leaf** with $n$ (key, data pointer) pairs plus one next-leaf pointer:

$$
n\,(K + P_{\text{data}}) + P_{\text{node}} \le B
$$

Take the **largest integer** that fits.

</div>

### Insertion

1. Search down to the correct leaf and insert the key in sorted order.
2. **Leaf overflow:** split the leaf into two halves and **copy up** a separator into the parent. The key stays in a leaf, because every key must be in the leaf level.
3. **Internal overflow:** split the node and **push up** its middle key. The key moves up and doesn't stay in either half.
4. If the root splits, a new root is created and the tree grows **one level taller**. B+ trees only grow at the root, which keeps every leaf at the same depth.

**Convention check:** books differ on whether a key equal to the separator goes left or right, and on which half gets the extra key after a split. Use the convention the figure in the question uses. In 2026 Q41, the root [5 | 8] above leaf [1, 5] shows that **"≤ separator goes left"**.

<!-- fig:bpt-q41 -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 210" role="img" aria-label="B+ tree before and after an insertion with splits" xmlns="http://www.w3.org/2000/svg"><text class="title" x="150" y="16" text-anchor="middle">before</text><text class="title" x="470" y="16" text-anchor="middle">after inserting 3</text><line class="ax" x1="150" y1="66" x2="245" y2="130"/><line class="ax" x1="150" y1="66" x2="150" y2="130"/><line class="ax" x1="150" y1="66" x2="55" y2="130"/><rect class="box" x="115.0" y="40" width="70" height="26" rx="4" style="stroke:var(--gd-ink);stroke-width:1.4"/><text class="title" x="135.0" y="58" text-anchor="middle">5</text><text class="title" x="165.0" y="58" text-anchor="middle">8</text><line class="grid" x1="150.0" y1="43" x2="150.0" y2="63"/><rect class="box" x="20.0" y="130" width="70" height="26" rx="4" style=""/><text class="title" x="40.0" y="148" text-anchor="middle">1</text><text class="title" x="70.0" y="148" text-anchor="middle">5</text><line class="grid" x1="55.0" y1="133" x2="55.0" y2="153"/><rect class="box" x="115.0" y="130" width="70" height="26" rx="4" style=""/><text class="title" x="135.0" y="148" text-anchor="middle">7</text><text class="title" x="165.0" y="148" text-anchor="middle">8</text><line class="grid" x1="150.0" y1="133" x2="150.0" y2="153"/><rect class="box" x="210.0" y="130" width="70" height="26" rx="4" style=""/><text class="title" x="230.0" y="148" text-anchor="middle">9</text><text class="title" x="260.0" y="148" text-anchor="middle">12</text><line class="grid" x1="245.0" y1="133" x2="245.0" y2="153"/><line class="ax" x1="545" y1="126" x2="590" y2="170"/><line class="ax" x1="545" y1="126" x2="505" y2="170"/><line class="ax" x1="400" y1="126" x2="425" y2="170"/><line class="ax" x1="400" y1="126" x2="350" y2="170"/><line class="ax" x1="470" y1="66" x2="545" y2="100"/><line class="ax" x1="470" y1="66" x2="400" y2="100"/><rect class="box-ink" x="450.0" y="40" width="40" height="26" rx="4" style="stroke:var(--gd-ink);stroke-width:1.4"/><text class="on-ink" x="470.0" y="58" text-anchor="middle">5</text><rect class="box" x="380.0" y="100" width="40" height="26" rx="4" style="stroke:var(--gd-ink);stroke-width:1.4"/><text class="title" x="400.0" y="118" text-anchor="middle">3</text><rect class="box" x="525.0" y="100" width="40" height="26" rx="4" style="stroke:var(--gd-ink);stroke-width:1.4"/><text class="title" x="545.0" y="118" text-anchor="middle">8</text><rect class="box" x="315.0" y="170" width="70" height="26" rx="4" style=""/><text class="title" x="335.0" y="188" text-anchor="middle">1</text><text class="title" x="365.0" y="188" text-anchor="middle">3</text><line class="grid" x1="350.0" y1="173" x2="350.0" y2="193"/><rect class="box" x="405.0" y="170" width="40" height="26" rx="4" style=""/><text class="title" x="425.0" y="188" text-anchor="middle">5</text><rect class="box" x="470.0" y="170" width="70" height="26" rx="4" style=""/><text class="title" x="490.0" y="188" text-anchor="middle">7</text><text class="title" x="520.0" y="188" text-anchor="middle">8</text><line class="grid" x1="505.0" y1="173" x2="505.0" y2="193"/><rect class="box" x="555.0" y="170" width="70" height="26" rx="4" style=""/><text class="title" x="575.0" y="188" text-anchor="middle">9</text><text class="title" x="605.0" y="188" text-anchor="middle">12</text><line class="grid" x1="590.0" y1="173" x2="590.0" y2="193"/><text class="t-mut" x="150" y="190" text-anchor="middle">leaf [1, 5] receives 3 → overflow</text><line class="mut" x1="300" y1="100" x2="330" y2="100"/></svg><figcaption>2026 Q41. Leaves hold at most 2 keys and internal nodes at most 3 pointers; a key equal to a separator goes left (the convention of the figure in the paper). Inserting 3 overflows leaf [1, 5] → split into [1, 3] and [5], separator 3 goes up. The root [3, 5, 8] now has 4 pointers → split: the middle key 5 moves up and becomes the new root.</figcaption></figure>
<!-- /fig:bpt-q41 -->

## 5.5 Choosing an index for a query

| Predicate | Hash index | B+ tree index |
|---|---|---|
| `col = value` (equality) | ✓ (best, about 1 I/O) | ✓ |
| `col > value`, `BETWEEN`, `ORDER BY` | ✗ (useless) | ✓ |
| Join on `a.x = b.y` (equality) | ✓ | ✓ |

**Rule:** a hash index is only useful for **equality**. A **range** condition needs an ordered index, a B+ tree.

---

## Summary: important points

<div class="formula">

1. Cost = block accesses. $bf = \lfloor B/R\rfloor$, blocks $= \lceil r/bf\rceil$.
2. Heap: linear search. Sorted: $\log_2 b$. Hashed: about 1 block for equality, useless for ranges.
3. Primary index is sparse (one entry per block). Secondary on a key is dense (one per record). At most one clustered index.
4. Multilevel: fan-out $= \lfloor B/(K + P)\rfloor$, levels $= \lceil\log_{fo}(\text{entries})\rceil$, search = levels + 1.
5. B+ tree internal node: $pP + (p - 1)K \le B$. Leaf: $n(K + P_d) + P \le B$.
6. A leaf split **copies up** a separator. An internal split **pushes up** the middle key. A root split adds a level.
7. B+ tree leaves hold all keys and are linked, which makes range queries efficient.
8. Hash is for equality only. B+ trees handle equality **and** ranges.

</div>

<div class="trap">

- An internal node has $p$ pointers but only $p - 1$ keys.
- Leaf sizing uses **data** pointers plus one **block** pointer for the next leaf.
- Round **down** for capacity (node order, $bf$) and **up** for counts (blocks, levels).

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2026 Q32 (1 mark, NAT)

Node size 4096 bytes, node pointer 10 bytes, key 11 bytes, data-record pointer 12 bytes. What is the maximum number of node pointers in a non-leaf node?

<details>
<summary>Show solution</summary>

**Answer: 195**

$10p + 11(p - 1) \le 4096$, so $21p \le 4107$ and $p \le 195.6$. The answer is **195**. Data-record pointers don't appear in internal nodes of a B+ tree.

</details>

### GATE DA 2026 Q41 (2 marks, MCQ)

Leaves hold at most 2 keys, and internal nodes have at most 3 pointers. The root is [5 | 8] with leaves [1, 5], [7, 8], [9, 12]. After inserting 3, what is the root?
(A) 5 (B) 8 (C) 3 and 5 (D) 3, 5 and 8

<details>
<summary>Show solution</summary>

**Answer: (A) 5**

1. 3 ≤ 5, so it goes into leaf [1, 5], which becomes [1, 3, 5]. That's more than 2 keys: **split** into [1, 3] and [5], and copy the separator 3 up.
2. The root becomes [3 | 5 | 8] with 4 pointers, more than 3: **split**. The middle key 5 is **pushed up** into a new root. The children are [3] and [8].
3. The new root is **[5]**. The tree's height has grown by one.

</details>

### GATE DA 2024 Q55 (2 marks, MSQ)

Movie(ID, CustomerRating), Genre(ID, Name), Movie_Genre(MovieID, GenreID). The query filters `CustomerRating > 3.4`, `Genre.Name = 'Comedy'` and joins on the IDs. Which indexing options can speed it up?
(A) B+ tree on all attributes (B) Hash on Genre.Name and B+ tree on the rest (C) Hash on Movie.CustomerRating and B+ tree on the rest (D) Hash on all attributes

<details>
<summary>Show solution</summary>

**Answer: A; B**

`CustomerRating > 3.4` is a **range** predicate and needs a B+ tree. `Name = 'Comedy'` and the joins are equalities, which either index type handles.

- (A) B+ trees work everywhere. ✓
- (B) Hash for the equality on Name, B+ trees for the range and joins. ✓
- (C) and (D) put a hash index on CustomerRating, which can't help a `>` condition. ✗

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (2 marks, NAT).** Block 1024 bytes, key 9 bytes, data pointer 7 bytes, block pointer 6 bytes. What is the maximum number of keys in a B+ tree **leaf**?

<details>
<summary>Show solution</summary>

**Answer: 63**

$16n + 6 \le 1024$, so $n \le 63.6$, giving **63**. (An internal node takes $6p + 9(p - 1) \le 1024$, so $p = 68$.)

</details>

**F2 (1 mark, NAT).** How many blocks do 30,000 records of 100 bytes occupy, with block size 1024 bytes and unspanned records?

<details>
<summary>Show solution</summary>

**Answer: 3000**

$bf = 10$, so $30000/10 = 3000$.

</details>

**F3 (2 marks, NAT).** For that file, a primary index uses 15-byte entries (9-byte key, 6-byte pointer). How many block accesses does a search need using binary search on the single-level index, plus one data block?

<details>
<summary>Show solution</summary>

**Answer: 7**

68 entries fit per block, so 3000 entries need 45 index blocks. $\lceil\log_2 45\rceil + 1 = 6 + 1 = 7$.

</details>

**F4 (2 marks, MCQ).** The keys 10, 20, 30, 40, 50, 60, 70 are inserted in order into an empty B+ tree with leaf capacity 2 and at most 3 pointers per internal node. A key equal to a separator goes right, the left half keeps the extra key on a leaf split, and the right leaf's first key is copied up. What is the root at the end?
(A) [30] (B) [50] (C) [30, 50] (D) [30, 50, 70]

<details>
<summary>Show solution</summary>

**Answer: (B)**

- After 30: leaves [10, 20] and [30], root [30].
- After 50: leaves [10, 20], [30, 40], [50], root [30 | 50].
- After 70: leaf [50, 60, 70] splits into [50, 60] and [70], and 70 is copied up. The root [30 | 50 | 70] now overflows, so 50 is pushed up.

The final root is **[50]**, with children [30] and [70]. (I confirmed this with a small B+ tree simulator.)

</details>

**F5 (2 marks, MSQ).** Which statements are true?
(A) In a B+ tree, every key appears in some leaf (B) A hash index can efficiently answer `salary BETWEEN 10 AND 20` (C) A table can have only one clustered index (D) A secondary index on a key field is dense

<details>
<summary>Show solution</summary>

**Answer: A; C; D**

(B) is false: hashing destroys key order, so a range query has to scan.

</details>

**F6 (1 mark, MCQ).** Which file organization gives the fastest single-record lookup by key equality on average?
(A) heap (B) sorted file with binary search (C) hashed file (D) all are equal

<details>
<summary>Show solution</summary>

**Answer: (C)**

Hashing reaches the right block in about 1 access.

</details>
