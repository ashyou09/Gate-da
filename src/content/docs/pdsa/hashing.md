---
title: 6. Hashing
description: Hash functions, load factor, chaining, linear and quadratic probing, double hashing, expected probe counts and deletion.
sidebar:
  label: 6. Hashing
  order: 6
---

**Why it matters:** 2024 Q16 and Q21 and 2025 Q18 came from hashing. The question styles are fixed: **fill the table** for a given hash function and probing rule, or recall the **expected number of probes**. Both are mechanical once you have the rules below.

## Topic map

<div class="mindmap">

- **Hashing**
  - Idea
    - key → slot in $O(1)$ average
    - load factor $\alpha = n/m$
  - Hash functions
    - division $h(k) = k \bmod m$, with $m$ prime
    - multiplication method
  - Collisions: chaining
    - list per slot, average search $1 + \alpha$
  - Collisions: open addressing
    - linear probing → primary clustering
    - quadratic probing → secondary clustering
    - double hashing
    - expected probes $\frac{1}{1-\alpha}$
  - Practicalities
    - deletion needs tombstones
    - rehash when $\alpha$ gets too large
    - Python `dict` / `set`

</div>

## 6.1 The idea

We want `insert`, `search` and `delete` in $O(1)$. A **hash function** $h$ maps each key to a slot in an array of size $m$. When two keys map to the same slot, that's a **collision**, and a collision-resolution method decides where the second key goes.

<div class="formula">

**Load factor**

$$
\alpha = \frac{n}{m} = \frac{\text{keys stored}}{\text{slots}}
$$

With chaining, $\alpha$ can exceed 1. With open addressing, $\alpha \le 1$, since each slot holds at most one key.

</div>

## 6.2 Hash functions

- **Division method:** $h(k) = k \bmod m$. Choose $m$ to be a **prime** that isn't close to a power of 2. If $m = 2^p$, only the last $p$ bits of the key matter, and patterned keys cluster.
- **Multiplication method:** $h(k) = \lfloor m \cdot (kA \bmod 1) \rfloor$ with $0 < A < 1$. Here $m$ can be anything.
- GATE often uses unusual functions like $h(x) = 3x \bmod 10$. Just compute exactly what's written.

A **good** hash function spreads keys uniformly. In the worst case (every key in one slot), every operation becomes $O(n)$.

## 6.3 Chaining

Each slot holds a linked list of every key that hashed there.

<div class="formula">

| Operation | Average (uniform hashing) | Worst |
|---|---|---|
| insert (at the head of the list) | $O(1)$ | $O(1)$ |
| unsuccessful search | $\Theta(1 + \alpha)$ | $\Theta(n)$ |
| successful search | $\Theta(1 + \alpha/2)$ | $\Theta(n)$ |

</div>

Deletion is easy: remove the node from its list.

## 6.4 Open addressing

Every key lives inside the table itself. On a collision you **probe** a sequence of slots $h(k, 0), h(k, 1), h(k, 2), \dots$ until you find an empty one.

| Method | Probe sequence | Weakness |
|---|---|---|
| Linear probing | $(h(k) + i) \bmod m$ | **primary clustering**: long runs of filled slots grow longer |
| Quadratic probing | $(h(k) + c_1 i + c_2 i^2) \bmod m$, often $+i^2$ | **secondary clustering**: keys with the same $h(k)$ follow the same path |
| Double hashing | $(h_1(k) + i \cdot h_2(k)) \bmod m$ | best spread. $h_2(k)$ must never be 0 and should be coprime to $m$ |

<div class="formula">

**Expected probes under uniform hashing** ($\alpha < 1$)

$$
\text{unsuccessful search (and insert)} \;\le\; \frac{1}{1-\alpha}
\qquad\qquad
\text{successful search} \;\le\; \frac{1}{\alpha}\ln\frac{1}{1-\alpha}
$$

At $\alpha = 0.75$: unsuccessful $= 4$ probes, successful $\approx 1.85$.

</div>

An **insert** does exactly the work of an unsuccessful search (probe until you hit an empty slot), so it costs the same.

**Counting probes:** count every slot you examine, **including the first one**. A key that lands directly in an empty slot took 1 probe.

### Deletion in open addressing

If you simply empty a slot, later searches stop there too early and miss keys that probed past it. Instead, mark the slot **DELETED** (a tombstone):

- **search** treats a tombstone as occupied and keeps probing;
- **insert** can reuse a tombstone slot.

## 6.5 In Python

`dict` and `set` are hash tables that use open addressing. That's why:

- keys must be **hashable** (immutable): a `tuple` works, a `list` doesn't;
- `x in d` is $O(1)$ on average;
- the table **resizes** (rehashes) as it fills, so `append`-style inserts are $O(1)$ amortised.

---

## Summary: important points

<div class="formula">

1. $\alpha = n/m$. Chaining allows $\alpha > 1$; open addressing needs $\alpha \le 1$.
2. Chaining: average search $\Theta(1 + \alpha)$, worst case $\Theta(n)$.
3. Linear $(h + i)$ → primary clustering. Quadratic $(h + i^2)$ → secondary clustering. Double hashing $(h_1 + i h_2)$ is the best of the three.
4. Unsuccessful search and insert take $\le \frac{1}{1-\alpha}$ probes. Successful search takes $\le \frac1\alpha \ln \frac1{1-\alpha}$.
5. Probes include the first slot examined.
6. Insertion **order** changes the final table. Follow the given order.
7. Deleting in open addressing needs tombstones.
8. Division method: choose $m$ prime, not a power of 2.

</div>

<div class="trap">

- Wrap around with $\bmod m$. Probing past the last slot continues at slot 0.
- Quadratic probing adds $i^2$ to the **original** $h(k)$, not to the previous probe position.
- "Insert" and "unsuccessful search" have the **same** expected cost.

</div>

---

## Test yourself (A): previous-year questions

### GATE DA 2025 Q18 (1 mark, MCQ)

Table size 10, $h(x) = 3x \bmod 10$, linear probing. Insert 1, 4, 5, 6, 14, 15. Where do 14 and 15 end up?
(A) 2 and 5 (B) 2 and 6 (C) 4 and 5 (D) 4 and 6

<details>
<summary>Show solution</summary>

**Answer: (D) 4 and 6**

| Key | $3x \bmod 10$ | Probes | Slot |
|---|---|---|---|
| 1 | 3 | 3 | 3 |
| 4 | 12 → 2 | 2 | 2 |
| 5 | 15 → 5 | 5 | 5 |
| 6 | 18 → 8 | 8 | 8 |
| 14 | 42 → 2 | 2 ✗, 3 ✗, 4 | **4** |
| 15 | 45 → 5 | 5 ✗, 6 | **6** |

</details>

### GATE DA 2024 Q21 (1 mark, MCQ)

Open addressing with uniform hashing and $\alpha = n/m < 1$. An unsuccessful search takes at most $\frac{1}{1-\alpha}$ expected probes. On average, inserting an element takes at most ___ probes.
(A) $\ln\frac{1}{1-\alpha}$ (B) $\frac{1}{1-\alpha}$ (C) $1 + \frac{\alpha}{2}$ (D) $\frac{1}{1+\alpha}$

<details>
<summary>Show solution</summary>

**Answer: (B)**

An insert probes until it finds an empty slot, which is exactly what an unsuccessful search does. So the bound is the same: $\frac{1}{1-\alpha}$.

The distractors are other formulas from the same chapter. (C) $1 + \frac\alpha2$ is the successful-search cost for **chaining**, and (A) is part of the successful-search bound for open addressing.

</details>

### GATE DA 2024 Q16 (1 mark, MCQ)

Match: (p) First In First Out, (q) Lookup operation, (r) Last In First Out with (i) Stacks, (ii) Queues, (iii) Hash tables.

<details>
<summary>Show solution</summary>

**Answer: (A) p–ii, q–iii, r–i**

A queue is FIFO. A hash table's job is fast lookup. A stack is LIFO.

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1 (1 mark, NAT).** Table of size 10, $h(k) = k \bmod 10$, **linear** probing. Insert 12, 22, 32, 7, 17. Which slot holds 17?

<details>
<summary>Show solution</summary>

**Answer: 8**

- 12 → slot 2.
- 22 → 2 is taken, so 3.
- 32 → 2 and 3 are taken, so 4.
- 7 → slot 7.
- 17 → 7 is taken, so **8**.

</details>

**F2 (2 marks, NAT).** Same keys and table, but with **quadratic** probing $(h(k) + i^2) \bmod 10$. Which slot holds 32?

<details>
<summary>Show solution</summary>

**Answer: 6**

- 12 → 2.
- 22 → 2 is taken ($i = 0$), then $2 + 1 = 3$ ($i = 1$).
- 32 → 2 is taken, then 3 is taken, then $2 + 4 = $ **6** ($i = 2$).

Compare with F1, where linear probing put 32 in slot 4. Quadratic probing jumps further, which is how it avoids primary clustering.

</details>

**F3 (2 marks, NAT).** Double hashing with $m = 11$, $h_1(k) = k \bmod 11$ and $h_2(k) = 7 - (k \bmod 7)$. Insert 14, 25, 36, 47. Which slot holds 47?

<details>
<summary>Show solution</summary>

**Answer: 5**

All four keys have $h_1 = 3$.

| Key | $h_2$ | Probe sequence $3 + i\,h_2 \bmod 11$ | Slot |
|---|---|---|---|
| 14 | 7 | 3 | 3 |
| 25 | $7 - 4 = 3$ | 3 ✗, 6 | 6 |
| 36 | $7 - 1 = 6$ | 3 ✗, 9 | 9 |
| 47 | $7 - 5 = 2$ | 3 ✗, **5** | **5** |

Even though all four keys collide on their first probe, double hashing sends each one along a different path.

</details>

**F4 (1 mark, NAT).** An open-addressed table is 75% full, with uniform hashing. What is the expected maximum number of probes for an unsuccessful search?

<details>
<summary>Show solution</summary>

**Answer: 4**

$\frac{1}{1 - 0.75} = 4$.

</details>

**F5 (2 marks, NAT).** Three keys are inserted into a table of 10 slots. Each key independently hashes to a uniformly random slot. What is the probability that **no** collision occurs? (Two decimal places.)

<details>
<summary>Show solution</summary>

**Answer: 0.72**

- The first key always lands in an empty slot.
- The second must avoid 1 used slot: $\frac{9}{10}$.
- The third must avoid 2 used slots: $\frac{8}{10}$.

$1 \times 0.9 \times 0.8 = 0.72$. This mixes hashing with probability, which is a typical GATE DA crossover.

</details>

**F6 (2 marks, MSQ).** Which statements are true?
(A) With chaining, the load factor can exceed 1 (B) Linear probing suffers from primary clustering (C) In open addressing, a deleted slot can simply be marked empty (D) Choosing $m = 2^{10}$ with the division method is ideal

<details>
<summary>Show solution</summary>

**Answer: A; B**

- **(C)** Marking the slot empty breaks later searches. A tombstone is needed.
- **(D)** With $m = 2^{10}$, only the last 10 bits of each key are used. A prime $m$ is preferred.

</details>
