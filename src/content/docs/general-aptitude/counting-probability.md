---
title: 5. Counting, probability & statistics
description: Permutations and combinations with restrictions, divisibility-based counting, classical and binomial probability, complements, and mean/median/mode puzzles.
sidebar:
  label: 5. Counting & probability
  order: 5
---

**Why it matters:** 2024 Q3 (counting numbers divisible by 3), 2024 Q7 (two girls and one boy) and 2026 Q7 (five integers with a given mean, median and mode) are small, exact counting problems. The trick in each one is to **organise the cases** so nothing is double-counted.

## Topic map

<div class="mindmap">

- **Counting & probability**
  - Counting principles
    - multiply for "and", add for disjoint "or"
    - permutations $n!/(n-r)!$, combinations $\binom nr$
    - repeated items: $n!/(n_1!\,n_2!\cdots)$
  - Restrictions
    - fix the restricted place first (no leading 0, even last digit)
    - divisibility by digit sum
    - complement: total − bad
  - Probability
    - favourable / total (equally likely outcomes)
    - complement, "at least one"
    - binomial $\binom nk p^k(1-p)^{n-k}$
  - Statistics puzzles
    - sum = n × mean, median = middle value, mode = most frequent

</div>

## 5.1 Counting rules

<div class="formula">

| Situation | Count |
|---|---|
| ordered selection of $r$ from $n$, no repetition | $^nP_r = \dfrac{n!}{(n-r)!}$ |
| unordered selection | $\binom nr = \dfrac{n!}{r!(n-r)!}$ |
| arrangements of $n$ items with repeats $n_1, n_2, \dots$ | $\dfrac{n!}{n_1!\,n_2!\cdots}$ (LEVEL: $\frac{5!}{2!\,2!} = 30$) |
| "at least one" of a kind | total − (none of that kind) |
| circular arrangements of $n$ | $(n-1)!$ |

</div>

**Restricted digit counting:** fill the **most restricted position first** (the first digit can't be 0; the last digit must be even), then multiply the choices for the other positions. If the restricted cases overlap, split into cases (for example, last digit 0 vs another even digit).

**Divisibility by 3:** a number is divisible by 3 exactly when its digit sum is. So choose the **set** of digits first (by its sum), then arrange it.

## 5.2 Probability

<div class="formula">

- Equally likely outcomes: $P(A) = \dfrac{|A|}{|\Omega|}$.
- **Complement:** $P(\text{at least one}) = 1 - P(\text{none})$.
- **Binomial** ($n$ independent trials, success probability $p$): $P(k \text{ successes}) = \binom nk p^k (1-p)^{n-k}$.
- Drawing without replacement: count with combinations, e.g. $P(\text{2 red from } 3R, 2B) = \binom32/\binom52 = 3/10$.

</div>

<!-- fig:ga-prob-tree -->
<figure class="diagram"><svg class="dg" viewBox="0 0 640 252" role="img" aria-label="Probability tree for three children" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="320" y1="32" x2="170.0" y2="63" style="stroke-width:1.4"/><line class="grid" x1="170.0" y1="87" x2="95.0" y2="118" style="stroke-width:1.4"/><line class="grid" x1="95.0" y1="142" x2="57.5" y2="173" style="stroke-width:1.4"/><text class="t-mut" x="57.5" y="215" text-anchor="middle" style="font-weight:400">GGG</text><circle class="box" cx="57.5" cy="185" r="12"/><text class="title" x="57.5" y="189" text-anchor="middle">G</text><line class="grid" x1="95.0" y1="142" x2="132.5" y2="173" style="stroke-width:1.4"/><text class="t-ink" x="132.5" y="215" text-anchor="middle" style="font-weight:700">GGB</text><circle class="box" cx="132.5" cy="185" r="12"/><text class="title" x="132.5" y="189" text-anchor="middle">B</text><circle class="box" cx="95.0" cy="130" r="12"/><text class="title" x="95.0" y="134" text-anchor="middle">G</text><line class="grid" x1="170.0" y1="87" x2="245.0" y2="118" style="stroke-width:1.4"/><line class="grid" x1="245.0" y1="142" x2="207.5" y2="173" style="stroke-width:1.4"/><text class="t-ink" x="207.5" y="215" text-anchor="middle" style="font-weight:700">GBG</text><circle class="box" cx="207.5" cy="185" r="12"/><text class="title" x="207.5" y="189" text-anchor="middle">G</text><line class="grid" x1="245.0" y1="142" x2="282.5" y2="173" style="stroke-width:1.4"/><text class="t-mut" x="282.5" y="215" text-anchor="middle" style="font-weight:400">GBB</text><circle class="box" cx="282.5" cy="185" r="12"/><text class="title" x="282.5" y="189" text-anchor="middle">B</text><circle class="box" cx="245.0" cy="130" r="12"/><text class="title" x="245.0" y="134" text-anchor="middle">B</text><circle class="box" cx="170.0" cy="75" r="12"/><text class="title" x="170.0" y="79" text-anchor="middle">G</text><line class="grid" x1="320" y1="32" x2="470.0" y2="63" style="stroke-width:1.4"/><line class="grid" x1="470.0" y1="87" x2="395.0" y2="118" style="stroke-width:1.4"/><line class="grid" x1="395.0" y1="142" x2="357.5" y2="173" style="stroke-width:1.4"/><text class="t-ink" x="357.5" y="215" text-anchor="middle" style="font-weight:700">BGG</text><circle class="box" cx="357.5" cy="185" r="12"/><text class="title" x="357.5" y="189" text-anchor="middle">G</text><line class="grid" x1="395.0" y1="142" x2="432.5" y2="173" style="stroke-width:1.4"/><text class="t-mut" x="432.5" y="215" text-anchor="middle" style="font-weight:400">BGB</text><circle class="box" cx="432.5" cy="185" r="12"/><text class="title" x="432.5" y="189" text-anchor="middle">B</text><circle class="box" cx="395.0" cy="130" r="12"/><text class="title" x="395.0" y="134" text-anchor="middle">G</text><line class="grid" x1="470.0" y1="87" x2="545.0" y2="118" style="stroke-width:1.4"/><line class="grid" x1="545.0" y1="142" x2="507.5" y2="173" style="stroke-width:1.4"/><text class="t-mut" x="507.5" y="215" text-anchor="middle" style="font-weight:400">BBG</text><circle class="box" cx="507.5" cy="185" r="12"/><text class="title" x="507.5" y="189" text-anchor="middle">G</text><line class="grid" x1="545.0" y1="142" x2="582.5" y2="173" style="stroke-width:1.4"/><text class="t-mut" x="582.5" y="215" text-anchor="middle" style="font-weight:400">BBB</text><circle class="box" cx="582.5" cy="185" r="12"/><text class="title" x="582.5" y="189" text-anchor="middle">B</text><circle class="box" cx="545.0" cy="130" r="12"/><text class="title" x="545.0" y="134" text-anchor="middle">B</text><circle class="box" cx="470.0" cy="75" r="12"/><text class="title" x="470.0" y="79" text-anchor="middle">B</text><circle class="box" cx="320" cy="20" r="12"/><text class="title" x="320" y="24" text-anchor="middle">·</text><text class="t-ink" x="320" y="242" text-anchor="middle">favourable: GGB, GBG, BGG → 3 of 8</text></svg><figcaption>All 2³ = 8 equally likely birth orders for three children (2024 Q7). Exactly three of them (GGB, GBG, BGG) have two girls and one boy, so the probability is 3/8 = C(3,2)/2³.</figcaption></figure>
<!-- /fig:ga-prob-tree -->

## 5.3 Mean, median and mode puzzles

For $n$ numbers:

- **sum** $= n \times$ mean;
- **median** = the middle value of the sorted list (or the average of the two middle values when $n$ is even);
- **mode** = the most frequent value. "**Single** mode" means no other value is equally frequent.

**Method:** sort the unknowns $a \le b \le c \le d \le e$, place the median, use the mode condition to fix any repeated values, then solve for the rest using the sum. Finally, check the mode is still unique.

---

## Summary: important points

<div class="formula">

1. Multiply for independent stages. Add for disjoint cases.
2. Fix the restricted position first. Use the complement for "at least".
3. Divisible by 3: choose digit sets whose sum is a multiple of 3, then arrange.
4. Repeated letters: divide by the factorial of each repeat count.
5. $P(\text{at least one}) = 1 - P(\text{none})$. Binomial: $\binom nk p^k q^{n-k}$.
6. Statistics puzzles: sum = $n$ × mean, place the median, enforce a single mode.

</div>

---

## Test yourself (A): previous-year questions

### GATE 2024 Q3 (1 mark)

How many 4-digit numbers divisible by 3 can be formed from the digits {1, 3, 4, 6, 7} without repetition?

<details>
<summary>Show solution</summary>

**Answer: 48**

The five digits sum to 21. Leaving out one digit $d$ gives a sum of $21 - d$, which is divisible by 3 only for $d = 3$ or $d = 6$. That's 2 digit sets, each with $4! = 24$ arrangements: $2 \times 24 = 48$. (I checked by enumeration.)

</details>

### GATE 2024 Q7 (2 marks)

Boy and girl are equally likely. In a family with three children, what is the probability of exactly two girls and one boy?

<details>
<summary>Show solution</summary>

**Answer: 3/8**

$\binom32(1/2)^3 = 3/8$. These are the three paths GGB, GBG, BGG in the tree above.

</details>

### GATE 2026 Q7 (2 marks)

Five integers from 0 to 20 (repetitions allowed) have mean 12, median 18 and a single mode of 20. How many such sets are there (ignoring order)?

<details>
<summary>Show solution</summary>

**Answer: 1**

- The sum is 60. Sorted, the list is $a \le b \le 18 \le d \le e$.
- 20 must appear at least twice. It can't be the median, so $d = e = 20$.
- Then $a + b = 60 - 18 - 40 = 2$, giving (0, 2) or (1, 1).
- (1, 1) would make 1 appear twice, tying with 20, so the mode wouldn't be single.

Only {0, 2, 18, 20, 20} works. (Confirmed by enumerating every possibility.)

</details>

---

## Test yourself (B): predicted 2027-style questions

**F1.** In how many ways can a committee of 3 be chosen from 5 men and 4 women so that it includes at least one woman?

<details>
<summary>Show solution</summary>

**Answer: 74**

$\binom93 - \binom53 = 84 - 10 = 74$.

</details>

**F2.** How many even 3-digit numbers can be formed from {0, 1, 2, 3, 4, 5} without repetition?

<details>
<summary>Show solution</summary>

**Answer: 52**

- Last digit 0: $5 \times 4 = 20$.
- Last digit 2 or 4: the first digit can be any of the 4 remaining non-zero digits, and the middle digit any of 4 remaining: $2 \times 4 \times 4 = 32$.

Total: $20 + 32 = 52$.

</details>

**F3.** How many distinct arrangements does the word LEVEL have?

<details>
<summary>Show solution</summary>

**Answer: 30**

$\frac{5!}{2!\,2!} = 30$.

</details>

**F4.** A die is rolled 4 times. What is the probability of at least one six? (2 decimal places)

<details>
<summary>Show solution</summary>

**Answer: 0.52**

$1 - (5/6)^4 = 0.518$.

</details>

**F5.** Five integers from 0 to 20 have mean 10, median 12 and a single mode of 15. How many such sets are there?

<details>
<summary>Show solution</summary>

**Answer: 4**

- $d = e = 15$, so $a + b = 50 - 12 - 30 = 8$ with $a \le b \le 12$.
- The candidates are (0,8), (1,7), (2,6), (3,5) and (4,4).
- (4, 4) is excluded, because it would tie with 15 for the mode.

That leaves **4**.

</details>
